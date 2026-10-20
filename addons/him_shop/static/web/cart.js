const money = (n) => n.toLocaleString("vi-VN") + "đ";
const $ = (id) => document.getElementById(id);
const cart = JSON.parse(localStorage.getItem("himcart") || "{}");
let promo = localStorage.getItem("himpromo") || "";
const save = () => { localStorage.setItem("himcart", JSON.stringify(cart)); render(); };

function render() {
  const keys = Object.keys(cart);
  const count = keys.reduce((a, k) => a + cart[k].qty, 0);
  $("cnt").textContent = count;
  $("pill").textContent = keys.length + " món đang chọn";
  $("empty").hidden = keys.length > 0;
  $("full").hidden = keys.length === 0;
  $("items").innerHTML = keys.map((k) => { const l = cart[k]; return `
    <article class="ci"><div class="ph"><img src="img/T${String(l.i + 1).padStart(2, "0")}.jpeg" alt="" onerror="this.remove()"></div>
      <div><h3>${l.n}</h3>
        <div class="opts"><span>${l.size}</span><span>${l.sugar} Ngọt</span><span>${l.ice}</span>${l.tops.map((t) => `<span class="tp2">+ ${t}</span>`).join("")}</div>
        ${l.note ? `<p class="nt">“${l.note}”</p>` : ""}
        <button class="lnk" data-n="${k}">✎ Sửa ghi chú</button></div>
      <div class="cr"><button class="del" data-d="${k}">🗑</button><b>${money(l.price * l.qty)}</b>
        <div class="qty"><button data-k="${k}" data-q="-1">−</button><b>${l.qty}</b><button data-k="${k}" data-q="1">+</button></div></div>
    </article>`; }).join("");
  const sub = keys.reduce((a, k) => a + cart[k].price * cart[k].qty, 0);
  const off = promo === "HIMNEW" ? Math.round(sub * 0.15) : 0;
  $("subl").textContent = `Tạm tính (${count} đồ uống)`;
  $("sub").textContent = money(sub);
  $("offrow").hidden = !off;
  $("off").textContent = "-" + money(off);
  $("applied").hidden = !off;
  $("tot").textContent = money(sub - off);
  $("go").textContent = `ĐẶT HÀNG NGAY (${money(sub - off)}) →`;
}

$("items").onclick = (e) => {
  const d = e.target.dataset;
  if (d.d) delete cart[d.d];
  else if (d.k) cart[d.k].qty = Math.max(1, cart[d.k].qty + +d.q);
  else if (d.n) {
    const v = prompt("Ghi chú cho món này:", cart[d.n].note || "");
    if (v === null) return;
    cart[d.n].note = v.trim();
  } else return;
  save();
};
$("apply").onclick = () => {
  const c = $("code").value.trim().toUpperCase();
  if (c !== "HIMNEW") { alert("Mã không hợp lệ"); return; }
  promo = c; localStorage.setItem("himpromo", c); render();
};
$("unapply").onclick = () => { promo = ""; localStorage.removeItem("himpromo"); $("code").value = ""; render(); };
$("note").value = localStorage.getItem("himnote") || "";
$("note").oninput = () => localStorage.setItem("himnote", $("note").value);
$("code").value = promo;
$("go").onclick = () => { location.href = "checkout.html"; };
render();
