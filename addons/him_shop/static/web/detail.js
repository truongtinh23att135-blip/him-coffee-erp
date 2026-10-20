const SIZES = [["Size M", "Chuẩn · 350ml", 0], ["Size L", "Lớn · 500ml", 6000]];
const SUGAR = ["100%", "70%", "50%", "30%"];
const ICE = ["100% đá", "70% đá", "50% đá", "Không đá"];
const DT = ["Thêm Kem Muối Cheese", "Thạch Sương Sáo", "Trân Châu Đường Đen", "Pudding Đậu Hũ"];
const m = document.createElement("div");
m.id = "modal"; m.hidden = true;
document.body.appendChild(m);
let s;
const total = () => (P[s.i][1] + SIZES[s.size][2] + s.tops.length * 10000) * s.qty;
const opt = (g, arr, fmt) => arr.map((v, k) =>
  `<button class="o${s[g] === k ? " on" : ""}" data-g="${g}" data-v="${k}">${fmt(v)}</button>`).join("");

function draw() {
  const p = P[s.i], sc = (m.querySelector(".dr") || {}).scrollTop || 0;
  m.innerHTML = `<div class="dlg"><button class="x" data-x>✕</button>
    <div class="dl"><div class="ph">🥤<img src="img/T${String(s.i + 1).padStart(2, "0")}.jpeg" alt="" onerror="this.remove()"></div>${p[4] ? `<span class="badge">${p[4]}</span>` : ""}</div>
    <div class="dr"><h2>${p[0]}</h2><div class="pr">${money(p[1])}</div><p class="ds">${p[3]}</p>
      <h4>1. Chọn Kích Cỡ <small>Bắt buộc</small></h4>
      <div class="og">${opt("size", SIZES, (v) => `<b>${v[0]}</b><small>${v[1]}${v[2] ? " · +" + money(v[2]) : ""}</small>`)}</div>
      <h4>2. Độ Ngọt (Đường &amp; Sữa đặc)</h4><div class="og">${opt("sugar", SUGAR, (v) => v)}</div>
      <h4>3. Lượng Đá</h4><div class="og">${opt("ice", ICE, (v) => v)}</div>
      <h4>4. Topping Thủ Công Thêm (+10.000đ) <small>Tùy chọn</small></h4>
      <div class="og">${DT.map((t, k) => `<label class="tp"><input type="checkbox" data-t="${k}" ${s.tops.includes(k) ? "checked" : ""}>${t}<small>+10k</small></label>`).join("")}</div>
      <div class="ft"><div class="qty"><button data-q="-1">−</button><b>${s.qty}</b><button data-q="1">+</button></div>
        <button class="add2" data-add>Thêm vào giỏ · ${money(total())}</button></div>
    </div></div>`;
  m.querySelector(".dr").scrollTop = sc;
}

m.onclick = (e) => {
  const b = e.target.closest("button"), d = b && b.dataset;
  if (e.target === m || (d && d.x !== undefined)) { m.hidden = true; return; }
  if (!b) return;
  if (d.g) s[d.g] = +d.v;
  else if (d.q) s.qty = Math.max(1, s.qty + +d.q);
  else if (d.add !== undefined) {
    const key = [s.i, s.size, s.sugar, s.ice, s.tops.join(".")].join("|");
    const unit = P[s.i][1] + SIZES[s.size][2] + s.tops.length * 10000;
    cart[key] = cart[key] || {i: s.i, n: P[s.i][0], price: unit, size: SIZES[s.size][0], sugar: SUGAR[s.sugar], ice: ICE[s.ice], tops: s.tops.map((k) => DT[k]), qty: 0, note: ""};
    cart[key].qty += s.qty;
    localStorage.setItem("himcart", JSON.stringify(cart));
    document.getElementById("cnt").textContent = Object.values(cart).reduce((a, c) => a + c.qty, 0);
    m.hidden = true;
    return;
  } else return;
  draw();
};
m.onchange = (e) => {
  if (e.target.dataset.t === undefined) return;
  const k = +e.target.dataset.t;
  s.tops = e.target.checked ? [...s.tops, k] : s.tops.filter((x) => x !== k);
  draw();
};
document.addEventListener("click", (e) => {
  const c = e.target.closest(".card");
  if (!c) return;
  e.stopPropagation();
  s = {i: +c.querySelector(".add").dataset.i, size: 0, sugar: 0, ice: 0, tops: [], qty: 1};
  draw();
  m.hidden = false;
}, true);
document.addEventListener("keydown", (e) => { if (e.key === "Escape") m.hidden = true; });

document.getElementById("cnt").textContent = Object.values(cart).reduce((a, c) => a + c.qty, 0);
