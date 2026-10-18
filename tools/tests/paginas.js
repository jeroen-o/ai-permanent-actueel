const { chromium, devices } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const fs=require('fs'); const W=process.env.AIPA_WERK||require('path').resolve(__dirname,'..')+'/.werk';
const B='http://localhost:8765/';
(async()=>{ const b=await chromium.launch(); const errs=[];
const ctx=await b.newContext({viewport:{width:1280,height:900},acceptDownloads:true}); const p=await ctx.newPage();
p.on('pageerror',x=>errs.push(x.message)); p.on('console',m=>{ if(m.type()==='error') errs.push(m.text().slice(0,200)); });
// register
await p.goto(B+'register/'); await p.fill('#r-naam','Jan "Test" =1+1'); await p.fill('#r-rol','adviseur'); await p.fill('#r-mods','1,2,3'); await p.fill('#r-datum','2026-10-18'); await p.fill('#r-score','85'); await p.fill('#r-cert','AIPA-202610-ABCDE');
await p.click('text=Toevoegen aan het register'); await p.fill('#r-naam','Piet'); await p.click('text=Toevoegen aan het register');
console.log('rijen', await p.locator('#r-tabel tbody tr').count());
const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#r-csv')]); const csv=fs.readFileSync(await dl.path(),'utf8'); console.log('csv', JSON.stringify(csv.split('\r\n').slice(0,2)));
const [pop]=await Promise.all([ctx.waitForEvent('page'),p.click('#r-print')]); await pop.waitForLoadState(); console.log('print-venster', (await pop.title()), (await pop.locator('tbody tr').count())+' rijen');
await p.locator('#r-tabel button[data-i="0"]').click(); console.log('na verwijderen', await p.locator('#r-tabel tbody tr').count());
// zoeken op glossary-term en pagina
const h=await ctx.newPage(); await h.goto(B); await h.waitForSelector('#zoek-knop'); await h.waitForTimeout(800);
await h.click('#zoek-knop'); await h.keyboard.type('deepfake'); await h.waitForTimeout(400);
console.log('deepfake ->', await h.locator('#zoek-resultaten [role=option]').first().innerText().then(t=>t.split('\n').slice(0,2).join(' / ')));
await h.locator('#zoek-resultaten [role=option]').first().click(); await h.waitForURL(/begrippen/); await h.waitForTimeout(1200);
console.log('landt op', h.url(), 'dt zichtbaar', await h.evaluate(()=>{ const r=document.getElementById('deepfake').getBoundingClientRect(); return r.top>=0&&r.top<400; }));
// toetsuitleg-bronlink
await h.goto(B+'kennistoets/?mods=3&start=1'); await h.waitForTimeout(1300);
await h.locator('#toets button[style*="text-align"]').first().click(); console.log('bronlink', await h.locator('#toets a:has-text("Meer lezen")').getAttribute('href'));
// mobiel: nieuwe pagina's
const m=await (await b.newContext({...devices['iPhone 13']})).newPage();
for (const u of ['nieuw/','begrippen/','wetgeving/','register/','artikel-4-ai-geletterdheid/','over/','privacy/','404.html']) { await m.goto(B+u); await m.waitForTimeout(300);
  const sw=await m.evaluate(()=>[document.documentElement.clientWidth,document.documentElement.scrollWidth]); console.log('mobiel', u, sw[0]===sw[1]?'OK':'BREED '+sw); await m.screenshot({path:W+'/p_'+u.replace(/\W/g,'')+'.png',fullPage:true}); }
console.log('errors', errs); await b.close(); })();
