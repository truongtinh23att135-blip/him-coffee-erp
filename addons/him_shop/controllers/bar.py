import json

from odoo import fields, http
from odoo.http import request


def ticket_dict(t):
    return {
        "id": t.id, "name": t.name, "channel": t.channel or "", "customer": t.customer or "",
        "note": t.note or "", "state": t.state, "lines": json.loads(t.body or "[]"),
        "printer": t.printer_id.name, "copies": t.printer_id.copies or 1,
        "auto": bool(t.printer_id.auto_print),
        "time": fields.Datetime.context_timestamp(t, t.create_date).strftime("%H:%M"),
    }


class HimBar(http.Controller):

    @http.route("/him/bar", type="http", auth="user")
    def page(self, **kw):
        return request.redirect("/him_shop/static/bar/bar.html")

    @http.route("/him/bar/tickets", type="http", auth="user", methods=["GET"])
    def tickets(self, **kw):
        ts = request.env["him.bar.ticket"].search([("state", "!=", "done")], order="id asc", limit=60)
        return request.make_json_response({"result": [ticket_dict(t) for t in ts]})

    @http.route("/him/bar/mark", type="http", auth="user", methods=["POST"], csrf=False)
    def mark(self, **kw):
        try:
            d = json.loads(request.httprequest.get_data(as_text=True) or "{}").get("data") or {}
            tid, state = int(d["id"]), d["state"]
        except (ValueError, KeyError, TypeError, AttributeError):
            return request.make_json_response({"error": {"message": "Du lieu khong hop le"}}, status=400)
        if state not in ("printed", "done"):
            return request.make_json_response({"error": {"message": "Trang thai khong hop le"}}, status=400)
        t = request.env["him.bar.ticket"].browse(tid).exists()
        if t:
            vals = {"state": state}
            if state == "printed":
                vals["printed_at"] = fields.Datetime.now()
            t.write(vals)
        return request.make_json_response({"result": True})
