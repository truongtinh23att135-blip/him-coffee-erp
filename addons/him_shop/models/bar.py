import json
import logging

from odoo import api, fields, models
from odoo.tools import html2plaintext

_logger = logging.getLogger(__name__)


class HimBarPrinter(models.Model):
    _name = "him.bar.printer"
    _description = "Máy in ảo (phiếu pha chế)"

    name = fields.Char("Tên máy in", required=True)
    active = fields.Boolean(default=True)
    category_ids = fields.Many2many(
        "product.category", string="Nhóm món in ở máy này",
        help="Để trống = in mọi món. Chọn nhóm cha thì gồm cả nhóm con.")
    copies = fields.Integer("Số liên mỗi phiếu", default=1)
    auto_print = fields.Boolean("Tự in khi có phiếu mới", default=True)
    pending_count = fields.Integer("Phiếu chưa xong", compute="_compute_pending")

    def _compute_pending(self):
        for p in self:
            p.pending_count = self.env["him.bar.ticket"].search_count(
                [("printer_id", "=", p.id), ("state", "!=", "done")])


class HimBarTicket(models.Model):
    _name = "him.bar.ticket"
    _description = "Phiếu in pha chế"
    _order = "id desc"

    name = fields.Char("Số phiếu", required=True)
    printer_id = fields.Many2one("him.bar.printer", "Máy in", required=True, ondelete="cascade")
    order_id = fields.Many2one("sale.order", "Đơn hàng", ondelete="cascade")
    channel = fields.Char("Kênh")
    customer = fields.Char("Khách")
    note = fields.Text("Ghi chú")
    body = fields.Text("Nội dung (JSON)")
    state = fields.Selection(
        [("new", "Mới"), ("printed", "Đã in"), ("done", "Đã làm xong")], default="new")
    printed_at = fields.Datetime("Giờ in")

    @api.model
    def _from_order(self, order):
        if self.search_count([("order_id", "=", order.id)]):
            return
        for printer in self.env["him.bar.printer"].search([]):
            lines = order.order_line.filtered(lambda l: not l.display_type and l.product_id)
            if printer.category_ids:
                allowed = self.env["product.category"].search(
                    [("id", "child_of", printer.category_ids.ids)])
                lines = lines.filtered(lambda l: l.product_id.categ_id in allowed)
            if not lines:
                continue
            items = []
            for l in lines:
                head, _sep, tail = (l.name or "").partition(" | ")
                items.append({"name": head or l.product_id.name, "qty": l.product_uom_qty, "opts": tail})
            partner = order.partner_id
            self.create({
                "name": order.name, "printer_id": printer.id, "order_id": order.id,
                "channel": order.team_id.name or "Online",
                "customer": " - ".join(x for x in (partner.name, partner.phone) if x),
                "note": html2plaintext(order.note or "").strip(),
                "body": json.dumps(items, ensure_ascii=False),
            })


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()
        for o in self:
            if o.origin == "WEB" or o.team_id.name == "Online":
                try:
                    with self.env.cr.savepoint():
                        self.env["him.bar.ticket"].sudo()._from_order(o)
                except Exception:
                    _logger.exception("Khong tao duoc phieu in cho don %s", o.name)
        return res
