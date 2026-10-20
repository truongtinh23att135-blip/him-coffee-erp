import json, os, re, urllib.request, urllib.error
KEY = open(os.path.expanduser("~/Documents/odoo-api-key.txt")).read().strip()
APP_JS = os.path.expanduser("~/him-coffee-web/public/app.js")
CAT = {"cafe": "1. Cà Phê", "may": "2. Cà Phê Máy", "milk": "3. Milk Tea HIM",
       "yogurt": "4. Yogurt Ice", "khac": "5. Khác"}

def odoo(model, method, body, quiet=False):
    req = urllib.request.Request(
        f"http://localhost:8069/json/2/{model}/{method}", data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"bearer {KEY}", "X-Odoo-Database": "him_coffee_erp",
                 "Content-Type": "application/json; charset=utf-8"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        if not quiet:
            print("   LOI:", e.read().decode()[:400])
        raise
print("== DANH MUC POS ==")
cid = {}
for i, (k, v) in enumerate(CAT.items(), 1):
    ids = odoo("pos.category", "search", {"domain": [["name", "=", v]], "limit": 1})
    cid[k] = ids[0] if ids else odoo("pos.category", "create", {"vals_list": [{"name": v, "sequence": i}]})[0]
    print("CO SAN :" if ids else "DA TAO :", v)

print("== MON TREN POS ==")
menu = re.findall(r'\["([^"]+)",\s*(\d+),\s*"(\w+)"', open(APP_JS, encoding="utf-8").read())
print(len(menu), "mon tren web")
for name, price, c in menu:
    p = odoo("product.product", "search", {"domain": [["name", "=", name]], "limit": 1})
    if not p:
        print("THIEU MON TRONG ODOO:", name)
        continue
    vals = {"available_in_pos": True, "sale_ok": True, "pos_categ_ids": [[6, 0, [cid[c]]]]}
    try:
        odoo("product.product", "write", {"ids": p, "vals": vals}, True)
    except Exception:
        vals.pop("pos_categ_ids")
        vals["pos_categ_id"] = cid[c]
        odoo("product.product", "write", {"ids": p, "vals": vals})
    print("DA DAT :", name, "->", CAT[c])

rows = odoo("product.product", "search_read", {"domain": [["available_in_pos", "=", True]], "fields": ["name"], "limit": 500})
print("San pham dang ban tren POS:", len(rows))
print("XONG. Mo POS, bam F5 de tai lai danh sach mon.")
