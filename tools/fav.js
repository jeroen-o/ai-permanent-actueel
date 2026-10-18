const { chromium } = (()=>{ try{ return require('playwright'); }catch(e){ return require('/opt/node-tools/node_modules/playwright'); } })();
const fs=require('fs'); const REPO=process.env.AIPA_REPO||require('path').resolve(__dirname,'..'); const WERK=process.env.AIPA_WERK||__dirname+'/.werk';
(async()=>{ const b=await chromium.launch(); const svg=fs.readFileSync(REPO+'/favicon.svg','utf8');
for (const [n,f] of [[16,WERK+'/f16.png'],[32,WERK+'/f32.png'],[48,WERK+'/f48.png'],[180,REPO+'/apple-touch-icon.png'],[192,REPO+'/icon-192.png'],[512,REPO+'/icon-512.png']]) {
  const p=await b.newPage({viewport:{width:n,height:n}});
  const s = n===180 ? svg.replace('rx="10"','rx="0"') : svg;
  await p.setContent(`<html><body style="margin:0;background:transparent">${s.replace('<svg ','<svg width="'+n+'" height="'+n+'" ')}</body></html>`);
  await p.screenshot({path:f, omitBackground: n!==180}); await p.close(); }
await b.close(); })();
