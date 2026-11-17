const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:800}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.goto('file://'+process.cwd()+'/index.html');
const r=await p.evaluate(()=>{const c=document.createElement('canvas');c.width=880;c.height=760;const g=CatGame.make(c);const out=[];for(const T of [3,8,14]){g.simulateTo(T);const s=g.state();out.push([T,s.score,s.lives,s.over])}return out});
console.log(JSON.stringify(r),errs);
await p.evaluate(()=>{const g=CatGame.make(document.getElementById('c'));window.__g=g;g.simulateTo(6.3)});await p.waitForTimeout(100);
await p.screenshot({path:'shot.png'});await b.close()})()
