const { chromium } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const fs=require('fs'); const REPO=process.env.AIPA_REPO||require('path').resolve(__dirname,'..'); const WERK=process.env.AIPA_WERK||__dirname+'/.werk';
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1280,height:900}});
  const pagina=process.argv[2]||'index.html', uit=process.argv[3]||'static.html';
  await p.goto('file://'+REPO+'/'+pagina); await p.waitForSelector('#toets',{timeout:30000}); await p.waitForTimeout(1200);
  const faq=(process.argv[2]||'index.html')==='index.html'?JSON.parse(fs.readFileSync(WERK+'/faq_all.json','utf8')):null;
  const html=await p.evaluate((faq)=>{
    const root=document.body.cloneNode(true);
    root.querySelectorAll('button[aria-pressed]').forEach(e=>{ const sp=document.createElement('span'); sp.textContent=e.textContent.trim()+' · '; e.replaceWith(sp); });
    root.querySelectorAll('script,style,svg,img,input,textarea,button,form,details,label,[role=search],[role=tablist],[role=status],canvas,mark').forEach(e=>{
      if(e.tagName==='MARK') e.replaceWith(e.textContent); else e.remove(); });
    root.querySelectorAll('a[aria-label="Terug naar home"]').forEach(e=>e.remove());
    // FAQ volledig uitschrijven
    const fs_=root.querySelector('#faq'); if(fs_&&faq){ const lijst=fs_.querySelector('div[style*="grid-column"]')||fs_; lijst.innerHTML=faq.map(f=>`<h3>${f.v}</h3><p>${f.a}</p>`).join(''); }
    const keep=new Set(['href','id']);
    root.querySelectorAll('*').forEach(e=>{ [...e.attributes].forEach(a=>{ if(!keep.has(a.name)) e.removeAttribute(a.name); }); });
    // lege elementen weg
    for(let i=0;i<4;i++) root.querySelectorAll('div,span,p,section,nav').forEach(e=>{ if(!e.textContent.trim()) e.remove(); });
    // overbodige div/span-nesting uitpakken
    root.querySelectorAll('div,span').forEach(e=>{ if(e.children.length===1&&e.childNodes.length===1&&!e.id) e.replaceWith(e.firstElementChild); });
    let h=root.innerHTML.replace(/<x-dc>|<\/x-dc>/g,'').replace(/\n\s*\n+/g,'\n');
    return h;
  },faq);
  fs.writeFileSync(WERK+'/'+uit,html); console.log(html.length);
  if(process.argv[2]){ await b.close(); return; }
  // OG-afbeelding
  const o=await b.newPage({viewport:{width:1200,height:630}});
  await o.setContent(`<html><body style="margin:0;width:1200px;height:630px;background:#1462ad;color:#fff;font-family:Arial,Helvetica,sans-serif;display:flex;flex-direction:column;justify-content:space-between;padding:72px;box-sizing:border-box">
  <div style="font-size:24px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;opacity:.85">Een activiteit van DFO BV</div>
  <div><div style="font-size:104px;font-weight:900;letter-spacing:-.03em;line-height:.95">AI Permanent<br>Actueel</div>
  <div style="font-size:32px;margin-top:28px;max-width:960px;line-height:1.3">AI-geletterdheid en klantcommunicatie voor hypotheek-, assurantie- en kredietadviseurs en volmachtbedrijven</div></div>
  <div style="font-size:26px;font-weight:700">ai-permanent-actueel.nl</div></body></html>`);
  await o.screenshot({path:REPO+'/og-image.png'});
  await b.close();
})();
