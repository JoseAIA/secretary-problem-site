"use strict";
(() => {
  const nInput=document.getElementById("full-n");
  const xInput=document.getElementById("full-x");
  if (!nInput || !xInput) return;
  const $=id=>document.getElementById(id);
  function continuation(n,x) {
    if (n===2) return 1-x;
    // n=3: rejection after first value x, optimal use of the last two draws.
    if (x <= .5) return .75 - .5*x*x;
    return .5+x-1.5*x*x;
  }
  function render() {
    const n=Number(nInput.value), x=Number(xInput.value);
    const threshold=n===2?.5:(1+Math.sqrt(6))/5;
    const stop=x**(n-1), go=continuation(n,x);
    $("full-n-value").textContent=String(n);
    $("full-x-value").textContent=x.toFixed(2);
    $("full-stop").textContent=(100*stop).toFixed(2)+"%";
    $("full-continue").textContent=(100*go).toFixed(2)+"%";
    $("full-cutoff").textContent=threshold.toFixed(5);
    $("full-decision").textContent=stop>=go?"Select the first observation":"Reject and continue";
    $("full-reason").textContent=
      "This compares the first observation x with the best strategy for the remaining "+
      (n-1)+" independent Uniform(0,1) observations. The exact first-stage cutoff is "+
      (n===2?"1/2":"(1+√6)/5")+".";
  }
  nInput.addEventListener("input",render);
  xInput.addEventListener("input",render);
  render();
})();
