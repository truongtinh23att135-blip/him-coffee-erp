const money = (n) => n.toLocaleString("vi-VN") + "đ";
const $ = (id) => document.getElementById(id);
const o = JSON.parse(localStorage.getItem("himlast") || "null");
if (!o) location.replace("index.html");
else {
  $("code").textContent = o.code;
  $("time").textContent = o.time;
  $("phone").textContent = o.customer.phone;
  $("eta").textContent = o.when === "Giao ngay" ? "15 - 20 phút (Hỏa tốc TP. Vinh)" : "Lúc " + o.when;
  $("name").textContent = o.customer.name;
  $("addr").textContent = o.customer.address;
  $("nbox").hidden = !o.note;
  $("note").textContent = o.note;
  $("pay").textContent = money(o.total);
  $("pill").textContent = o.count + " phần đồ uống";
  $("items").innerHTML = o.items.map((l) => `
    <div class="mi"><div class="ph"><img src="img/T${String(l.i + 1).padStart(2, "0")}.jpeg" alt="" onerror="this.remove()"></div>
    <div><b>${l.n}</b><small>SL: ${l.qty} · ${l.size} · ${l.sugar} Ngọt · ${l.ice}${l.tops.length ? " · " + l.tops.join(", ") : ""}</small>${l.note ? `<small>“${l.note}”</small>` : ""}</div>
    <b>${money(l.price * l.qty)}</b></div>`).join("");
  $("subl").textContent = `Tạm tính (${o.count} đồ uống)`;
  $("sub").textContent = money(o.sub);
  $("offrow").hidden = !o.off;
  $("off").textContent = "-" + money(o.off);
  $("tot").textContent = money(o.total);
  $("copy").onclick = () => { navigator.clipboard.writeText(o.code); $("copy").textContent = "Đã chép ✓"; };
  $("print").onclick = () => window.print();
}
