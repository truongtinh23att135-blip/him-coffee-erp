const money = (n) => n.toLocaleString("vi-VN") + "đ";
const $ = (id) => document.getElementById(id);
const cart = JSON.parse(localStorage.getItem("himcart") || "{}");
const keys = Object.keys(cart);
if (!keys.length) location.replace("cart.html");
const AREAS = ["P. Hưng Bình (Quán Gốc)", "P. Lê Mao", "P. Trường Thi", "P. Hà Huy Tập", "P. Quán Bàu", "P. Hưng Dũng"];
let area = 0, when = "now";
const count = keys.reduce((a, k) => a + cart[k].qty, 0);
const sub = keys.reduce((a, k) => a + cart[k].price * cart[k].qty, 0);
const off = localStorage.getItem("himpromo") === "HIMNEW" ? Math.round(sub * 0.15) : 0;
const total = sub - off;

$("cnt").textContent = count;
$("pill").textContent = count + " món";
$("items").innerHTML = keys.map((k) => { const l = cart[k]; return `
  <div class="mi"><div class="ph"><img src="img/T${String(l.i + 1).padStart(2, "0")}.jpeg" alt="" onerror="this.remove()"></div>
  <div><b>${l.n}</b><small>${l.size}, ${l.sugar} Ngọt, ${l.ice}${l.tops.length ? ", + " + l.tops.join(", ") : ""}</small></div>
  <div style="text-align:right"><b>${money(l.price * l.qty)}</b><small>x${l.qty}</small></div></div>`; }).join("");
$("subl").textContent = `Tạm tính (${count} ly)`;
$("sub").textContent = money(sub);
$("offrow").hidden = !off;
$("off").textContent = "-" + money(off);
$("tot").textContent = money(total);
$("go").textContent = `XÁC NHẬN ĐẶT HÀNG • ${money(total)} →`;

function chips() {
  $("areas").innerHTML = AREAS.map((a, i) => `<button type="button" data-a="${i}" class="${i === area ? "on" : ""}">${a}</button>`).join("");
  $("when").innerHTML = [["now", "Giao ngay (15 - 20 phút)"], ["later", "Hẹn giờ nhận"]]
    .map(([v, t]) => `<button type="button" data-w="${v}" class="${v === when ? "on" : ""}" style="border-radius:12px;padding:12px">${t}</button>`).join("");
}
$("areas").onclick = (e) => { if (e.target.dataset.a) { area = +e.target.dataset.a; chips(); } };
$("when").onclick = (e) => { if (e.target.dataset.w) { when = e.target.dataset.w; $("later").hidden = when !== "later"; chips(); } };

const saved = JSON.parse(localStorage.getItem("himcust") || "{}");
$("name").value = saved.name || "";
$("phone").value = saved.phone || "";
$("addr").value = saved.addr || "";
$("note").value = localStorage.getItem("himnote") || "";
chips();

$("go").onclick = async () => {
  const name = $("name").value.trim(), phone = $("phone").value.replace(/[\s.]/g, "");
  const addr = $("addr").value.trim(), errs = [];
  const bad = (id, on) => $(id).classList.toggle("bad", on);
  bad("name", name.length < 2); if (name.length < 2) errs.push("Vui lòng nhập họ và tên.");
  const okP = /^(0|\+84)\d{9}$/.test(phone);
  bad("phone", !okP); if (!okP) errs.push("Số điện thoại chưa đúng (ví dụ 0912345678).");
  bad("addr", addr.length < 5); if (addr.length < 5) errs.push("Vui lòng nhập địa chỉ chi tiết.");
  if (when === "later" && !$("time").value) errs.push("Vui lòng chọn giờ nhận hàng.");
  $("err").hidden = !errs.length;
  $("err").innerHTML = "<b>Yêu cầu bổ sung thông tin</b><br>" + errs.join("<br>");
  if (errs.length) { $("err").scrollIntoView({behavior: "smooth", block: "center"}); return; }
  localStorage.setItem("himcust", JSON.stringify({name, phone, addr}));
  const order = {
    webOrderId: "WEB-" + Date.now(),
    customer: {name, phone, address: `${addr}, ${AREAS[area]}, TP. Vinh`},
    when: when === "later" ? $("time").value : "Giao ngay",
    note: $("note").value.trim(), voucher: off ? "HIMNEW" : "", total,
    items: keys.map((k) => ({...cart[k]})),
  };
  const FN = "http://127.0.0.1:5001/him-coffee-web/us-central1/createOnlineOrder";
  $("go").disabled = true; $("go").textContent = "Đang gửi đơn...";
  try {
    const r = await fetch(FN, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({data: {
      webOrderId: order.webOrderId, customer: order.customer, when: order.when, note: order.note, voucher: order.voucher,
      items: order.items.map((l) => ({name: l.n, qty: l.qty, size: l.size, sugar: l.sugar, ice: l.ice, tops: l.tops, note: l.note})),
    }})});
    const j = await r.json();
    if (!r.ok) throw new Error((j.error && j.error.message) || "Lỗi máy chủ");
    order.code = "#" + j.result.odooName;
  } catch (e) {
    $("go").disabled = false; $("go").textContent = `XÁC NHẬN ĐẶT HÀNG • ${money(total)} →`;
    $("err").hidden = false; $("err").innerHTML = "<b>Chưa gửi được đơn</b><br>" + e.message;
    return;
  }
  Object.assign(order, {sub, off, count, time: new Date().toLocaleString("vi-VN")});
  localStorage.setItem("himlast", JSON.stringify(order));
  ["himcart", "himpromo", "himnote"].forEach((k) => localStorage.removeItem(k));
  location.href = "success.html";
};
