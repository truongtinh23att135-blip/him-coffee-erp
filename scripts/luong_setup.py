import json, os, random, urllib.request, urllib.error
from datetime import date, datetime, timedelta
KEY = open(os.path.expanduser("~/Documents/odoo-api-key.txt")).read().strip()

def odoo(model, method, body):
    req = urllib.request.Request(
        f"http://localhost:8069/json/2/{model}/{method}", data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"bearer {KEY}", "X-Odoo-Database": "him_coffee_erp",
                 "Content-Type": "application/json; charset=utf-8"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        print("   LOI:", e.read().decode()[:400])
        raise

print("== 1. THONG SO LUONG ==")
CFG = {"name": "Cấu hình lương HIM COFFEE", "standard_days": 26, "hours_per_day": 8,
       "ot_rate_weekday": 1.5, "ot_rate_weekend": 2.0, "ot_rate_holiday": 3.0,
       "rate_bhxh": 8.0, "rate_bhyt": 1.5, "rate_bhtn": 1.0,
       "personal_deduction": 15500000, "dependent_deduction": 6200000}
c = odoo("simple.payroll.config", "search", {"domain": [], "limit": 1})
if c:
    odoo("simple.payroll.config", "write", {"ids": c, "vals": CFG})
    print("DA SUA :", CFG["name"])
else:
    c = odoo("simple.payroll.config", "create", {"vals_list": [CFG]})
    print("DA TAO :", CFG["name"])
cap = odoo("simple.payroll.config", "read", {"ids": c, "fields": ["insurance_cap", "unemployment_cap"]})[0]
print(f"Tran BHXH/BHYT: {cap['insurance_cap']:,.0f} | Tran BHTN: {cap['unemployment_cap']:,.0f}  <-- KIEM TRA lai theo quy dinh va vung cua quan")

print("== 2. HO SO LUONG NHAN VIEN ==")
# ma: (luong co ban/thang, phu cap co dinh, dong bao hiem, tinh thue)
P = {"NV001": (18000000, 1000000, True, True), "NV002": (8000000, 700000, True, True),
     "NV003": (7500000, 700000, True, True), "NV004": (7500000, 500000, True, True),
     "NV005": (7500000, 500000, True, True), "NV006": (5200000, 0, False, False),
     "NV007": (8000000, 500000, True, True), "NV008": (5824000, 0, False, False)}
emp = {}
for code, (wage, allow, ins, tax) in P.items():
    r = odoo("hr.employee", "search_read", {"domain": [["barcode", "=", code]], "fields": ["name"], "limit": 1})
    if not r:
        print("THIEU NHAN VIEN", code, "(hay chay script nhan vien truoc)")
        continue
    emp[code] = r[0]["id"]
    vals = {"employee_id": emp[code], "wage": wage, "allowance": allow, "pay_insurance": ins,
            "pay_tax": tax, "dependents": 0, "insurance_salary": 0}
    old = odoo("simple.payroll.profile", "search", {"domain": [["employee_id", "=", emp[code]]], "limit": 1})
    if old:
        odoo("simple.payroll.profile", "write", {"ids": old, "vals": vals})
    else:
        odoo("simple.payroll.profile", "create", {"vals_list": [vals]})
    print("DA SUA :" if old else "DA TAO :", code, r[0]["name"], f"{wage:,}")

print("== 3. CHAM CONG THANG TRUOC ==")
first = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)
nxt = (first + timedelta(days=32)).replace(day=1)
F, H7 = "%Y-%m-%d %H:%M:%S", timedelta(hours=7)
lo = datetime.combine(first, datetime.min.time()) - H7
hi = datetime.combine(nxt, datetime.min.time()) - H7
SHIFT = {"NV001": (7, 15), "NV002": (7, 15), "NV005": (7, 15), "NV007": (7, 15)}
random.seed(11)
for i, (code, eid) in enumerate(emp.items()):
    dom = [["employee_id", "=", eid], ["check_in", ">=", lo.strftime(F)], ["check_in", "<", hi.strftime(F)]]
    if odoo("hr.attendance", "search", {"domain": dom, "limit": 1}):
        print("CO SAN :", code)
        continue
    s, e = SHIFT.get(code, (15, 22.5))
    rows, d = [], first
    while d < nxt:
        part_time = code in ("NV006", "NV008") and d.day % 3 == 0
        if (d.day + i) % 7 != 0 and not part_time:
            day = datetime.combine(d, datetime.min.time())
            ci = day + timedelta(hours=s, minutes=random.randint(-5, 12)) - H7
            extra = random.randint(60, 120) if random.random() < 0.12 else 0
            co = day + timedelta(hours=e, minutes=random.randint(0, 20) + extra) - H7
            rows.append({"employee_id": eid, "check_in": ci.strftime(F), "check_out": co.strftime(F)})
        d += timedelta(days=1)
    odoo("hr.attendance", "create", {"vals_list": rows})
    print("DA TAO :", code, len(rows), "ngay cong")

print("== 4. DOT TINH LUONG ==")
name = f"Lương tháng {first:%m/%Y}"
run = odoo("simple.payroll.run", "search", {"domain": [["name", "=", name]], "limit": 1})
if not run:
    run = odoo("simple.payroll.run", "create", {"vals_list": [{
        "name": name, "date_from": first.isoformat(), "date_to": (nxt - timedelta(days=1)).isoformat()}]})
odoo("simple.payroll.run", "action_generate", {"ids": run})
slips = odoo("simple.payroll.payslip", "search_read", {"domain": [["run_id", "=", run[0]]], "fields": ["employee_id", "state"]})
for s in slips:
    if s["state"] != "draft":
        continue
    att = odoo("hr.attendance", "search_read", {"domain": [
        ["employee_id", "=", s["employee_id"][0]], ["check_in", ">=", lo.strftime(F)],
        ["check_in", "<", hi.strftime(F)], ["check_out", "!=", False]],
        "fields": ["check_in", "check_out"], "limit": 500})
    per = {}
    for a in att:
        ci, co = datetime.strptime(a["check_in"], F), datetime.strptime(a["check_out"], F)
        day = (ci + H7).date()
        per[day] = per.get(day, 0.0) + (co - ci).total_seconds() / 3600.0
    wk = we = 0.0
    for day, h in per.items():
        extra = h - 8
        if extra > 0 and extra * 60 >= 15:
            if day.weekday() >= 5:
                we += extra
            else:
                wk += extra
    odoo("simple.payroll.payslip", "write", {"ids": [s["id"]], "vals": {
        "worked_days": len(per), "ot_weekday": round(wk, 2), "ot_weekend": round(we, 2)}})

rows = odoo("simple.payroll.payslip", "search_read", {"domain": [["run_id", "=", run[0]]], "fields": [
    "employee_id", "worked_days", "ot_weekday", "ot_weekend", "gross", "bhxh", "bhyt", "bhtn", "tax", "net"]})
print(f"{'Nhan vien':<20}{'Cong':>5}{'OT(h)':>7}{'Thu nhap':>13}{'BH':>10}{'TNCN':>9}{'Thuc linh':>13}")
for r in rows:
    print(f"{r['employee_id'][1]:<20}{r['worked_days']:>5g}{r['ot_weekday'] + r['ot_weekend']:>7.1f}"
          f"{r['gross']:>13,.0f}{r['bhxh'] + r['bhyt'] + r['bhtn']:>10,.0f}{r['tax']:>9,.0f}{r['net']:>13,.0f}")
print("XONG. Vao Odoo > Luong > Dot tinh luong > mo dot de xem, xac nhan va thanh toan.")
