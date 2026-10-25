/* Real-browser acceptance test. Use only disposable local accounts and database. */
const {chromium}=require('playwright');
const {spawn,spawnSync}=require('node:child_process');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const out=path.resolve(process.env.EVIDENCE_DIR || path.join(root,'evidence'));
fs.mkdirSync(out,{recursive:true});
const db=path.join(out,'browser-test-'+Date.now()+'.db');
const python=process.env.PYTHON || (process.platform==='win32'?'python':'python3');
const port=process.env.TEST_PORT || '8765',base='http://127.0.0.1:'+port;
const log=fs.openSync(path.join(out,'browser-server.log'),'w');
const env={...process.env,UPSKILL_DB:db,HOST:'127.0.0.1',PORT:port};
const server=spawn(python,['app.py'],{cwd:root,env,stdio:['ignore',log,log]});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function ready(){for(let i=0;i<60;i++){try{if((await fetch(base+'/health')).ok)return;}catch{}await sleep(100);}throw Error('Server startup failed');}
async function fillForm(page,selector,values){for(const [name,value] of Object.entries(values)){const el=page.locator(selector+' [name="'+name+'"]');if(await el.evaluate(x=>x.tagName)==='SELECT')await el.selectOption(value);else await el.fill(value);}}
async function submit(page,form){await page.locator(form+' button[type="submit"]').click();}
async function saved(page){await page.waitForFunction(()=>document.getElementById('message').textContent==='Saved successfully.');}
(async()=>{
 let browser,context;
 const results=[];
 try{
  await ready();
  browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXE?{executablePath:process.env.BROWSER_EXE}:{})});
  context=await browser.newContext({viewport:{width:1365,height:900}});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);
  await fillForm(page,'#register-form',{name:'Demo Student',email:'student@example.com',password:'DemoPass2026!'});await submit(page,'#register-form');
  await page.getByText('Account created. Sign in to continue.',{exact:true}).waitFor();
  await fillForm(page,'#login-form',{email:'student@example.com',password:'DemoPass2026!'});await submit(page,'#login-form');await page.locator('#dashboard').waitFor({state:'visible'});
  await fillForm(page,'#profile-form',{name:'Demo Student',goal:'Data Analyst',interests:'data analytics python',department:'CSE (AI & ML)',academic_year:'Year 3'});await submit(page,'#profile-form');await saved(page);
  await page.locator('#skills-form input[value="Python"]').check();await page.locator('select[data-skill="Python"]').selectOption('1');
  await page.locator('#skills-form input[value="SQL"]').check();await page.locator('select[data-skill="SQL"]').selectOption('3');
  await submit(page,'#skills-form');await page.waitForFunction(()=>document.getElementById('readiness').textContent==='20%');
  assert((await page.locator('#gaps').innerText()).includes('Python - needs practice'));
  assert((await page.locator('#recommendations').innerText()).includes('Project:'));
  await fillForm(page,'#portfolio-form',{kind:'project',title:'Student database analysis',skill:'SQL'});await submit(page,'#portfolio-form');await page.getByText('PROJECT: Student database analysis (SQL)',{exact:true}).waitFor();
  await page.locator('#notifications-enabled').check();await page.locator('#progress input').first().check();
  await page.waitForFunction(()=>document.getElementById('practice-progress').textContent==='20%');
  await page.reload();await page.getByText('PROJECT: Student database analysis (SQL)',{exact:true}).waitFor();
  assert.equal(await page.locator('#academic-year').inputValue(),'Year 3');
  await page.evaluate(require('axe-core').source);
  const accessibility=await page.evaluate(async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}}));
  fs.writeFileSync(path.join(out,'accessibility.json'),JSON.stringify({violations:accessibility.violations,passes:accessibility.passes.length,incomplete:accessibility.incomplete.length},null,2));
  assert.equal(accessibility.violations.length,0,JSON.stringify(accessibility.violations.map(v=>({id:v.id,description:v.description,nodes:v.nodes.map(n=>n.target)}))));
  results.push('axe-core WCAG 2.1 A/AA automated scan: zero violations');
  await page.screenshot({path:path.join(out,'student-dashboard.png'),fullPage:true});results.push('Student registration, login, academics, weak skills, projects, progress and reload passed');
  await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(out,'mobile-dashboard.png'),fullPage:true});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));results.push('390px mobile viewport: no horizontal overflow');
  await page.setViewportSize({width:1365,height:900});
  const promote=spawnSync(python,['app.py','promote-admin','student@example.com'],{cwd:root,env,encoding:'utf8'});assert.equal(promote.status,0,promote.stderr);
  await page.reload();await page.locator('#admin-card').waitFor({state:'visible'});
  await page.locator('#admin-skill-form input').fill('Docker');await page.locator('#admin-skill-form button').click();await page.getByRole('button',{name:'Delete Docker',exact:true}).waitFor();
  await fillForm(page,'#admin-role-form',{role:'Platform Engineer',skills:'Docker:3, Linux:2'});await submit(page,'#admin-role-form');await page.getByRole('button',{name:'Edit Platform Engineer',exact:true}).waitFor();
  await fillForm(page,'#admin-resource-form',{skill:'Docker',title:'Docker getting started',url:'https://docs.docker.com/get-started/',description:'Container fundamentals'});await submit(page,'#admin-resource-form');await page.getByRole('button',{name:'Edit Docker getting started',exact:true}).waitFor();
  await page.getByRole('button',{name:'Edit Docker getting started',exact:true}).click();await page.locator('#admin-resource-form [name="title"]').fill('Docker official guide');await submit(page,'#admin-resource-form');await page.getByRole('button',{name:'Edit Docker official guide',exact:true}).waitFor();
  await page.screenshot({path:path.join(out,'admin-dashboard.png'),fullPage:true});
  results.push('Admin skill creation, career role/target levels, course creation and editing passed');
  assert.deepEqual(errors,[]);results.push('No uncaught browser JavaScript exceptions');
  fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({passed:true,results,viewport:[1365,900],mobile:[390,844],recorded_at:new Date().toISOString()},null,2));
  console.log(JSON.stringify({passed:true,results},null,2));
 }finally{if(context)await context.close();if(browser)await browser.close();server.kill();fs.closeSync(log);}
})().catch(e=>{console.error(e);process.exitCode=1;});
