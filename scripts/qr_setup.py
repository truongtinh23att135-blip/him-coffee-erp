import json, os, urllib.request, urllib.error
KEY = open(os.path.expanduser("~/Documents/odoo-api-key.txt")).read().strip()
PM_NAME = "Chuyển khoản / QR - C1"
BINS = {"mb": "970422", "mbbank": "970422", "vietcombank": "970436", "vcb": "970436",
        "techcombank": "970407", "tcb": "970407", "acb": "970416", "bidv": "970418",
        "vietinbank": "970415", "agribank": "970405", "tpbank": "970423",
        "vpbank": "970432", "sacombank": "970403"}

def odoo(model, method, body, quiet=False):
    req = urllib.request.Request(
        f"http://localhost:8069/json/2/{model}/{method}", data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"bearer {KEY}", "X-Odoo-Database": "him_coffee_erp",
                 "Content-Type": "application/json; charset=utf-8"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        if not quiet:
            print("   LOI:", e.read().decode()[:300].replace("\n", " "))
        raise

def options(model, field):
    r = odoo("ir.model.fields.selection", "search_read", {"domain": [
        ["field_id.model", "=", model], ["field_id.name", "=", field]], "fields": ["value", "name"]}, True)
    return [(x["value"], x["name"]) for x in r]

def has_field(model, field):
    return bool(odoo("ir.model.fields", "search", {"domain": [["model", "=", model], ["name", "=", field]]}, True))

print("== 1. HIEN TRANG ==")
mods = {m["name"]: m["state"] for m in odoo("ir.module.module", "search_read", {
    "domain": [["name", "in", ["l10n_vn", "account_qr_code_emv", "point_of_sale"]]], "fields": ["name", "state"]})}
print("  Module:", mods)
company = odoo("res.company", "search_read", {"domain": [], "fields": ["name", "partner_id", "country_id"], "limit": 1})[0]
print("  Cong ty:", company["name"], "| quoc gia:", company["country_id"])
pm = odoo("pos.payment.method", "search_read", {"domain": [["name", "=", PM_NAME]], "fields": ["name", "journal_id"], "limit": 1})
print("  Phuong thuc thanh toan POS:", pm)
print("  Cac truong QR cua pos.payment.method:", [f for f in ("payment_method_type", "qr_code_method") if has_field("pos.payment.method", f)])
print("  Tuy chon payment_method_type:", options("pos.payment.method", "payment_method_type"))
print("  Tuy chon qr_code_method     :", options("pos.payment.method", "qr_code_method"))
print("  Tuy chon proxy_type (tai khoan ngan hang):", options("res.partner.bank", "proxy_type"))
ok = mods.get("l10n_vn") == "installed" and mods.get("point_of_sale") == "installed"
if not ok:
    raise SystemExit("\nThieu module Vietnam - Accounting (l10n_vn). Gui ket qua tren cho minh, DUNG tu cai.")

print("\n== 2. THONG TIN TAI KHOAN NHAN TIEN (se lam ra ma QR that, hay nhap CHINH XAC) ==")
bank_in = input("Ten ngan hang (vi du MB, Vietcombank, Techcombank, ACB, BIDV): ").strip()
acc = input("So tai khoan nhan tien: ").strip()
holder = input("Ten chu tai khoan (IN HOA, khong dau): ").strip().upper()
if not (bank_in and acc.isdigit() and holder):
    raise SystemExit("Thieu thong tin, chua thay doi gi. Chay lai khi co du ngan hang, so tai khoan, ten chu tai khoan.")
bin_code = BINS.get(bank_in.lower().replace(" ", ""))
if not bin_code:
    bin_code = input("Khong co san ma BIN cua ngan hang nay. Nhap ma BIN (6 so): ").strip()
if not (bin_code.isdigit() and len(bin_code) == 6):
    raise SystemExit("Ma BIN phai gom dung 6 chu so.")
print(f"\nNgan hang: {bank_in} | BIN: {bin_code} | STK: {acc} | Chu TK: {holder}")
print("CANH BAO: ma QR se chuyen TIEN THAT vao tai khoan nay. Kiem tra ma BIN tren danh sach ngan hang VietQR.")
if input("Gõ Y de tiep tuc: ").strip().upper() != "Y":
    raise SystemExit("Da huy, chua thay doi gi.")

print("\n== 3. CAU HINH ==")
def try_write(model, ids, vals, label):
    try:
        odoo(model, "write", {"ids": ids, "vals": vals}, True)
        print("DA DAT :", label)
        return True
    except Exception:
        print("BO QUA :", label, "(Odoo khong nhan truong nay)")
        return False

cid = odoo("res.company", "search", {"domain": [], "limit": 1})
if has_field("res.company", "qr_code"):
    try_write("res.company", cid, {"qr_code": True}, "bat ma QR ngan hang (Accounting)")

vn = odoo("res.country", "search", {"domain": [["code", "=", "VN"]], "limit": 1})
bank = odoo("res.bank", "search", {"domain": [["bic", "=", bin_code]], "limit": 1})
if not bank:
    bank = odoo("res.bank", "search", {"domain": [["name", "ilike", bank_in]], "limit": 1})
    if bank:
        try_write("res.bank", bank, {"bic": bin_code}, "gan ma BIN cho ngan hang co san")
if not bank:
    bank = odoo("res.bank", "create", {"vals_list": [{"name": bank_in, "bic": bin_code, "country": vn[0] if vn else False}]})
    print("DA TAO : ngan hang", bank_in)
partner = company["partner_id"][0]
pb = odoo("res.partner.bank", "search", {"domain": [["acc_number", "=", acc], ["partner_id", "=", partner]], "limit": 1})
if not pb:
    pb = odoo("res.partner.bank", "create", {"vals_list": [{
        "partner_id": partner, "acc_number": acc, "bank_id": bank[0], "acc_holder_name": holder}]})
    print("DA TAO : tai khoan ngan hang", acc)
else:
    print("CO SAN : tai khoan ngan hang", acc)
proxy = [o for o in options("res.partner.bank", "proxy_type") if o[0] not in ("none", False)]
pick = [o for o in proxy if any(k in (o[0] + o[1]).lower() for k in ("account", "bank", "stk"))]
if len(pick) == 1 or (not pick and len(proxy) == 1):
    ptype = (pick or proxy)[0][0]
else:
    for i, o in enumerate(proxy):
        print(f"  [{i}] {o[0]} - {o[1]}")
    ptype = proxy[int(input("Chon loai dinh danh (so tai khoan ngan hang): "))][0] if proxy else None
if ptype:
    try_write("res.partner.bank", pb, {"proxy_type": ptype}, f"loai dinh danh = {ptype}")
    try_write("res.partner.bank", pb, {"proxy_value": acc}, "gia tri dinh danh = so tai khoan")
if has_field("res.partner.bank", "include_reference"):
    try_write("res.partner.bank", pb, {"include_reference": True}, "ghi ma don vao noi dung chuyen khoan")
try_write("res.partner", [partner], {"city": "TP. Vinh", **({"country_id": vn[0]} if vn else {})}, "dia chi cong ty (thanh pho, quoc gia)")

journal = pm[0]["journal_id"][0] if pm and pm[0]["journal_id"] else None
if journal:
    jt = odoo("account.journal", "read", {"ids": [journal], "fields": ["type", "name"]})[0]
    if jt["type"] != "bank":
        print("Nhat ky hien tai la loai", jt["type"], "- chuyen sang nhat ky ngan hang")
        journal = None
if not journal:
    jb = odoo("account.journal", "search", {"domain": [["type", "=", "bank"]], "limit": 1})
    journal = jb[0] if jb else None
if not journal:
    raise SystemExit("Chua co nhat ky ngan hang. Tao trong Invoicing > Configuration > Journals roi chay lai.")
try_write("account.journal", [journal], {"bank_account_id": pb[0]}, "gan tai khoan ngan hang vao nhat ky")

qopt = [o[0] for o in options("pos.payment.method", "qr_code_method")]
qr_m = next((v for v in qopt if "emv" in v.lower()), None)
vals = {"journal_id": journal, "payment_method_type": "qr_code"}
if qr_m:
    vals["qr_code_method"] = qr_m
if pm:
    for k, v in vals.items():
        try_write("pos.payment.method", [pm[0]["id"]], {k: v}, f"phuong thuc '{PM_NAME}': {k} = {v}")
else:
    print("KHONG THAY phuong thuc thanh toan", PM_NAME, "- tao trong POS > Configuration > Payment Methods")
print("\nXONG. Vao POS, nhan Ctrl+Shift+R, them mon, bam Payment, chon '" + PM_NAME + "'.")
print("Kiem tra bang app ngan hang: ten nguoi nhan va so tien phai dung (CHUA bam thanh toan).")
