import json, os, urllib.request
key = open(os.path.expanduser('~/Documents/odoo-api-key.txt')).read().strip()
req = urllib.request.Request("http://localhost:8069/json/2/stock.quant/search_read",
    data=json.dumps({"domain": [["location_id.usage", "=", "internal"]], "fields": ["product_id", "quantity"], "limit": 500}).encode(),
    method="POST", headers={"Authorization": f"bearer {key}", "X-Odoo-Database": "him_coffee_erp", "Content-Type": "application/json; charset=utf-8"})
tot = {}
for q in json.load(urllib.request.urlopen(req)):
    n = q["product_id"][1]
    tot[n] = tot.get(n, 0) + q["quantity"]
for n, v in sorted(tot.items()): print(f"{v:>10g} | {n}")
