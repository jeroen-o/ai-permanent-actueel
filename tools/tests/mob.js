const { chromium, devices } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const fs=require('fs'); const REPO=process.env.AIPA_REPO||require('path').resolve(__dirname,'../..'); const ANTW=JSON.parse(fs.readFileSync((process.env.AIPA_WERK||REPO+'/tools/.werk')+'/antw.json','utf8'));
const B='http://localhost:8765/';
(async()=>{ const b=await chromium.launch(); const ctx=await b.newContext({...devices['iPhone 13']}); const p=await ctx.newPage(); const errs=[];
p.on('pageerror',x=>errs.push(x.message)); p.on('console',m=>{ if(m.type()==='error') errs.push(m.text().slice(0,200)); });
for (const u of ['', 'kennistoets/', 'en/knowledge-test/']) {
  await p.goto(B+u); await p.waitForSelector('#toets'); await p.waitForTimeout(1200);
  const breed=await p.evaluate(()=>{ const W=document.documentElement.clientWidth; return {W, sw:document.documentElement.scrollWidth, te_breed:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width>0&&(r.right>W+1)&&getComputedStyle(e).position!=='fixed';}).slice(0,5).map(e=>e.tagName+'.'+(e.id||'')+' '+Math.round(e.getBoundingClientRect().right))}; });
  console.log(u||'home', JSON.stringify(breed));
  await p.screenshot({path:(process.env.AIPA_WERK||REPO+'/tools/.werk')+'/m_'+(u.replace(/\W/g,'')||'home')+'.png', fullPage:true});
}
// mobiel: zoeken, tabs, toets spelen
await p.goto(B); await p.waitForSelector('#zoek-knop'); await p.waitForTimeout(800);
await p.tap('#zoek-knop'); await p.waitForTimeout(200); await p.fill('#zoek','privacy'); await p.waitForTimeout(300);
const box=await p.locator('#zoek-resultaten').boundingBox(); console.log('zoekdropdown', box&&[Math.round(box.x),Math.round(box.width)]);
await p.locator('#zoek-resultaten [role=option]').first().tap(); await p.waitForTimeout(1200);
await p.locator('#kc-tab-volmacht').tap(); await p.waitForTimeout(300); console.log('volmacht items', await p.locator('#kc-paneel [id^=kc-]').count());
await p.locator('#kc-modellen, [id=kc-m-dvd]').first().scrollIntoViewIfNeeded();
await p.goto(B+'kennistoets/?mods=1,2,3,4,5&start=1'); await p.waitForTimeout(1500);
for(let i=0;i<40;i++){ const ps=await p.locator('#toets p').allInnerTexts(); const v=ps.map(x=>x.trim()).find(x=>ANTW[x]); if(!v) break;
  const k=p.locator('#toets button[style*="text-align"]'); const t=(await k.allInnerTexts()).map(x=>x.replace(/^[A-D]\n/,'').trim()); await k.nth(t.indexOf(ANTW[v])).tap(); await p.locator('#toets button.btn-primary').first().tap(); await p.waitForTimeout(60); }
await p.waitForTimeout(900); const bb=await p.locator('[role=status]').boundingBox(); console.log('banner zichtbaar mobiel', bb&&Math.round(bb.y), 'canvas', await p.locator('canvas').count());
await p.screenshot({path:(process.env.AIPA_WERK||REPO+'/tools/.werk')+'/m_feest.png'});
console.log('errors', errs); await b.close(); })();
