"use strict";
(() => {
  const sliders = Array.from({length:4},(_,i)=>document.getElementById("odds-p-"+(i+1)));
  if (sliders.some(el=>!el)) return;
  const $ = id=>document.getElementById(id);
  const success = (p, s) => {
    let total = 0;
    for (let k=s-1;k<p.length;k++) {
      let term = p[k];
      for (let j=s-1;j<k;j++) term *= (1-p[j]);
      for (let j=k+1;j<p.length;j++) term *= (1-p[j]);
      total += term;
    }
    return total;
  };
  const threshold = p => {
    let tailOdds = 0, s = 1;
    for (let k=p.length-1;k>=0;k--) {
      tailOdds += p[k]/(1-p[k]);
      if (tailOdds>=1) {s=k+1;break;}
    }
    return s;
  };
  function render() {
    const p=sliders.map(el=>Number(el.value));
    p.forEach((v,i)=>$("odds-value-"+(i+1)).textContent=v.toFixed(2));
    const s=threshold(p);
    const scores=Array.from({length:p.length},(_,i)=>success(p,i+1));
    $("odds-threshold").textContent="s = "+s;
    $("odds-probability").textContent=(100*scores[s-1]).toFixed(2)+"%";
    const best=Math.max(...scores);
    $("odds-explanation").textContent="Comenzar en el ensayo "+s+
      " y aceptar el primer éxito. Las probabilidades de comenzar en los ensayos 1–4 son "+
      scores.map(x=>(100*x).toFixed(2)+"%").join(", ")+
      ". Máximo: "+(100*best).toFixed(2)+"%.";
  }
  sliders.forEach(el=>el.addEventListener("input",render));
  render();
})();
