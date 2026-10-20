import json
import logging

from odoo import api, fields, models
from odoo.tools import html2plaintext

from . import delta

_logger = logging.getLogger(__name__)


class HimBarTicket(models.Model):
    _inherit = "him.bar.ticket"

    pos_order_id = fields.Many2one("pos.order", "Đơn POS", ondelete="cascade")
    pos_key = fields.Char("Mã đơn POS (uuid)", index=True)

    @api.model
    def _send_delta(self, key, title, customer, note, lines, pos_order=None):
        """Gửi xuống Bar phần món CHƯA gửi của đơn POS (theo key). Trả về số phiếu tạo ra."""
        prev = self.search([("pos_key", "=", key)])
        flat = [{"name": l["name"], "qty": l["qty"], "opts": l["opts"],
                 "pid": l["product"].id, "categ": l["product"].categ_id.id} for l in lines]
        created = 0
        for printer in self.env["him.bar.printer"].search([]):
            allowed = None
            if printer.category_ids:
                allowed = set(self.env["product.category"].search(
                    [("id", "child_of", printer.category_ids.ids)]).ids)
            mine = prev.filtered(lambda t: t.printer_id == printer)
            items = delta.delta_items(flat, delta.sent_totals(mine.mapped("body")), allowed)
            if not items:
                continue
            self.create({
                "name": title + (" · thêm" if mine else ""),
                "printer_id": printer.id, "pos_key": key,
                "pos_order_id": pos_order.id if pos_order else False,
                "channel": "Tại quầy", "customer": customer, "note": note,
                "body": json.dumps(items, ensure_ascii=False),
            })
            created += 1
        return created

    @api.model
    def _from_pos(self, order):
        lines = [{
            "name": l.full_product_name or l.product_id.name, "qty": l.qty, "product": l.product_id,
            "opts": (getattr(l, "customer_note", "") or "").strip(),
        } for l in order.lines if l.product_id and l.qty > 0]
        if not lines:
            return 0
        partner = order.partner_id
        note = getattr(order, "general_note", "") or getattr(order, "note", "") or ""
        key = getattr(order, "uuid", "") or order.pos_reference or order.name
        return self._send_delta(
            key, order.pos_reference or order.name,
            " - ".join(x for x in (partner.name, partner.phone) if x) or "Khách lẻ",
            html2plaintext(note).strip() if note else "", lines, pos_order=order)


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for o in orders:
            try:
                with self.env.cr.savepoint():
                    self.env["him.bar.ticket"].sudo()._from_pos(o)
            except Exception:
                _logger.exception("Khong tao duoc phieu in cho don POS %s", o.name)
        return orders
