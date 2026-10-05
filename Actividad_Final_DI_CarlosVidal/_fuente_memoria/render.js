const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();const p=await b.newPage();
 await p.goto('file://'+__dirname+'/memoria.html',{waitUntil:'networkidle'});
 await p.evaluate(()=>document.fonts.ready);
 await p.pdf({path:process.argv[2]||'memoria.pdf',format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,
  headerTemplate:'<div></div>',
  footerTemplate:'<div style="width:100%;font-family:Arial;font-size:8px;color:#52606D;padding:0 18mm;display:flex;justify-content:space-between"><span>Carlos Vidal Marín · 2.º DAM · Desarrollo de Interfaces</span><span class="pageNumber"></span></div>'});
 await b.close();
})();
