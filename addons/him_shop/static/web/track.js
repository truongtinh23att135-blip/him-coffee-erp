const money = (n) => Math.round(n).toLocaleString("vi-VN") + "đ";
const $ = (id) => document.getElementById(id);
const FN = "/him/track";
const STEPS = [["Đã nhận đơn & xác nhận qua điện thoại", "Quán đã nhận đơn của bạn"], ["Barista đang pha chế", "Đồ uống đang được chuẩn bị"],
  ["Shipper HIM giao tận nơi", "Đơn đang trên đường giao"], ["Giao hàng thành công & Thanh toán COD", "Hoàn tất, cảm ơn bạn"]];

async function look(code, phone) {
  $("msg").textContent = "Đang tra cứu...";
  try {
    const r = await fetch(FN, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({data: {code, phone}})});
    const j = await r.json();
    if (!r.ok) throw new Error((j.error && j.error.message) || "Lỗi máy chủ");
    show(j.result);
  } catch (e) { $("msg").textContent = e.message; }
}

function show(o) {
  $("form").hidden = true; $("res").hidden = false;
  $("title").textContent = "Đơn hàng #" + o.code;
  $("pill").textContent = o.cancelled ? "Đơn đã hủy" : o.stage >= 4 ? "Đã giao & thanh toán" : o.stage >= 3 ? "Đã giao hàng" : "Đang chuẩn bị";
  $("tl").innerHTML = STEPS.map((s, i) => `<li class="${o.cancelled ? "" : i < o.stage ? "done" : i === o.stage ? "now" : ""}"><i>${i < o.stage && !o.cancelled ? "✓" : ""}</i><div><b>${s[0]}</b><small>${s[1]}</small></div></li>`).join("");
  $("items").innerHTML = o.items.map((l) => `<div class="mi" style="grid-template-columns:1fr auto"><div><b>${l.name}</b><small>SL: ${l.qty}</small></div><b>${money(l.total)}</b></div>`).join("");
  $("note").textContent = o.note;
  $("sub").textContent = money(o.sub);
  $("offrow").hidden = !o.off;
  $("off").textContent = "-" + money(o.off);
  $("tot").textContent = money(o.total);
}

$("go").onclick = () => look($("code").value, $("phone").value);
const q = new URLSearchParams(location.search), last = JSON.parse(localStorage.getItem("himlast") || "null");
$("code").value = q.get("code") || (last ? last.code.replace("#", "") : "");
$("phone").value = q.get("phone") || (last ? last.customer.phone : "");
if (q.get("code") && q.get("phone")) look($("code").value, $("phone").value);
