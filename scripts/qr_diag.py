import json, os, urllib.request, urllib.error
KEY = open(os.path.expanduser("~/Documents/odoo-api-key.txt")).read().strip()

def odoo(model, method, body):
    req = urllib.request.Request(
        f"http://localhost:8069/json/2/{model}/{method}", data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"bearer {KEY}", "X-Odoo-Database": "him_coffee_erp",
                 "Content-Type": "application/json; charset=utf-8"})
    return json.load(urllib.request.urlopen(req, timeout=120))

def read(model, ids, fields):
    out = {}
    for f in fields:
        try:
            out.update(odoo(model, "read", {"ids": ids, "fields": [f]})[0])
        except Exception:
            out[f] = "(khong co truong nay)"
    return out

def mask(s):
    s = str(s or "")
    return ("*" * max(len(s) - 4, 0)) + s[-4:] if s else "(trong)"

print("Module:", {m["name"]: m["state"] for m in odoo("ir.module.module", "search_read", {
    "domain": [["name", "in", ["l10n_vn", "account_qr_code_emv", "point_of_sale"]]], "fields": ["name", "state"]})})
pms = odoo("pos.payment.method", "search_read", {"domain": [], "fields": ["name"]})
print("Phuong thuc thanh toan:", [(p["id"], p["name"]) for p in pms])
for p in pms:
    if "QR" not in p["name"] and "khoản" not in p["name"]:
        continue
    d = read("pos.payment.method", [p["id"]], ["name", "payment_method_type", "qr_code_method", "journal_id", "config_ids"])
    print("\n== PHUONG THUC:", d)
    jid = d["journal_id"][0] if isinstance(d.get("journal_id"), list) else None
    if jid:
        j = read("account.journal", [jid], ["name", "type", "bank_account_id"])
        print("  Nhat ky:", j)
        bid = j["bank_account_id"][0] if isinstance(j.get("bank_account_id"), list) else None
        if bid:
            b = read("res.partner.bank", [bid], ["acc_number", "bank_id", "proxy_type", "proxy_value", "include_reference"])
            print("  Tai khoan NH: so", mask(b.get("acc_number")), "| ngan hang", b.get("bank_id"),
                  "| proxy_type", b.get("proxy_type"), "| proxy_value", mask(b.get("proxy_value")), "| ghi ma don", b.get("include_reference"))
            if isinstance(b.get("bank_id"), list):
                print("  Ngan hang (BIN):", read("res.bank", [b["bank_id"][0]], ["name", "bic"]))
        else:
            print("  >>> Nhat ky CHUA co tai khoan ngan hang")
for c in odoo("pos.config", "search_read", {"domain": [], "fields": ["name"]}):
    cfg = read("pos.config", [c["id"]], ["payment_method_ids"])
    print("POS", c["id"], c["name"], "-> phuong thuc:", cfg.get("payment_method_ids"))
print("Cong ty bat QR:", read("res.company", odoo("res.company", "search", {"domain": [], "limit": 1}), ["qr_code"]))
