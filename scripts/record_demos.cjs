/* Capture actual browser sessions against the working local app, with disposable data. */
const {chromium}=require('playwright');
const {spawn,spawnSync}=require('node:child_process');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),out=path.join(root,'evidence','videos');fs.mkdirSync(out,{recursive:true});
const python=process.env.PYTHON || (process.platform==='win32'?'python':'python3');
const env={...process.env,UPSKILL_DB:path.resolve(process.env.DEMO_DB || path.join(out,'recording.db')),PORT:'8766',HOST:'127.0.0.1'};
const base='http://127.0.0.1:8766';
const log=fs.openSync(path.join(out,'recording-server.log'),'w'),server=spawn(python,['app.py'],{cwd:root,env,stdio:['ignore',log,log]});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function fill(page,form,values){for(const [name,value] of Object.entries(values)){const el=page.locator(form+' [name="'+name+'"]');if(await el.evaluate(x=>x.tagName)==='SELECT')await el.selectOption(value);else await el.fill(value);}}
async function submit(page,form){await page.locator(form+' button[type="submit"]').click();}
async function account(page,email){await fill(page,'#register-form',{name:'Demo Student',email,password:'DemoPass2026!'});await submit(page,'#register-form');await page.getByText('Account created. Sign in to continue.',{exact:true}).waitFor();await fill(page,'#login-form',{email,password:'DemoPass2026!'});await submit(page,'#login-form');await page.locator('#dashboard').waitFor({state:'visible'});}
(async()=>{
 let browser;
 try{
  for(let i=0;i<60;i++){try{if((await fetch(base+'/health')).ok)break;}catch{}await sleep(100);}
  browser=await chromium.launch({headless:true});
  for(const sprint of [1,2]){
   const duration=sprint===1?60:120;
   const context=await browser.newContext({viewport:{width:1280,height:720},recordVideo:{dir:out,size:{width:1280,height:720}}});
   const page=await context.newPage(),start=Date.now(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   const at=async seconds=>{await sleep(Math.max(0,seconds*1000-(Date.now()-start)));};
   await page.goto(base);await at(4);
   const email='sprint'+sprint+'-'+Date.now()+'@example.com';await account(page,email);await at(12);
   await fill(page,'#profile-form',{name:'Demo Student',goal:sprint===1?'Data Analyst':'Cloud Engineer',department:'CSE (AI & ML)',academic_year:'Year 3',interests:sprint===1?'data analysis':'cloud infrastructure linux'});
   await submit(page,'#profile-form');await at(20);
   await page.locator('#skills-form input[value="Python"]').check();await page.locator('select[data-skill="Python"]').selectOption(sprint===1?'2':'1');await submit(page,'#skills-form');await at(28);
   await page.locator('#gaps').scrollIntoViewIfNeeded();await at(sprint===1?39:40);
   if(sprint===2){
    await page.locator('#portfolio-form').scrollIntoViewIfNeeded();await fill(page,'#portfolio-form',{kind:'project',title:'Cloud service architecture',skill:'Cloud Fundamentals'});await submit(page,'#portfolio-form');await at(49);
   }
   await page.locator('#notifications-enabled').scrollIntoViewIfNeeded();await page.locator('#notifications-enabled').check();await page.locator('#progress input').first().check();await at(sprint===1?51:60);
   if(sprint===2){
    await page.reload();await page.locator('#practice-progress').scrollIntoViewIfNeeded();await at(70);
    const promoted=spawnSync(python,['app.py','promote-admin',email],{cwd:root,env});if(promoted.status!==0)throw Error('Admin setup failed');
    await page.reload();await page.locator('#admin-card').scrollIntoViewIfNeeded();await at(80);
    await fill(page,'#admin-resource-form',{skill:'Linux',title:'Ubuntu command-line practice',url:'https://ubuntu.com/tutorials/command-line-for-beginners',description:'Official Linux command-line exercises'});await submit(page,'#admin-resource-form');await at(91);
    await page.locator('#admin-role-form').scrollIntoViewIfNeeded();await fill(page,'#admin-role-form',{role:'Cloud Engineer',skills:'Linux:2, Networking:2, Python:2, Cloud Fundamentals:2, Git:2'});await submit(page,'#admin-role-form');await at(102);
    await page.locator('#audit-list').scrollIntoViewIfNeeded();await at(111);
   }
   await page.reload();await page.locator('#gaps').scrollIntoViewIfNeeded();await at(duration);
   const video=page.video();await context.close();await video.saveAs(path.join(out,'sprint-'+sprint+'-raw.webm'));
   if(errors.length)throw Error(errors.join('; '));console.log('Recorded sprint '+sprint+' ('+duration+' seconds)');
  }
 }finally{if(browser)await browser.close();server.kill();fs.closeSync(log);}
})().catch(e=>{console.error(e);process.exitCode=1;});
