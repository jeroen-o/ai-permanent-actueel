const { chromium } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const fs=require('fs'); const REPO=process.env.AIPA_REPO||require('path').resolve(__dirname,'../..');
const ANTW=JSON.parse(fs.readFileSync((process.env.AIPA_WERK||REPO+'/tools/.werk')+'/antw.json','utf8'));
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
for (const [pad,naam] of [['kennistoets/','NL'],['en/knowledge-test/','EN']]) {
  const gezien=new Set(); let totaal=0;
  for (let r=0;r<4;r++) {
    await p.goto('http://localhost:8765/'+pad+'?mods=1,2,3,4,5,6,7&start=1'); await p.waitForSelector('#toets .sc-interp',{timeout:15000}); await p.waitForTimeout(150);
    const meta=await p.locator('#toets .sc-interp').first().innerText(); totaal=+meta.match(/of (\d+)|van (\d+)/i).slice(1).find(Boolean);
    for (let i=0;i<totaal;i++) {
      const v=(await p.locator('#toets p').allInnerTexts()).map(x=>x.trim()).find(x=>ANTW[x]); if(!v) throw new Error('vraag niet herkend '+i);
      gezien.add(v);
      const k=p.locator('#toets button[style*="text-align"]'); const t=(await k.allInnerTexts()).map(x=>x.replace(/^[A-D]\n/,'').trim());
      await k.nth(t.indexOf(ANTW[v])).click(); await p.locator('#toets button.btn-primary').first().click(); await p.waitForTimeout(30);
    }
  }
  console.log(naam,'vragen per toets:',totaal,'| verschillende vragen gezien in 4 toetsen:',gezien.size,'van 315');
}
console.log('errors',errs); await b.close(); })();
