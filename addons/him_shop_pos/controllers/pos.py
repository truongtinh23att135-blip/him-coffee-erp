import json

from odoo import http
from odoo.http import request


def reply(data, status=200):
    return request.make_json_response(data, status=status)


class HimPosBar(http.Controller):

    @http.route("/him/bar/pos_send", type="http", auth="user", methods=["POST"], csrf=False)
    def pos_send(self, **kw):
        try:
            d = json.loads(request.httprequest.get_data(as_text=True) or "{}").get("data") or {}
            key, raw = str(d["key"])[:80], d.get("lines") or []
        except (ValueError, KeyError, TypeError, AttributeError):
            return reply({"error": {"message": "Du lieu khong hop le"}}, 400)
        Product = request.env["product.product"].sudo()
        lines = []
        for r in raw[:100]:
            try:
                qty, name = float(r["qty"]), str(r["name"])[:200]
            except (KeyError, TypeError, ValueError):
                continue
            if qty <= 0:
                continue
            pid = r.get("product_id")
            product = Product.browse(pid).exists() if isinstance(pid, int) else Product
            lines.append({"name": name, "qty": qty, "opts": str(r.get("note") or "")[:200], "product": product})
        if not lines:
            return reply({"result": {"sent": 0}})
        sent = request.env["him.bar.ticket"].sudo()._send_delta(
            key, str(d.get("title") or "POS")[:60], str(d.get("customer") or "Khách lẻ")[:120],
            str(d.get("note") or "")[:300], lines)
        return reply({"result": {"sent": sent}})
