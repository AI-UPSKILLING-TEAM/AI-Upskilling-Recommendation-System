/* Safety-gate tests for release automation; these never contact GitHub. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
const yaml=fs.readFileSync(path.join(root,'.github/workflows/release.yml'),'utf8');
const source=yaml.split('          script: |')[1].split(/\r?\n/).slice(1).map(line=>line.startsWith('            ')?line.slice(12):line).join('\n');
const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
const execute=new AsyncFunction('github','context','core','require',source);
const sha='a'.repeat(40),head='b'.repeat(40);
const tests=[];
async function scenario(name,options={},expectedError=false){
 const writes=[];let released=false;
 const context={repo:{owner:'example',repo:'project'},payload:{workflow_run:{head_sha:sha,head_repository:{full_name:options.foreign?'foreign/project':'example/project'},html_url:'https://example.invalid/run'}}};
 const pr={merged:true,base:{ref:'main'},merge_commit_sha:options.wrongMerge?'e'.repeat(40):sha,head:{sha:head},user:{login:'author'},html_url:'https://example.invalid/pr'};
 const reviews=options.noApproval?[]:[{state:'APPROVED',commit_id:options.stale?'f'.repeat(40):head,user:{login:options.author?'author':'reviewer'},submitted_at:'2026-10-26T00:00:00Z'}];
 let release={id:1,draft:true,assets:[],html_url:'https://example.invalid/release'};
 const getReviews=async()=>({data:reviews}),getReleases=async()=>({data:[]});
 const mutation=name=>writes.push(name);
 const github={paginate:async fn=>(await fn()).data,rest:{
  pulls:{get:async()=>({data:pr}),listReviews:getReviews},
  git:{getRef:async()=>{if(options.wrongTag)return {data:{object:{type:'commit',sha:'f'.repeat(40)}}};throw Object.assign(Error('missing'),{status:404});},
   getTag:async()=>({data:{object:{sha}}}),createTag:async()=>{mutation('tag');return {data:{sha:'c'.repeat(40)}};},createRef:async()=>{mutation('ref');},
   getCommit:async()=>({data:{tree:{sha:'d'.repeat(40)}}}),getTree:async()=>({data:{tree:['Project_22_Report.pdf','evidence/videos/Sprint_1_Demo.mp4','evidence/videos/Sprint_2_Demo.mp4'].map((p,i)=>({path:p,type:'blob',sha:String(i)}))}}),
   getBlob:async()=>({data:{content:Buffer.from('disposable test asset').toString('base64'),encoding:'base64'}})},
  repos:{listReleases:getReleases,createRelease:async p=>{assert.equal(p.draft,true);mutation('draft');return {data:release};},
   uploadReleaseAsset:async p=>{assert.equal(released,false);mutation('upload');release.assets.push({name:p.name,state:'uploaded',digest:'sha256:'+crypto.createHash('sha256').update(p.data).digest('hex')});return {data:{}};},
   getRelease:async()=>({data:release}),updateRelease:async p=>{assert.equal(release.assets.length,3);released=true;mutation('publish');release={...release,...p};return {data:release};}},
  issues:{update:async p=>{assert.equal(released,true,'Issue closure must follow verified publication');assert.equal(p.state,'closed');mutation('close-'+p.issue_number);}}
 }};
 const core={notice:()=>{},summary:{addHeading(){return this;},addLink(){return this;},addRaw(){return this;},async write(){}}};
 if(expectedError){await assert.rejects(execute(github,context,core,require));assert.deepEqual(writes,[],'No write may precede acceptance gate');}
 else{await execute(github,context,core,require);if(options.wrongMerge)assert.deepEqual(writes,[]);else{assert.equal(writes.filter(x=>x.startsWith('close-')).length,16);assert.equal(released,true);}}
 tests.push({name,passed:true});
}
(async()=>{
 await scenario('missing independent approval blocks publication',{noApproval:true},true);
 await scenario('author cannot self-approve',{author:true},true);
 await scenario('approval of an older revision is rejected',{stale:true},true);
 await scenario('foreign repository is rejected',{foreign:true},true);
 await scenario('unrelated main commit cannot release',{wrongMerge:true});
 await scenario('existing release tag cannot be moved',{wrongTag:true},true);
 await scenario('valid reviewed merge verifies assets before release and issue closure');
 const out=path.join(root,'evidence');fs.mkdirSync(out,{recursive:true});
 fs.writeFileSync(path.join(out,'release-gate-tests.json'),JSON.stringify({simulation_only:true,real_release_not_executed:true,tests},null,2));
 console.log(JSON.stringify({passed:tests.length,simulation_only:true,tests},null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
