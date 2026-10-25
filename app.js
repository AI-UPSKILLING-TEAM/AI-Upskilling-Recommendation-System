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
async function handle(action, success='Saved successfully.') { try { await action(); say(success); } catch(error) { say(error.message); } }
function makeText(parent, tag, text, className='') { const el = document.createElement(tag); el.textContent = text; if(className) el.className=className; parent.append(el); return el; }
function render() {
  $('auth').hidden = true; $('dashboard').hidden = false;
  $('greeting').textContent = `Hello, ${dashboard.profile.name}`;
  $('profile-name').value = dashboard.profile.name;
  $('interests').value = dashboard.profile.interests;
  $('career-goal').value = dashboard.profile.goal || 'Data Analyst';
  const portfolio=$('portfolio-list');portfolio.replaceChildren();
  if(!dashboard.portfolio.length) makeText(portfolio,'p','No courses, projects or certifications added yet.','muted');
  for(const item of dashboard.portfolio){
    const row=document.createElement('div');row.className='progress-item';
    makeText(row,'span',item.kind.toUpperCase()+': '+item.title+' ('+item.skill+')');
    const remove=document.createElement('button');remove.className='secondary mini';remove.type='button';remove.textContent='Remove';
    remove.setAttribute('aria-label','Remove '+item.title);
    remove.addEventListener('click',()=>handle(async()=>{await request('/api/portfolio/delete','POST',{id:item.id});await refresh();}));
    row.append(remove);portfolio.append(row);
  }
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
  for(const item of a.recommendations){const row=document.createElement('div');row.className='recommendation';makeText(row,'strong',item.skill);const link=document.createElement('a');link.textContent=item.resource;link.href=item.url;link.target='_blank';link.rel='noopener noreferrer';row.append(link);makeText(row,'small',item.activity);list.append(row);}
  const progress=$('progress');progress.replaceChildren();
  for(const item of a.recommendations){
    const wrap=document.createElement('div');wrap.className='progress-item';
    const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=dashboard.completed.includes(item.skill);
    input.addEventListener('change',()=>handle(async()=>{await request('/api/progress','POST',{skill:item.skill,completed:input.checked});await refresh();}));
    label.append(input,document.createTextNode(`Practiced ${item.skill}`));wrap.append(label);progress.append(wrap);
  }
}
async function showNotifications() {
  const data=await request('/api/notifications');
  $('notifications-enabled').checked=data.enabled;
  const pane=$('notifications-list');pane.replaceChildren();
  if(!data.items.length) makeText(pane,'p','No milestones logged yet.','muted');
  for(const item of data.items) {
    const row=document.createElement('div');row.className='progress-item';
    makeText(row,'span',item.title);if(!item.read_at) {
      const button=document.createElement('button');button.className='mini secondary';button.textContent='Mark read';
      button.addEventListener('click',()=>handle(async()=>{await request('/api/notifications/read','POST',{id:item.id});await showNotifications();}));
      row.append(button);
    } pane.append(row);
  }
  $('admin-card').hidden = dashboard.profile.role !== 'admin';
  if(dashboard.profile.role === 'admin') {
    const students=await request('/api/admin/users');
    $('admin-summary').textContent=students.users.length+' registered learner accounts';
  }
}
async function refresh() { dashboard=await request('/api/dashboard'); render(); await showNotifications(); }
async function load(){
  catalog=await request('/api/catalog'); const select=$('career-goal');
  for (const goal of Object.keys(catalog.career_paths)) {const option=document.createElement('option');option.value=goal;option.textContent=goal;select.append(option);}
  for (const skill of catalog.skills){
    for(const id of ['resource-skill','portfolio-skill']){
      const option=document.createElement('option');option.value=skill;option.textContent=skill;$(id).append(option);
    }
  }
  if(token) {try{await refresh();}catch(error){token='';sessionStorage.removeItem('skillpath_token');say('Session expired. Please sign in.');}}
}
$('register-form').addEventListener('submit', event=>{event.preventDefault();handle(async()=>{await request('/api/register','POST',formData(event.target));event.target.reset();say('Account created. Sign in to continue.');});});
$('login-form').addEventListener('submit', event=>{event.preventDefault();handle(async()=>{const result=await request('/api/login','POST',formData(event.target));token=result.token;sessionStorage.setItem('skillpath_token',token);await refresh();say('Signed in.');});});
$('profile-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{await request('/api/profile','POST',formData(event.target));await refresh();});});
$('skills-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{const skills=[...event.target.querySelectorAll('input:checked')].map(x=>x.value);await request('/api/skills','POST',{skills});await refresh();});});
$('logout').addEventListener('click',()=>handle(async()=>{await request('/api/logout','POST',{});token='';sessionStorage.removeItem('skillpath_token');$('dashboard').hidden=true;$('auth').hidden=false;say('Signed out.');}));
load().catch(e=>say(`Unable to load app: ${e.message}`));

$('notifications-enabled').addEventListener('change',event=>handle(async()=>{
  await request('/api/notifications/preferences','POST',{enabled:event.target.checked});
  await showNotifications();
}));
$('admin-resource-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{
  await request('/api/admin/resources','POST',formData(event.target));
  event.target.reset();await refresh();
},'Learning resource added.');});

$('portfolio-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{
  await request('/api/portfolio/add','POST',formData(event.target));event.target.reset();await refresh();
},'Portfolio item saved.');});
$('admin-role-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{
  const data=formData(event.target);
  const skills=[...new Set(data.skills.split(',').map(s=>s.trim()).filter(Boolean))];
  await request('/api/admin/roles','POST',{role:data.role,skills});
  catalog=await request('/api/catalog');
  const select=$('career-goal');select.replaceChildren();
  for(const goal of Object.keys(catalog.career_paths)){
    const option=document.createElement('option');option.value=goal;option.textContent=goal;select.append(option);
  }
  await refresh();
},'Career-role requirements updated.');});
