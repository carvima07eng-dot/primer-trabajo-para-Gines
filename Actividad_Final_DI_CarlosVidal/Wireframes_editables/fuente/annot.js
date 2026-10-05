// Dibuja recuadros discontinuos y números sobre los elementos con data-co="n"
// data-cp = posición del número: tl (arriba-izq, por defecto), tr (arriba-dcha)
window.addEventListener('load',()=>{
  document.querySelectorAll('[data-co]').forEach(el=>{
    const r=el.getBoundingClientRect(), pad=+(el.dataset.pad||6), sm=document.body.classList.contains('sm');
    if(!el.hasAttribute('data-nobox')){
      const b=document.createElement('div');b.className='box';
      Object.assign(b.style,{left:(r.left-pad)+'px',top:(r.top-pad)+'px',width:(r.width+2*pad)+'px',height:(r.height+2*pad)+'px'});
      document.body.appendChild(b);
    }
    const c=document.createElement('div');c.className='co'+(sm?' s':'');c.textContent=el.dataset.co;
    const s=sm?26:34, p=el.dataset.cp||'tl';
    let x=p.includes('r')?r.right+pad-s/2:r.left-pad-s/2, y=p.includes('b')?r.bottom+pad-s/2:r.top-pad-s/2;
    x=Math.max(2,Math.min(x,innerWidth-s-2)); y=Math.max(2,Math.min(y,innerHeight-s-2));
    Object.assign(c.style,{left:x+'px',top:y+'px'});document.body.appendChild(c);
  });
});
