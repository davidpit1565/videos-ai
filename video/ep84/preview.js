// usage: node preview.js <scene N | all> [fractions comma list, default .1,.5,.9]  -> out/prev/sN-fK.png (1080x1920)
const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{
 const H=__dirname, cues=JSON.parse(fs.readFileSync(H+'/preview-cues.json'));
 const which=process.argv[2]||'all'; const fr=(process.argv[3]||'.1,.5,.9').split(',').map(Number);
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
 p.on('console',m=>{if(/error|warn/i.test(m.type()))console.log('[console]',m.text())});
 await p.goto('file://'+H+'/hf/'+(process.env.PAGE||'index')+'.html'); await p.waitForTimeout(800);
 fs.mkdirSync(H+'/out/prev',{recursive:true});
 const ids=which==='all'?cues.T0.map((_,i)=>i+1):[+which];
 for(const n of ids){ for(const f of fr){ const t=process.env.AT?+process.env.AT:cues.T0[n-1]+cues.DUR[n-1]*f;
   await p.evaluate(t=>{window.__reel.seek(t);return 1},t); await p.waitForTimeout(380);
   await p.screenshot({path:`${H}/out/prev/s${n}-f${f}.png`}); } }
 await b.close();
})();
