"use strict";
(() => {
  const nInput = document.getElementById("postdoc-n");
  const kInput = document.getElementById("postdoc-k");
  const rankInput = document.getElementById("postdoc-rank");
  if (!nInput || !kInput || !rankInput) return;
  const $ = id => document.getElementById(id);
  const fmt = p => (100*p).toFixed(3) + "%";
  function reward(n,k,a) {
    if (a === 1) return (k*(n-k))/(n*(n-1));
    if (a === 2) return (k*(k-1))/(n*(n-1));
    return 0;
  }
  function solve(n) {
    const v = Array(n+2).fill(0);
    for (let k=n;k>=1;k--) {
      const continuation = v[k+1];
      let total = 0;
      for (let a=1;a<=k;a++) total += Math.max(reward(n,k,a),continuation);
      v[k]=total/k;
    }
    return v;
  }
  function render() {
    const n = Number(nInput.value);
    kInput.max=String(n);
    if (Number(kInput.value)>n) kInput.value=String(n);
    const k=Number(kInput.value);
    rankInput.max=String(k);
    if (Number(rankInput.value)>k) rankInput.value=String(k);
    const a=Number(rankInput.value);
    const values=solve(n);
    const stop=reward(n,k,a), go=values[k+1];
    const accept=(stop>=go && stop>0);
    $("postdoc-n-value").textContent=String(n);
    $("postdoc-k-value").textContent=String(k);
    $("postdoc-rank-value").textContent=String(a);
    $("postdoc-stop").textContent=fmt(stop);
    $("postdoc-continue").textContent=fmt(go);
    $("postdoc-initial").textContent=fmt(values[1]);
    $("postdoc-decision").textContent=accept?"Select this candidate":go>0?"Continue":"No winning selection available";
    $("postdoc-reason").textContent="After observing relative rank "+a+" at position "+k+
       ", selecting now wins with probability "+fmt(stop)+
       "; continuing optimally wins with probability "+fmt(go)+
       ". At ties, selection is shown when its winning probability is positive.";
  }
  [nInput,kInput,rankInput].forEach(el=>el.addEventListener("input",render));
  render();
})();
