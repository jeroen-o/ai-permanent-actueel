const { chromium } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const REPO=process.env.AIPA_REPO||require('path').resolve(__dirname,'../..');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const e=[];
p.on('pageerror',x=>e.push('PE '+x.message)); p.on('console',m=>{ if(m.type()==='error'||m.type()==='warning') e.push(m.type()+' '+m.text().slice(0,300)); });
await p.goto('file://'+REPO+'/'+(process.argv[2]||'index.html')); await p.waitForTimeout(4000);
console.log(e.slice(0,8).join('\n')); console.log('kc items', await p.locator('#kc-paneel [id^=kc-]').count()); await b.close(); })();
