import json, os, re, urllib.request, urllib.error
KEY = open(os.path.expanduser("~/Documents/odoo-api-key.txt")).read().strip()
VAT = 8.0  # thue GTGT (%). Doi thanh 10.0 khi het han giam thue (31/12/2026) neu khong duoc gia han
APP_JS = os.path.expanduser("~/him-coffee-web/public/app.js")

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

def read1(model, ids, fields):
    try:
        return odoo(model, "read", {"ids": ids, "fields": fields}, True)[0]
    except Exception:
        out = {}
        for f in fields:
            try:
                out.update(odoo(model, "read", {"ids": ids, "fields": [f]}, True)[0])
            except Exception:
                pass
        return out

print("== 1. HIEN TRANG ==")
cid = odoo("res.company", "search", {"domain": [], "limit": 1})
co = read1("res.company", cid, ["name", "country_id", "currency_id", "vat", "street", "street2",
                                "city", "phone", "chart_template", "report_footer"])
for k in ("name", "country_id", "currency_id", "vat", "chart_template"):
    print(f"  {k:<15}: {co.get(k)}")
mods = odoo("ir.module.module", "search_read", {"domain": [["name", "in", ["account", "l10n_vn", "sale", "point_of_sale"]]], "fields": ["name", "state"]})
print("  Modules:", {m["name"]: m["state"] for m in mods})
print("  Hoa don da vao so:", odoo("account.move", "search_count", {"domain": [["move_type", "=", "out_invoice"], ["state", "=", "posted"]]}))
if not co.get("vat"):
    print("  CHUA CO MA SO THUE (MST): nhap trong Settings > Companies (script khong the doan)")

print("== 2. THONG TIN CONG TY ==")
fill = {"street": "78 Nguyễn Thị Minh Khai", "street2": "P. Hưng Bình", "city": "TP. Vinh", "phone": "1900 6886",
        "report_footer": "HIM COFFEE Roastery · 78 Nguyễn Thị Minh Khai, P. Hưng Bình, TP. Vinh, Nghệ An · Hotline 1900 6886"}
vn = odoo("res.country", "search", {"domain": [["code", "=", "VN"]], "limit": 1})
if vn and not co.get("country_id"):
    fill["country_id"] = vn[0]
for k, v in fill.items():
    if co.get(k):
        print("CO SAN :", k)
        continue
    try:
        odoo("res.company", "write", {"ids": cid, "vals": {k: v}}, True)
        print("DA DAT :", k)
    except Exception:
        print("BO QUA :", k)
terms = "<p>Thanh toán khi nhận hàng (COD) hoặc chuyển khoản. Cảm ơn quý khách đã sử dụng dịch vụ của HIM COFFEE.</p>"
try:
    odoo("res.company", "write", {"ids": cid, "vals": {"invoice_terms": terms}}, True)
    print("DA DAT : dieu khoan tren hoa don")
except Exception:
    print("BO QUA : dieu khoan tren hoa don")
vnd = odoo("res.currency", "search", {"domain": [["name", "=", "VND"], ["active", "in", [True, False]]], "limit": 1})
if vnd:
    odoo("res.currency", "write", {"ids": vnd, "vals": {"active": True}})
    print("DA BAT : tien te VND")

print("== 3. THUE GTGT ==")
tname = f"VAT {VAT:g}% (đã gồm trong giá)"
tax = odoo("account.tax", "search", {"domain": [["name", "=", tname], ["type_tax_use", "=", "sale"]], "limit": 1})
base = {"name": tname, "amount_type": "percent", "amount": VAT, "type_tax_use": "sale", "description": f"{VAT:g}%"}
if tax:
    print("CO SAN :", tname)
else:
    for extra in ({"price_include_override": "tax_included"}, {"price_include": True}):
        try:
            tax = odoo("account.tax", "create", {"vals_list": [{**base, **extra}]}, True)
            print("DA TAO :", tname)
            break
        except Exception:
            continue
    if not tax:
        try:
            grp = odoo("account.tax.group", "create", {"vals_list": [{"name": "VAT"}]}, True)
            tax = odoo("account.tax", "create", {"vals_list": [{**base, "tax_group_id": grp[0], "price_include_override": "tax_included"}]})
            print("DA TAO :", tname)
        except Exception:
            print("KHONG TAO DUOC THUE: hay gui dong LOI o tren cho minh")
if tax:
    t = read1("account.tax", tax, ["amount", "price_include", "price_include_override"])
    print("  Gia da gom thue:", t.get("price_include", t.get("price_include_override")))
    menu = [m[0] for m in re.findall(r'\["([^"]+)",\s*(\d+),\s*"\w+"', open(APP_JS, encoding="utf-8").read())]
    pids = odoo("product.product", "search", {"domain": [["name", "in", menu]]})
    odoo("product.product", "write", {"ids": pids, "vals": {"taxes_id": [[6, 0, tax]]}})
    print("DA GAN THUE cho", len(pids), "mon")

print("== 4. DIEU KHOAN THANH TOAN ==")
for name, days in (("Thanh toán khi nhận hàng (COD)", 0), ("Công nợ 15 ngày", 15), ("Công nợ 30 ngày", 30)):
    if odoo("account.payment.term", "search", {"domain": [["name", "=", name]], "limit": 1}):
        print("CO SAN :", name)
        continue
    ok = False
    for line in ({"value": "percent", "value_amount": 100, "nb_days": days, "delay_type": "days_after"},
                 {"value": "percent", "value_amount": 100, "nb_days": days}):
        try:
            odoo("account.payment.term", "create", {"vals_list": [{"name": name, "line_ids": [[0, 0, line]]}]}, True)
            ok = True
            break
        except Exception:
            pass
    print("DA TAO :" if ok else "BO QUA :", name)

print("== 5. SO NHAT KY ==")
for name, jtype, code in (("Tiền mặt - COD online", "cash", "COD"), ("Ngân hàng - VietQR", "bank", "VQR")):
    if odoo("account.journal", "search", {"domain": [["code", "=", code]], "limit": 1}):
        print("CO SAN :", name)
        continue
    try:
        odoo("account.journal", "create", {"vals_list": [{"name": name, "type": jtype, "code": code}]}, True)
        print("DA TAO :", name)
    except Exception:
        print("BO QUA :", name, "(tao trong Invoicing > Configuration > Journals)")

print("== 6. TONG KET ==")
for j in odoo("account.journal", "search_read", {"domain": [], "fields": ["name", "type", "code"]}):
    print(f"  [{j['code']}] {j['name']} ({j['type']})")
unpaid = odoo("account.move", "search_read", {"domain": [["move_type", "=", "out_invoice"], ["state", "=", "posted"], ["payment_state", "in", ["not_paid", "partial"]]], "fields": ["amount_residual"]})
print(f"  Hoa don con no: {len(unpaid)} | tong: {sum(x['amount_residual'] for x in unpaid):,.0f}")
print("LUU Y: giam VAT 8% chi het 31/12/2026, tu 01/01/2027 doi VAT ve 10.0 neu khong duoc gia han;")
print("       hay hoi ke toan ve do uong nhieu duong (mot nguon ghi nhan co the khong duoc giam thue trong 2026).")
