# ---------- geslaagd: HOERA-banner + confetti ----------
t = sub1('''        <span style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700">Resultaat</span>''',
'''        <sc-if value="{{ geslaagd }}" hint-placeholder-val="{{ false }}">
          <div role="status" aria-live="polite" style="background:var(--color-accent);color:var(--color-bg);padding:var(--space-4) var(--space-6);font-size:clamp(30px,5.5vw,56px);font-weight:900;letter-spacing:-0.02em;line-height:1">HOERA! GESLAAGD 🎉</div>
        </sc-if>
        <span style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700">Resultaat</span>''', t)
t = sub1("volgende:()=>this.setState(st=>st.idx+1<st.reeks.length?{idx:st.idx+1,keuze:null}:{fase:'klaar',keuze:null}),",
         "volgende:()=>this.setState(st=>st.idx+1<st.reeks.length?{idx:st.idx+1,keuze:null}:{fase:'klaar',keuze:null},()=>{ const st=this.state; if(st.fase!=='klaar') return; setTimeout(()=>{ const el=document.querySelector('#toets [role=status]')||document.querySelector('#toets .sc-interp')||document.getElementById('toets'); if(el) this.scrollNaarEl(el,false); },30); if(st.reeks.length&&Math.round(st.goed/st.reeks.length*100)>=70) this.confetti(); }),", t)
CONFETTI = r'''
  confetti(){
    if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const c=document.createElement('canvas'), dpr=window.devicePixelRatio||1, W=window.innerWidth, H=window.innerHeight;
    c.width=W*dpr; c.height=H*dpr; c.setAttribute('aria-hidden','true');
    Object.assign(c.style,{position:'fixed',inset:'0',width:W+'px',height:H+'px',pointerEvents:'none',zIndex:'9999'});
    document.body.appendChild(c); const g=c.getContext('2d'); g.scale(dpr,dpr);
    const kleuren=['#1462ad','#6fa6da','#0b3a68','#f5b700','#e4572e','#2bb673','#ffffff'];
    const stukjes=Array.from({length:220},(_,i)=>{ const links=i%2===0, hoek=(links?-60:-120)*Math.PI/180+(Math.random()-0.5)*0.9, v=9+Math.random()*9;
      return {x:links?0:W,y:H*0.75,vx:Math.cos(hoek)*v,vy:Math.sin(hoek)*v,w:6+Math.random()*6,h:8+Math.random()*8,r:Math.random()*6.3,vr:(Math.random()-0.5)*0.35,k:kleuren[i%kleuren.length]}; });
    const start=performance.now(), duur=4200;
    const stap=nu=>{ const t=nu-start; g.clearRect(0,0,W,H);
      stukjes.forEach(p=>{ p.vy+=0.25; p.vx*=0.99; p.vy*=0.99; p.x+=p.vx; p.y+=p.vy; p.r+=p.vr;
        g.save(); g.globalAlpha=Math.max(0,1-Math.max(0,t-duur+1200)/1200); g.translate(p.x,p.y); g.rotate(p.r); g.fillStyle=p.k; g.fillRect(-p.w/2,-p.h/2,p.w,p.h*Math.abs(Math.cos(p.r*2))); g.restore(); });
      if(t<duur) requestAnimationFrame(stap); else c.remove(); };
    requestAnimationFrame(stap);
  }
'''
t = sub1("  kopieer(tekst,key){", CONFETTI + "  kopieer(tekst,key){", t)
