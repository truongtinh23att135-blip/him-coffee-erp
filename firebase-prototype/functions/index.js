const {setGlobalOptions} = require("firebase-functions");
const {onCall, HttpsError} = require("firebase-functions/https");
const {defineSecret} = require("firebase-functions/params");
const logger = require("firebase-functions/logger");

setGlobalOptions({maxInstances: 10});
const ODOO_API_KEY = defineSecret("ODOO_API_KEY");

async function odoo(model, method, body) {
  const res = await fetch(`${process.env.ODOO_URL}/json/2/${model}/${method}`, {
    method: "POST",
    headers: {
      "Authorization": `bearer ${ODOO_API_KEY.value()}`,
      "X-Odoo-Database": process.env.ODOO_DB,
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  if (!res.ok) {
    logger.error("Odoo error", {model, method, status: res.status, text});
    throw new HttpsError("internal", `Odoo báo lỗi (${res.status})`);
  }
  return JSON.parse(text);
}

const info = async (id) => {
  const [o] = await odoo("sale.order", "read", {ids: [id], fields: ["name", "amount_total"]});
  return {odooOrderId: id, odooName: o.name, amountTotal: o.amount_total};
};

exports.createOnlineOrder = onCall({secrets: [ODOO_API_KEY]}, async (request) => {
  const {webOrderId, customer, items, voucher, when, note} = request.data || {};
  if (!webOrderId || !customer || !customer.name || !customer.phone ||
      !customer.address || !Array.isArray(items) || !items.length) {
    throw new HttpsError("invalid-argument", "Thiếu thông tin đơn hàng");
  }
  for (const i of items) {
    if (!i.name || !Number.isInteger(i.qty) || i.qty < 1) {
      throw new HttpsError("invalid-argument", "Món hàng không hợp lệ");
    }
  }

  // 1. Chống tạo trùng đơn
  const existed = await odoo("sale.order", "search", {
    domain: [["client_order_ref", "=", webOrderId]], limit: 1,
  });
  if (existed.length) return {...(await info(existed[0])), duplicated: true};

  // 2. Tìm món trong Odoo theo tên
  const names = [...new Set(items.map((i) => i.name))];
  const found = await odoo("product.product", "search_read", {
    domain: [["name", "in", names], ["sale_ok", "=", true]],
    fields: ["name", "list_price"],
  });
  const byName = Object.fromEntries(found.map((p) => [p.name, p]));
  for (const n of names) {
    if (!byName[n]) throw new HttpsError("not-found", `Món "${n}" chưa có trong Odoo`);
  }

  // 3. Tìm hoặc tạo khách theo số điện thoại
  let [partnerId] = await odoo("res.partner", "search", {
    domain: [["phone", "=", customer.phone]], limit: 1,
  });
  if (!partnerId) {
    [partnerId] = await odoo("res.partner", "create", {
      vals_list: [{name: customer.name, phone: customer.phone, street: customer.address}],
    });
  }

  // 4. Team Online
  const [teamId] = await odoo("crm.team", "search", {
    domain: [["name", "=", "Online"]], limit: 1,
  });

  // 5. Tạo đơn: giá tính tại server, voucher HIMNEW = giảm 15%
  const disc = voucher === "HIMNEW" ? 15 : 0;
  const lines = items.map((i) => {
    const p = byName[i.name];
    const tops = Array.isArray(i.tops) ? i.tops : [];
    const extra = (i.size === "Size L" ? 6000 : 0) + tops.length * 10000;
    const label = `${i.name} | ${i.size || ""}, ${i.sugar || ""} ngọt, ${i.ice || ""}` +
      (tops.length ? `, + ${tops.join(", ")}` : "") + (i.note ? ` | Ghi chú: ${i.note}` : "");
    return [0, 0, {
      product_id: p.id, name: label, product_uom_qty: i.qty,
      price_unit: p.list_price + extra, discount: disc,
    }];
  });
  const [orderId] = await odoo("sale.order", "create", {
    vals_list: [{
      partner_id: partnerId, partner_shipping_id: partnerId,
      team_id: teamId || false, client_order_ref: webOrderId, origin: "WEB",
      note: `Giao tới: ${customer.address}. Giờ nhận: ${when || "Giao ngay"}. ` +
        `Ghi chú: ${note || "không"}. Thanh toán khi nhận hàng (COD)`,
      order_line: lines,
    }],
  });
  await odoo("sale.order", "action_confirm", {ids: [orderId]});
  logger.info("Đã tạo đơn", {webOrderId, orderId});
  return info(orderId);
});

exports.trackOrder = onCall({secrets: [ODOO_API_KEY]}, async (request) => {
  const norm = (s) => String(s || "").replace(/\D/g, "").replace(/^84/, "0");
  const d = request.data || {};
  const code = String(d.code || "").replace("#", "").trim().toUpperCase();
  const phone = norm(d.phone);
  if (!code || !phone) throw new HttpsError("invalid-argument", "Vui lòng nhập mã đơn và số điện thoại");
  const miss = new HttpsError("not-found", "Không tìm thấy đơn khớp mã và số điện thoại");
  const [o] = await odoo("sale.order", "search_read", {
    domain: [["name", "=", code]], limit: 1,
    fields: ["name", "state", "amount_total", "note", "partner_id", "order_line", "picking_ids", "invoice_ids"],
  });
  if (!o) throw miss;
  const [pt] = await odoo("res.partner", "read", {ids: [o.partner_id[0]], fields: ["phone"]});
  if (norm(pt.phone) !== phone) throw miss;
  const rd = (model, ids, fields) => ids.length ? odoo(model, "read", {ids, fields}) : [];
  const pk = await rd("stock.picking", o.picking_ids, ["state"]);
  const inv = await rd("account.move", o.invoice_ids, ["state", "payment_state"]);
  const ln = await rd("sale.order.line", o.order_line, ["name", "product_uom_qty", "price_unit", "price_subtotal"]);
  const delivered = pk.length > 0 && pk.every((p) => p.state === "done");
  const paid = inv.some((i) => i.state === "posted" && ["paid", "in_payment"].includes(i.payment_state));
  const sub = ln.reduce((a, l) => a + l.price_unit * l.product_uom_qty, 0);
  const net = ln.reduce((a, l) => a + l.price_subtotal, 0);
  return {
    code: o.name, cancelled: o.state === "cancel", stage: paid ? 4 : delivered ? 3 : 1,
    items: ln.map((l) => ({name: l.name, qty: l.product_uom_qty, total: l.price_subtotal})),
    sub, off: Math.round(sub - net), total: o.amount_total, note: o.note || "",
  };
});
