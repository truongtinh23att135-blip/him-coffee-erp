import json
import re

from odoo import http
from odoo.http import request
from odoo.tools import html2plaintext

MENU_ROOT = "Thực đơn HIM"
SIZE_L_EXTRA = 6000
TOPPING_PRICE = 10000
PROMO = {"HIMNEW": 15.0}


def norm_phone(s):
    s = re.sub(r"\D", "", str(s or ""))
    return "0" + s[2:] if s.startswith("84") else s


def line_extra(item):
    tops = item.get("tops") if isinstance(item.get("tops"), list) else []
    return (SIZE_L_EXTRA if item.get("size") == "Size L" else 0) + TOPPING_PRICE * len(tops)


def line_label(item):
    tops = item.get("tops") if isinstance(item.get("tops"), list) else []
    label = "%s | %s, %s ngọt, %s" % (
        item["name"], item.get("size", ""), item.get("sugar", ""), item.get("ice", ""))
    if tops:
        label += ", + " + ", ".join(str(t)[:60] for t in tops)
    if item.get("note"):
        label += " | Ghi chú: " + str(item["note"])[:200]
    return label


def ok(result):
    return request.make_json_response({"result": result})


def fail(msg, status=400):
    return request.make_json_response({"error": {"message": msg}}, status=status)


def payload():
    try:
        data = json.loads(request.httprequest.get_data(as_text=True) or "{}")
    except ValueError:
        return {}
    d = data.get("data") if isinstance(data, dict) else None
    return d if isinstance(d, dict) else {}


def order_info(o):
    return {"odooOrderId": o.id, "odooName": o.name, "amountTotal": o.amount_total}


class HimShop(http.Controller):

    @http.route("/him", type="http", auth="public")
    def home(self, **kw):
        return request.redirect("/him_shop/static/web/index.html")

    @http.route("/him/menu.json", type="http", auth="public", methods=["GET"])
    def menu(self, **kw):
        rows = request.env["product.product"].sudo().search_read(
            [("sale_ok", "=", True), ("categ_id.parent_id.name", "=", MENU_ROOT)],
            ["name", "list_price"])
        return ok([{"id": r["id"], "name": r["name"], "price": r["list_price"]} for r in rows])

    @http.route("/him/order", type="http", auth="public", methods=["POST"], csrf=False)
    def order(self, **kw):
        d, env = payload(), request.env(su=True)
        cust = d.get("customer") if isinstance(d.get("customer"), dict) else {}
        ref = str(d.get("webOrderId") or "")[:40]
        name = str(cust.get("name") or "").strip()[:100]
        phone = norm_phone(cust.get("phone"))[:15]
        addr = str(cust.get("address") or "").strip()[:250]
        items = d.get("items")
        if not (ref and name and phone and addr and isinstance(items, list) and 0 < len(items) <= 30):
            return fail("Thiếu thông tin đơn hàng")
        clean = []
        for i in items:
            try:
                q, nm = int(i["qty"]), str(i["name"])
            except (TypeError, KeyError, ValueError):
                return fail("Món hàng không hợp lệ")
            if not 1 <= q <= 50:
                return fail("Số lượng không hợp lệ")
            clean.append({**i, "qty": q, "name": nm})

        Order = env["sale.order"]
        dup = Order.search([("client_order_ref", "=", ref)], limit=1)
        if dup:
            return ok(dict(order_info(dup), duplicated=True))
        found = {p.name: p for p in env["product.product"].search(
            [("name", "in", list({i["name"] for i in clean})), ("sale_ok", "=", True)])}
        for i in clean:
            if i["name"] not in found:
                return fail('Món "%s" chưa có trong hệ thống' % i["name"])
        disc = PROMO.get(str(d.get("voucher") or "").upper(), 0.0)
        partner = env["res.partner"].search([("phone", "=", phone)], limit=1) or \
            env["res.partner"].create({"name": name, "phone": phone, "street": addr})
        team = env["crm.team"].search([("name", "=", "Online")], limit=1)
        order = Order.create({
            "partner_id": partner.id, "partner_shipping_id": partner.id,
            "team_id": team.id or False, "client_order_ref": ref, "origin": "WEB",
            "note": "Giao tới: %s. Giờ nhận: %s. Ghi chú: %s. Thanh toán khi nhận hàng (COD)" % (
                addr, str(d.get("when") or "Giao ngay")[:40], str(d.get("note") or "không")[:300]),
            "order_line": [(0, 0, {
                "product_id": found[i["name"]].id, "name": line_label(i),
                "product_uom_qty": i["qty"],
                "price_unit": found[i["name"]].list_price + line_extra(i),
                "discount": disc}) for i in clean],
        })
        order.action_confirm()
        return ok(order_info(order))

    @http.route("/him/track", type="http", auth="public", methods=["POST"], csrf=False)
    def track(self, **kw):
        d = payload()
        code = str(d.get("code") or "").replace("#", "").strip().upper()
        phone = norm_phone(d.get("phone"))
        if not code or not phone:
            return fail("Vui lòng nhập mã đơn và số điện thoại")
        o = request.env["sale.order"].sudo().search([("name", "=", code)], limit=1)
        if not o or norm_phone(o.partner_id.phone) != phone:
            return fail("Không tìm thấy đơn khớp mã và số điện thoại", 404)
        delivered = bool(o.picking_ids) and all(p.state == "done" for p in o.picking_ids)
        paid = any(m.state == "posted" and m.payment_state in ("paid", "in_payment")
                   for m in o.invoice_ids)
        lines = o.order_line
        sub = sum(l.price_unit * l.product_uom_qty for l in lines)
        net = sum(l.price_total for l in lines)
        return ok({
            "code": o.name, "cancelled": o.state == "cancel",
            "stage": 4 if paid else 3 if delivered else 1,
            "items": [{"name": l.name, "qty": l.product_uom_qty, "total": l.price_total} for l in lines],
            "sub": sub, "off": round(sub - net), "total": o.amount_total,
            "note": html2plaintext(o.note or "").strip(),
        })
