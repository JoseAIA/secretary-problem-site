"use strict";
(() => {
  const nControl = document.getElementById("explorer-n");
  const rControl = document.getElementById("explorer-r");
  if (!nControl || !rControl) return;
  const $ = (id) => document.getElementById(id);
  const probability = (n, r) => {
    if (r === 0) return 1 / n;
    let harmonic = 0;
    for (let j = r; j < n; j += 1) harmonic += 1 / j;
    return (r / n) * harmonic;
  };
  const optimal = (n) => {
    let best = 0;
    for (let r = 1; r < n; r += 1) {
      if (probability(n, r) > probability(n, best) + 1e-12) best = r;
    }
    return best;
  };
  const svg = $("explorer-chart");
  const NS = "http://www.w3.org/2000/svg";
  function shape(tag, attrs, text) {
    const el = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, String(value));
    if (text !== undefined) el.textContent = text;
    svg.appendChild(el);
    return el;
  }
  function render() {
    const n = Number(nControl.value);
    rControl.max = String(n - 1);
    if (Number(rControl.value) >= n) rControl.value = String(n - 1);
    const r = Number(rControl.value);
    const best = optimal(n);
    const values = Array.from({ length: n }, (_, k) => probability(n, k));
    $("explorer-n-value").textContent = String(n);
    $("explorer-r-value").textContent = String(r);
    $("explorer-your-prob").textContent = (100 * values[r]).toFixed(2) + "%";
    $("explorer-best").textContent = "r = " + best + " (" + (100 * values[best]).toFixed(2) + "%)";
    $("explorer-difference").textContent = "Diferencia respecto al óptimo: " +
      (100 * (values[best] - values[r])).toFixed(2) + " puntos porcentuales.";
    svg.replaceChildren();
    const left = 44, right = 670, top = 14, bottom = 221;
    const x = k => left + (right - left) * k / (n - 1);
    const y = p => bottom - (bottom - top) * p / 0.5;
    for (const tick of [0, .1, .2, .3, .4, .5]) {
      shape("line", { x1:left, y1:y(tick), x2:right, y2:y(tick), stroke:"#d3d9e5", "stroke-width":1 });
      shape("text", { x:38, y:y(tick)+4, "text-anchor":"end", "font-size":12, fill:"#24324a" }, String(Math.round(tick*100)) + "%");
    }
    shape("polyline", {
      points:values.map((v,k)=>x(k).toFixed(2)+","+y(v).toFixed(2)).join(" "),
      fill:"none", stroke:"#4f86c6", "stroke-width":3, "stroke-linejoin":"round"
    });
    shape("line", {x1:x(r),y1:top,x2:x(r),y2:bottom,stroke:"#ef8354","stroke-dasharray":"5 4","stroke-width":2});
    shape("circle", {cx:x(best),cy:y(values[best]),r:6,fill:"#17805e"});
    shape("circle", {cx:x(r),cy:y(values[r]),r:5,fill:"#ef8354",stroke:"#fff","stroke-width":1.5});
    shape("text", {x:left,y:241,"font-size":12,fill:"#24324a"}, "0");
    shape("text", {x:right,y:241,"font-size":12,"text-anchor":"end",fill:"#24324a"}, String(n-1));
    shape("text", {x:(left+right)/2,y:258,"font-size":12,"text-anchor":"middle",fill:"#24324a"}, "Umbral de rechazo r");
  }
  nControl.addEventListener("input",render);
  rControl.addEventListener("input",render);
  $("explorer-optimize").addEventListener("click", () => {
    rControl.value = String(optimal(Number(nControl.value)));
    render();
  });
  render();
})();
