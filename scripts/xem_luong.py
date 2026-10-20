import json, os, urllib.request, urllib.error
KEY = open(os.path.expanduser("~/Documents/odoo-api-key.txt")).read().strip()
def odoo(model, method, body):
    req = urllib.request.Request(f"http://localhost:8069/json/2/{model}/{method}",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"bearer {KEY}", "X-Odoo-Database": "him_coffee_erp",
                 "Content-Type": "application/json; charset=utf-8"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        print("   LOI:", e.read().decode()[:300]); return []
print("Module:", odoo("ir.module.module", "search_read", {"domain": [["name", "=", "simple_payroll"]], "fields": ["state"]}))
def xml(m):
    return [r["res_id"] for r in odoo("ir.model.data", "search_read", {"domain": [["module", "=", "simple_payroll"], ["model", "=", m]], "fields": ["res_id"], "limit": 1000})]
models = odoo("ir.model", "read", {"ids": xml("ir.model"), "fields": ["model", "name"]})
fids = xml("ir.model.fields")
fields = odoo("ir.model.fields", "read", {"ids": fids, "fields": ["model", "name", "field_description", "ttype", "required", "relation"]})
sel = odoo("ir.model.fields.selection", "search_read", {"domain": [["field_id", "in", fids]], "fields": ["field_id", "value"]})
selmap = {}
for s in sel: selmap.setdefault(s["field_id"][0], []).append(s["value"])
for m in models:
    n = odoo(m["model"], "search_count", {"domain": []})
    print(f"\n=== {m['model']} ({m['name']}) - {n} ban ghi")
    for f in sorted([x for x in fields if x["model"] == m["model"]], key=lambda x: x["name"]):
        extra = (" -> " + f["relation"]) if f["relation"] else ""
        sv = (" " + str(selmap[f["id"]])) if f["id"] in selmap else ""
        print(f"  {f['name']:<24}{f['ttype']:<10}{'*' if f['required'] else ' '} {f['field_description']}{extra}{sv}")
    names = [x["name"] for x in fields if x["model"] == m["model"]]
    for r in odoo(m["model"], "search_read", {"domain": [], "fields": names, "limit": 3}):
        print("  VD:", json.dumps(r, ensure_ascii=False)[:300])
