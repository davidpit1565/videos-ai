const { chromium } = require('playwright');
(async()=>{
 const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1400},deviceScaleFactor:1});
 await p.goto('https://github.com/Jakeschincariol/replica-skill',{waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(3000);
 await p.screenshot({path:'hf/assets/replica-repo-top.png'}); await b.close();
})();
