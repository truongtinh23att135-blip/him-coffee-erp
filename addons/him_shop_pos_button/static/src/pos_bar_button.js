/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    himNotify(message, type) {
        const svc = this.notification || (this.env && this.env.services && this.env.services.notification);
        if (svc && svc.add) {
            svc.add(message, { type });
        } else {
            console.log(message);
        }
    },

    async himSendToBar() {
        const order = this.getOrder();
        if (!order) {
            return;
        }
        const raw = (order.getOrderlines ? order.getOrderlines() : order.lines) || [];
        const val = (l, getter, field) => (typeof l[getter] === "function" ? l[getter]() : l[field]);
        const lines = raw.map((l) => ({
            product_id: l.product_id && l.product_id.id,
            name: val(l, "getFullProductName", "full_product_name") ||
                (l.product_id && (l.product_id.display_name || l.product_id.name)) || "",
            qty: val(l, "getQuantity", "qty"),
            note: l.customer_note || "",
        }));
        try {
            const r = await fetch("/him/bar/pos_send", {
                method: "POST",
                credentials: "same-origin",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ data: {
                    key: String(order.uuid || order.id || order.name),
                    title: String(order.pos_reference || order.name || order.trackingNumber || "POS"),
                    customer: (order.partner_id && order.partner_id.name) || "",
                    note: order.internal_note || order.general_note || "",
                    lines,
                } }),
            });
            const j = await r.json();
            const n = (j.result && j.result.sent) || 0;
            this.himNotify(n ? `Đã gửi ${n} phiếu xuống Bar` : "Không có món mới để gửi", n ? "success" : "info");
        } catch (e) {
            this.himNotify("Không gửi được xuống Bar: " + e.message, "danger");
        }
    },
});
