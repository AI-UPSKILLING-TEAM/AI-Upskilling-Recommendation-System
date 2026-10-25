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
  $('department').value=dashboard.profile.department; $('academic-year').value=dashboard.profile.academic_year; $('phone').value=dashboard.profile.phone;
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
    const wrap=document.createElement('div');wrap.className='skill-row';
    label.append(checkbox,document.createTextNode(skill));
    const level=document.createElement('select');level.dataset.skill=skill;level.setAttribute('aria-label',skill+' proficiency');
    for(const [value,text] of [[1,'Beginner'],[2,'Intermediate'],[3,'Advanced']]){const option=document.createElement('option');option.value=value;option.textContent=text;level.append(option);}
    level.value=dashboard.levels[skill] || 2;wrap.append(label,level);$('skill-options').append(wrap);
  }
  const a=dashboard.analysis;
  $('readiness').textContent = `${a.readiness_percent}%`;
  $('practice-progress').textContent = `${a.practice_progress_percent}%`;
  const gaps=$('gaps');gaps.replaceChildren();
  if(!a.career_goal) makeText(gaps,'p','Save a career goal to see your skill gaps.');
  else if(!a.gap_skills.length) makeText(gaps,'p','You have marked all required skills. Keep practicing!');
  else a.gap_skills.forEach(s=>makeText(gaps,'span',s+(a.weak_skills.includes(s)?' - needs practice':' - missing'),'tag'));
  if(a.career_goal)makeText(gaps,'p','Career goal: '+a.career_goal,'muted');
  const list=$('recommendations');list.replaceChildren();
  if(!a.recommendations.length) makeText(list,'p',a.career_goal?'No missing skills for the selected career goal.':'Save a career goal to see recommendations.');
  for(const item of a.recommendations){const row=document.createElement('div');row.className='recommendation';makeText(row,'strong',item.skill);const link=document.createElement('a');link.textContent=item.resource;link.href=item.url || '#progress';link.target='_blank';link.rel='noopener noreferrer';row.append(link);makeText(row,'small',item.reason);makeText(row,'small','Project: '+item.project);list.append(row);}
  const certs=$('certifications');certs.replaceChildren();
  if(!a.certifications.length)makeText(certs,'p','No recommended certification for this career path at present.','muted');
  for(const cert of a.certifications){
    const wrap=document.createElement('div');wrap.className='recommendation';
    const link=document.createElement('a');link.href=cert.url;link.textContent=cert.title;
    link.target='_blank';link.rel='noopener noreferrer';wrap.append(link);
    makeText(wrap,'small',cert.note);certs.append(wrap);
  }
  const progress=$('progress');progress.replaceChildren();
  for(const skill of a.required_skills){
    const item={skill};
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
    await renderAdmin();
  }
}
async function refresh() { dashboard=await request('/api/dashboard'); render(); await showNotifications(); }
async function loadCatalog(){
  catalog=await request('/api/catalog');
  const select=$('career-goal');select.replaceChildren();
  for(const goal of Object.keys(catalog.career_paths)){const option=document.createElement('option');option.value=goal;option.textContent=goal;select.append(option);}
  for(const id of ['resource-skill','portfolio-skill']){
    $(id).replaceChildren();for(const skill of catalog.skills){const option=document.createElement('option');option.value=skill;option.textContent=skill;$(id).append(option);}
  }
}
async function load(){
  await loadCatalog();
  if(token){try{await refresh();}catch(error){token='';sessionStorage.removeItem('skillpath_token');$('auth').hidden=false;$('dashboard').hidden=true;say('Please sign in again.');}}
}
$('register-form').addEventListener('submit', event=>{event.preventDefault();handle(async()=>{await request('/api/register','POST',formData(event.target));event.target.reset();},'Account created. Sign in to continue.');});
$('login-form').addEventListener('submit', event=>{event.preventDefault();handle(async()=>{const result=await request('/api/login','POST',formData(event.target));token=result.token;sessionStorage.setItem('skillpath_token',token);await refresh();},'Signed in.');});
$('profile-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{await request('/api/profile','POST',formData(event.target));await refresh();});});
$('skills-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{const skills=[...event.target.querySelectorAll('input:checked')].map(x=>x.value);const levels={};event.target.querySelectorAll('select[data-skill]').forEach(el=>{if(skills.includes(el.dataset.skill))levels[el.dataset.skill]=Number(el.value);});await request('/api/skills','POST',{skills,levels});await refresh();});});
$('logout').addEventListener('click',()=>handle(async()=>{await request('/api/logout','POST',{});token='';sessionStorage.removeItem('skillpath_token');$('dashboard').hidden=true;$('auth').hidden=false;},'Signed out.'));
load().catch(e=>say(`Unable to load app: ${e.message}`));

$('notifications-enabled').addEventListener('change',event=>handle(async()=>{
  await request('/api/notifications/preferences','POST',{enabled:event.target.checked});
  await showNotifications();
}));
$('admin-resource-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{
  const data=formData(event.target);if(data.id)data.id=Number(data.id);else delete data.id;await request('/api/admin/resources','POST',data);
  event.target.reset();await refresh();
},'Learning resource added.');});

$('portfolio-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{
  await request('/api/portfolio/add','POST',formData(event.target));event.target.reset();await refresh();
},'Portfolio item saved.');});
$('admin-role-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{
  const data=formData(event.target);
  const entries=data.skills.split(',').map(s=>s.trim()).filter(Boolean).map(s=>s.split(':'));
  const skills=[...new Set(entries.map(parts=>parts[0].trim()))],required_levels={};
  for(const parts of entries)required_levels[parts[0].trim()]=parts.length>1?Number(parts[1]):2;
  await request('/api/admin/roles','POST',{role:data.role,skills,required_levels});await loadCatalog();await refresh();
},'Career-role requirements updated.');});
function actionButton(parent,text,action){
  const button=document.createElement('button');button.type='button';button.className='secondary mini';button.textContent=text;
  button.addEventListener('click',()=>handle(action));parent.append(button);
}
async function adminChange(route,data){await request('/api/admin/'+route,'POST',data);await loadCatalog();await refresh();}
async function renderAdmin(){
  const students=await request('/api/admin/users'),resources=await request('/api/resources'),audit=await request('/api/admin/audit');
  $('admin-summary').textContent=students.users.length+' accounts registered';
  for(const id of ['resource-list','role-list','admin-skill-list','student-list','audit-list'])$(id).replaceChildren();
  for(const item of resources.custom){
    const row=document.createElement('div');row.className='management-row';makeText(row,'span',item.kind+': '+item.title+' ('+item.skill+')');
    actionButton(row,'Edit '+item.title,async()=>{const f=$('admin-resource-form');for(const key of ['id','skill','title','url','description','kind'])f.elements.namedItem(key).value=item[key];f.scrollIntoView({block:'center'});});
    actionButton(row,'Delete '+item.title,async()=>{if(confirm('Delete this shared resource?'))await adminChange('resources-delete',{id:item.id});});$('resource-list').append(row);
  }
  for(const [role,skills] of Object.entries(catalog.career_paths)){
    const row=document.createElement('div');row.className='management-row';makeText(row,'span',role+': '+skills.join(', '));
    actionButton(row,'Edit '+role,async()=>{const f=$('admin-role-form');f.elements.role.value=role;f.elements.skills.value=skills.map(s=>s+':'+catalog.required_levels[role][s]).join(', ');f.scrollIntoView({block:'center'});});
    actionButton(row,'Delete '+role,async()=>{if(confirm('Delete this career role?'))await adminChange('roles-delete',{role});});$('role-list').append(row);
  }
  for(const name of catalog.skills){
    const row=document.createElement('div');row.className='management-row';makeText(row,'span',name);
    actionButton(row,'Delete '+name,async()=>{if(confirm('Delete this skill? Skills in use are protected.'))await adminChange('skills-delete',{name});});$('admin-skill-list').append(row);
  }
  for(const student of students.users.filter(u=>u.role==='student')){
    const form=document.createElement('form');form.className='student-form';makeText(form,'strong',student.email);
    for(const [key,label] of [['name','Name'],['department','Department'],['academic_year','Academic year']]){
      const wrap=document.createElement('label');wrap.textContent=label;const input=document.createElement('input');input.name=key;input.value=student[key];input.maxLength=key==='academic_year'?30:key==='name'?80:100;input.required=key==='name';wrap.append(input);form.append(wrap);
    }
    const save=document.createElement('button');save.textContent='Save '+student.name;form.append(save);
    form.addEventListener('submit',e=>{e.preventDefault();handle(()=>adminChange('users',{...formData(form),id:student.id}));});
    actionButton(form,'Delete account '+student.name,async()=>{if(confirm('Delete this student and their learning data?'))await adminChange('users-delete',{id:student.id});});$('student-list').append(form);
  }
  for(const item of audit.audit.slice(0,15))makeText($('audit-list'),'p',item.action+' | '+item.target+' | '+new Date(item.created_at*1000).toLocaleString(),'muted');
}
$('admin-skill-form').addEventListener('submit',event=>{event.preventDefault();handle(async()=>{await adminChange('skills',formData(event.target));event.target.reset();});});
