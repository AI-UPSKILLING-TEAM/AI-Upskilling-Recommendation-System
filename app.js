const $ = id => document.getElementById(id);
let token = sessionStorage.getItem('skillpath_token') || '';
let catalog = null;
let dashboard = null;
const say = msg => { $('message').textContent = msg; };
async function request(route, method='GET', body=null) {
  const headers = {};
  if (body !== null) headers['Content-Type'] = 'application/json';
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const response = await fetch(route, {method, headers, body: body === null ? null : JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}
function formData(form) { return Object.fromEntries(new FormData(form)); }
async function handle(action) { try { await action(); say('Saved successfully.'); } catch(error) { say(error.message); } }
function makeText(parent, tag, text, className='') { const el = document.createElement(tag); el.textContent = text; if(className) el.className=className; parent.append(el); return el; }
function render() {
  $('auth').hidden = true; $('dashboard').hidden = false;
  $('greeting').textContent = `Hello, ${dashboard.profile.name}`;
  $('profile-name').value = dashboard.profile.name;
  $('interests').value = dashboard.profile.interests;
  $('career-goal').value = dashboard.profile.goal || 'Data Analyst';
  $('skill-options').replaceChildren();
  for (const skill of catalog.skills) {
    const label=document.createElement('label'); const checkbox=document.createElement('input');
    checkbox.type='checkbox'; checkbox.name='skills'; checkbox.value=skill; checkbox.checked=dashboard.skills.includes(skill);
    label.append(checkbox,document.createTextNode(skill)); $('skill-options').append(label);
  }
  const a=dashboard.analysis;
  $('readiness').textContent = `${a.readiness_percent}%`;
  const gaps=$('gaps');gaps.replaceChildren();
  if(!a.career_goal) makeText(gaps,'p','Save a career goal to see your skill gaps.');
  else if(!a.missing_skills.length) makeText(gaps,'p','You have marked all required skills. Keep practicing!');
  else a.missing_skills.forEach(s=>makeText(gaps,'span',s,'tag'));
  const list=$('recommendations');list.replaceChildren();
  if(!a.recommendations.length) makeText(list,'p','No missing skills for the selected career goal.');
  for(const item of a.recommendations){const row=document.createElement('div');row.className='recommendation';makeText(row,'strong',item.skill);makeText(row,'div',item.resource);makeText(row,'small',item.activity);list.append(row);}
  const progress=$('progress');progress.replaceChildren();
  for(const item of a.recommendations){
    const wrap=document.createElement('div');wrap.className='progress-item';
    const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=dashboard.completed.includes(item.skill);
    input.addEventListener('change',()=>handle(async()=>{await request('/api/progress','POST',{skill:item.skill,completed:input.checked});await refresh();}));
    label.append(input,document.createTextNode(`Practiced ${item.skill}`));wrap.append(label);progress.append(wrap);
  }
}
async function refresh() { dashboard=await request('/api/dashboard'); render(); }
async function load(){
  catalog=await request('/api/catalog'); const select=$('career-goal');
  for (const goal of Object.keys(catalog.career_paths)) {const option=document.createElement('option');option.value=goal;option.textContent=goal;select.append(option);}
  if(token) {try{await refresh();}catch(error){token='';sessionStorage.removeItem('skillpath_token');say('Session expired. Please sign in.');}}
}
$('register-form').addEventListener('submit', event=>{event.preventDefault();handle(async()=>{await request('/api/register','POST',formData(event.target));event.target.reset();say('Account created. Sign in to continue.');});});
$('login-form').addEventListener('submit', event=>{event.preventDefault();handle(async()=>{const result=await request('/api/login','POST',formData(event.target));token=result.token;sessionStorage.setItem('skillpath_token',token);await refresh();say('Signed in.');});});
$('profile-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{await request('/api/profile','POST',formData(event.target));await refresh();});});
$('skills-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{const skills=[...event.target.querySelectorAll('input:checked')].map(x=>x.value);await request('/api/skills','POST',{skills});await refresh();});});
$('logout').addEventListener('click',()=>handle(async()=>{await request('/api/logout','POST',{});token='';sessionStorage.removeItem('skillpath_token');$('dashboard').hidden=true;$('auth').hidden=false;say('Signed out.');}));
load().catch(e=>say(`Unable to load app: ${e.message}`));
