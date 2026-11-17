// node render.js jobs.json  -> each job {html, w, h, out, transparent, scale}
const {chromium}=require('/opt/node-tools/node_modules/playwright');const fs=require('fs');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();
for(const j of jobs){const p=await b.newPage({viewport:{width:j.w,height:j.h},deviceScaleFactor:j.scale||1});
await p.setContent('<!doctype html><meta charset=utf-8><style>html,body{margin:0;padding:0;background:'+(j.transparent?'transparent':'#fff')+'}svg{display:block}</style>'+j.html);
await p.screenshot({path:j.out,omitBackground:!!j.transparent,clip:{x:0,y:0,width:j.w,height:j.h}});await p.close();}
await b.close()})()
