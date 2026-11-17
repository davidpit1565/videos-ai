// Real captures of live public pages (7.11.2026), Playwright chromium, dark scheme, DSF 2.
const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const O='/home/user/videos-ai/video/nextreel-git/hf/assets/cap/';
const fs=require('fs');
(async()=>{
 const b=await chromium.launch({args:['--no-sandbox']});
 const ctx=await b.newContext({viewport:{width:1280,height:1000},deviceScaleFactor:1.6,colorScheme:'dark',locale:'en-US'});
 const p=await ctx.newPage(); const meta={};
 const go=async(u)=>{await p.goto(u,{waitUntil:'domcontentloaded',timeout:45000}); await p.waitForTimeout(3500);};
 // repo page
 await go('https://github.com/git/git');
 try{await p.click('button:has-text("Accept")',{timeout:1500});}catch(e){}
 await p.screenshot({path:O+'gh-repo.jpg',type:'jpeg',quality:88});
 meta.repo={};
 for(const [k,sel] of Object.entries({fork:'a[href$="/forks"]',star:'a[href$="/stargazers"]',code:'button:has-text("Code")'})){
   try{const el=p.locator(sel).first(); const bb=await el.boundingBox(); meta.repo[k]={bb,text:(await el.innerText()).trim()};}catch(e){meta.repo[k]=null}}
 // code dropdown
 try{await p.locator('button:has-text("Code")').first().click(); await p.waitForTimeout(1800); await p.screenshot({path:O+'gh-code.jpg',type:'jpeg',quality:88});}catch(e){console.log('code ERR',e.message.slice(0,120))}
 // commits
 await go('https://github.com/git/git/commits/master/');
 await p.screenshot({path:O+'gh-commits.jpg',type:'jpeg',quality:88});
 // branches
 await go('https://github.com/git/git/branches');
 await p.screenshot({path:O+'gh-branches.jpg',type:'jpeg',quality:88});
 // git-scm (light, own scheme)
 await go('https://git-scm.com/');
 await p.screenshot({path:O+'gitscm.jpg',type:'jpeg',quality:88});
 fs.writeFileSync(O+'meta.json',JSON.stringify(meta,null,1)); console.log(JSON.stringify(meta));
 await b.close();
})();
