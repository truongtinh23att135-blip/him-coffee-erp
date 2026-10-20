const CATS = {cafe: "1. Cà Phê", may: "2. Cà Phê Máy", milk: "3. Milk Tea HIM", yogurt: "4. Yogurt Ice", khac: "5. Khác"};
// Dữ liệu tạm để xem giao diện, sau này lấy từ Odoo: [tên, giá, danh mục, mô tả ngắn, nhãn]
const P = [
  ["Cà Phê Muối", 42000, "cafe", "Đá viên + Kem béo mặn", "BEST SELLER"],
  ["Bạc Xỉu", 39000, "cafe", "Vị ngọt béo nhẹ nhàng", ""],
  ["Nâu Lắc / Đen Lắc", 35000, "cafe", "Lắc bọt sâu mịn, mát lạnh", ""],
  ["Cà Phê Kem Caramel", 45000, "cafe", "Caramel ngậy thơm", ""],
  ["Dừa Phê Sương Sáo", 49000, "cafe", "Cốt dừa béo, sương sáo mát", ""],
  ["Cold Brew", 49000, "cafe", "Ủ lạnh 18 giờ", "Ủ LẠNH 18H"],
  ["Cold Chanh Vàng / Cold Mơ", 49000, "cafe", "Chua thanh, tươi mát", ""],
  ["Espresso", 29000, "may", "Chiết xuất máy chuẩn Ý", ""],
  ["Gừng Sữa Kỳ Sơn", 49000, "milk", "Đặc sản Nghệ An", "ĐẶC SẢN NGHỆ AN"],
  ["Trà Sữa Trân Châu Đường Đen", 35000, "milk", "Trân châu dẻo ngọt", ""],
  ["Trà Olong Sữa TCĐĐ", 49000, "milk", "Vị olong đậm đà", ""],
  ["Trà Nhãn Hoa Nhài", 49000, "khac", "Hương hoa nhài thanh khiết", ""],
  ["Sữa Chua Truyền Thống", 45000, "yogurt", "Lên men tự nhiên", ""],
  ["Sữa Chua Lắc", 49000, "yogurt", "Lắc tươi mát lạnh", ""],
  ["Sữa Chua Dừa", 55000, "yogurt", "Cốt dừa béo ngậy", ""],
  ["Chocolatte", 45000, "may", "Cacao đậm, sữa béo", ""],
  ["Matcha Latte", 59000, "khac", "Matcha Uji Nhật Bản", ""],
  ["Matcha Mây Xanh", 59000, "khac", "Kem mây bồng bềnh", ""],
  ["Dừa Sữa Kem Matcha", 59000, "khac", "Cốt dừa, kem matcha", ""],
  ["Trà Vải Hoa Hồng", 59000, "khac", "Hoa hồng & vải thiều", ""],
  ["Trà Măng Cầu", 59000, "khac", "Chua ngọt đào hạt", ""],
  ["Trà Mơ Him", 45000, "khac", "Mơ ngâm truyền thống", ""],
  ["Trà Đào Sả", 59000, "khac", "Giòn tan sảng khoái", ""],
  ["Bơ Già Dừa Non", 65000, "khac", "Bơ sáp, dừa non béo", "SIGNATURE"],
];
const TOPS = [["Trân Châu Đen","🟤"],["Trân Châu Trắng","⚪"],["Thạch Sương Sáo","⬛"],["Đậu Hũ","🟡"],["Thạch Nhãn","🟠"],["Thạch Đào","🍑"],["Kem Cheese","🧀"]];
const money = (n) => n.toLocaleString("vi-VN") + "đ";
const plain = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").toLowerCase();
const cart = JSON.parse(localStorage.getItem("himcart") || "{}");
let cat = "all", q = "";

function render() {
  let list = P.map((p, i) => ({p, i})).filter(({p}) =>
    (cat === "all" || p[2] === cat) && plain(p[0]).includes(plain(q)));
  const s = document.getElementById("sort").value;
  if (s === "1") list.sort((a, b) => a.p[1] - b.p[1]);
  if (s === "2") list.sort((a, b) => b.p[1] - a.p[1]);
  document.getElementById("grid").innerHTML = list.map(({p, i}) => `
    <article class="card">
      <div class="ph" style="background:linear-gradient(135deg,hsl(${20 + i * 9} 45% 75%),hsl(${20 + i * 9} 40% 45%))">${p[2] === "yogurt" ? "🥛" : p[2] === "may" ? "☕" : "🥤"}<img src="img/T${String(i + 1).padStart(2, "0")}.jpeg" alt="${p[0]}" loading="lazy" onerror="this.remove()"></div>
      ${p[4] ? `<span class="badge">${p[4]}</span>` : ""}
      <h3>${p[0]}</h3><p>${p[3]}</p>
      <div class="row"><b>${money(p[1])}</b><button class="add" data-i="${i}">+ Thêm</button></div>
    </article>`).join("") || "<p>Không tìm thấy món phù hợp.</p>";
}

function chips() {
  const all = {all: `Tất cả (${P.length})`, ...CATS};
  document.getElementById("chips").innerHTML = Object.entries(all).map(([k, v]) =>
    `<button data-c="${k}" class="${k === cat ? "on" : ""}">${v}</button>`).join("");
}

document.getElementById("chips").onclick = (e) => {
  if (e.target.dataset.c) { cat = e.target.dataset.c; chips(); render(); }
};
document.getElementById("grid").onclick = (e) => {
  const i = e.target.dataset.i;
  if (i === undefined) return;
  cart[i] = (cart[i] || 0) + 1;
  document.getElementById("cnt").textContent = Object.values(cart).reduce((a, b) => a + b, 0);
};
document.querySelectorAll(".q").forEach((el) => el.oninput = () => {
  q = el.value;
  document.querySelectorAll(".q").forEach((o) => o.value = q);
  render();
});
document.getElementById("sort").onchange = render;
document.getElementById("tops").innerHTML = TOPS.map(([n, e]) =>
  `<div><span>${e}</span>${n}<small>+10.000đ</small></div>`).join("");
chips();
render();

// Lay gia mon tu Odoo (neu doi gia trong Odoo thi web doi theo)
fetch("/him/menu.json").then((r) => r.json()).then((j) => {
  (j.result || []).forEach((m) => { const p = P.find((x) => x[0] === m.name); if (p) p[1] = Math.round(m.price); });
  render();
}).catch(() => {});
