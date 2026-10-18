const { chromium, devices } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const fs=require('fs'); const REPO=process.env.AIPA_REPO||require('path').resolve(__dirname,'../..'); const ANTW=JSON.parse(fs.readFileSync((process.env.AIPA_WERK||REPO+'/tools/.werk')+'/antw.json','utf8'));
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1280,height:900}}); const errs=[];
p.on('pageerror',x=>errs.push(x.message));
await p.goto('http://localhost:8765/'); await p.waitForSelector('#toets'); await p.waitForTimeout(1000);
for (const [link,id] of [['Klantcommunicatie','klantcommunicatie'],['Kantoorscan','scan'],['Vragen','faq']]) {
  await p.click('header nav >> text='+link); await p.waitForTimeout(1200);
  const r=await p.evaluate(id=>({kop:document.querySelector('header').getBoundingClientRect().bottom, titel:document.querySelector('#'+id+' h2').getBoundingClientRect().top}),id);
  console.log(link, 'header-onderkant', Math.round(r.kop), 'h2-top', Math.round(r.titel), r.titel>=r.kop?'OK':'VERSTOPT'); }
await p.goto('http://localhost:8765/#klantcommunicatie'); await p.waitForTimeout(2000);
console.log('directe link', await p.evaluate(()=>{ const k=document.querySelector('header').getBoundingClientRect().bottom, t=document.querySelector('#klantcommunicatie h2').getBoundingClientRect().top; return Math.round(k)+' / '+Math.round(t)+(t>=k?' OK':' VERSTOPT'); }));
console.log('zoekveld zichtbaar voor klik', await p.locator('#zoek').count(), 'gratis-zoekform', await p.locator('#gratis form').count(), 'DFO BV in header', await p.locator('header >> text=DFO BV').count());
await p.click('#zoek-knop'); await p.keyboard.type('deepfake'); await p.waitForTimeout(300);
console.log('resultaten', await p.locator('#zoek-resultaten [role=option]').count(), 'focus', await p.evaluate(()=>document.activeElement.id));
await p.screenshot({path:(process.env.AIPA_WERK||REPO+'/tools/.werk')+'/zoek.png'});
await p.keyboard.press('Escape'); await p.waitForTimeout(200); console.log('na esc paneel', await p.locator('#zoek-paneel').count(), 'focus', await p.evaluate(()=>document.activeElement.id));
await p.click('#zoek-knop'); await p.click('h1'); await p.waitForTimeout(200); console.log('klik buiten sluit', await p.locator('#zoek-paneel').count());
// vragenbank
const tellen={}; for(let r=0;r<3;r++){ await p.goto('http://localhost:8765/kennistoets/?mods=3&start=1'); await p.waitForTimeout(1300);
  const v=(await p.locator('#toets p').allInnerTexts()).map(x=>x.trim()).find(x=>ANTW[x]); tellen[v]=(tellen[v]||0)+1; }
console.log('verschillende eerste vragen in 3 rondes (module 3):', Object.keys(tellen).length, '| ANTW kent', Object.keys(ANTW).length);
await p.goto('http://localhost:8765/kennistoets/'); await p.waitForTimeout(1200); await p.click('text=Alle modules'); console.log(await p.locator('text=/Start de toets/').innerText());
await p.goto('http://localhost:8765/privacy/'); console.log('privacy', await p.title());
console.log('errors', errs); await b.close(); })();
