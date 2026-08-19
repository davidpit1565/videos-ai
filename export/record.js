const {chromium}=require('playwright-core');
(async()=>{
  const [file,w,h,dur,out]=process.argv.slice(2);
  const W=+w,H=+h,D=+dur;
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args:['--no-sandbox','--force-device-scale-factor=1','--hide-scrollbars']});
  const ctx=await b.newContext({viewport:{width:W,height:H},deviceScaleFactor:1,
    recordVideo:{dir:out,size:{width:W,height:H}}});
  const p=await ctx.newPage();
  await p.goto('file://'+file+'?render=1');
  await p.waitForTimeout(3000);                 // let fonts settle
  await p.evaluate(()=>window.__reel.seek(0));
  await p.waitForTimeout(400);
  const t0=Date.now();
  await p.evaluate(()=>window.__reel.play());
  await p.waitForTimeout(D*1000+900);
  console.log('wall clock:',((Date.now()-t0)/1000).toFixed(1),'s for',D,'s of video');
  await ctx.close(); await b.close();
})();
