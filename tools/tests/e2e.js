const { chromium } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const fs=require('fs'); const REPO=process.env.AIPA_REPO||require('path').resolve(__dirname,'../..'); const ANTW=JSON.parse(fs.readFileSync((process.env.AIPA_WERK||REPO+'/tools/.werk')+'/antw.json','utf8'));
const B='http://localhost:8765/';
async function speel(p, goed){
  let i=0;
  for(;i<40;i++){
    const ps=await p.locator('#toets p').allInnerTexts(); const vraag=ps.map(x=>x.trim()).find(x=>ANTW[x]);
    if(!vraag) break;
    const knoppen=p.locator('#toets button[style*="text-align: left"], #toets button[style*="text-align:left"]');
    const teksten=(await knoppen.allInnerTexts()).map(t=>t.replace(/^[A-D]\n/,'').trim());
    let idx=teksten.findIndex(t=>(goed===null||i<goed)?t===ANTW[vraag]:t!==ANTW[vraag]);
    if(idx<0){ console.log("GEEN MATCH", JSON.stringify(vraag), JSON.stringify(ANTW[vraag]), JSON.stringify(teksten)); return i; }
    await knoppen.nth(idx).click();
    await p.locator('#toets button.btn-primary').first().click(); await p.waitForTimeout(60);
  }
  return i;
}
(async()=>{ const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:1280,height:900},acceptDownloads:true}); const p=await ctx.newPage(); const errs=[];
p.on('pageerror',x=>errs.push(x.message)); p.on('console',m=>{ if(m.type()==='error') errs.push(m.text().slice(0,200)); });
await p.goto(B); await p.waitForSelector('#gratis'); await p.waitForTimeout(800);
const [dl]=await Promise.all([p.waitForEvent('download'), p.click('text=Zet in mijn agenda (Outlook, Apple)')]);
const ics=fs.readFileSync(await dl.path(),'utf8'); console.log('ics', dl.suggestedFilename(), ics.split('\r\n').filter(l=>/DTSTART|RRULE|TRIGGER/.test(l)).join(' | '));
console.log('google', (await p.getAttribute('a:has-text("Google Agenda")','href')).slice(0,160));
await p.click('#zoek-knop'); await p.waitForTimeout(200); await p.keyboard.type('shadow'); await p.waitForTimeout(500);
console.log('zoek via vergrootglas', await p.locator('#zoek-resultaten [role=option]').count(), 'scrollY', await p.evaluate(()=>scrollY));
await p.keyboard.press('Escape');
await p.fill('#tip-adressen','a@b.nl; fout'); await p.click('text=Zet de mail klaar'); await p.waitForTimeout(200);
console.log('tip fout:', await p.locator('#tip [role=alert]').innerText());
await p.fill('#tip-adressen','a@b.nl, c@d.nl'); await p.fill('#tip-naam','Jan');
await p.evaluate(()=>{ window.__nav=[]; const d=Object.getOwnPropertyDescriptor(window.location.__proto__,'href'); });
p.on('request',r=>{});
const mail=await p.evaluate(()=>new Promise(res=>{ const org=window.location; window.addEventListener('beforeunload',()=>{}); 
  const h=Object.getOwnPropertyDescriptor(Location.prototype,'href'); try{ Object.defineProperty(Location.prototype,'href',{set(v){res(v);},get(){return h.get.call(this);},configurable:true}); }catch(e){ res('kan niet onderscheppen'); }
  document.evaluate("//button[contains(.,'Zet de mail klaar')]",document,null,9,null).singleNodeValue.click(); setTimeout(()=>res('geen navigatie'),500); }));
console.log('mailto', decodeURIComponent(mail).slice(0,120));
await p.reload(); await p.waitForSelector('#pakket'); await p.waitForTimeout(800);
await p.locator('#pakket button[aria-pressed]').nth(1).click(); await p.click('text=Toets over mijn pakket'); await p.waitForURL(/kennistoets/); await p.waitForTimeout(1500);
console.log('url', p.url(), '| meta:', await p.locator('#toets .sc-interp').filter({hasText:'Vraag 1 van'}).first().innerText());
await speel(p,null); await p.waitForTimeout(400);
console.log('banner', await p.locator('[role=status]').innerText(), '| canvas', await p.locator('canvas').count());
await p.screenshot({path:(process.env.AIPA_WERK||REPO+'/tools/.werk')+'/feest.png'});
await p.waitForTimeout(4500); console.log('canvas na 4.5s', await p.locator('canvas').count());
await p.click('text=Opnieuw'); await p.click('text=Alle modules'); await p.click('text=/Start de toets/'); await speel(p,3); await p.waitForTimeout(300);
console.log('onvoldoende banner', await p.locator('[role=status]').count(), '| canvas', await p.locator('canvas').count());
await p.goto(B+'en/knowledge-test/'); await p.waitForSelector('#toets'); await p.waitForTimeout(1000);
await p.click('text=All modules'); await p.click('text=/Start the test/'); await speel(p,null); await p.waitForTimeout(400);
console.log('EN banner', await p.locator('[role=status]').innerText(), '|', (await p.locator('#toets').innerText()).split('\n').slice(1,4).join(' | '));
await p.screenshot({path:(process.env.AIPA_WERK||REPO+'/tools/.werk')+'/en.png'});
await p.goto(B+'kennistoets/'); await p.waitForSelector('#toets'); await p.waitForTimeout(800);
await p.click('header >> text=Klantcommunicatie'); await p.waitForURL(u=>u.hash==='#klantcommunicatie'); await p.waitForTimeout(1500);
console.log('naar home hash', p.url(), Math.round(await p.evaluate(()=>document.getElementById('klantcommunicatie').getBoundingClientRect().top)));
console.log('errors', errs); await b.close(); })();
