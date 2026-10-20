import json


def sent_totals(bodies):
    """Cộng dồn số lượng đã gửi xuống Bar, theo (mã món hoặc tên, ghi chú)."""
    sent = {}
    for body in bodies:
        for x in json.loads(body or "[]"):
            k = (x.get("pid") or x["name"], x.get("opts", ""))
            sent[k] = sent.get(k, 0) + x["qty"]
    return sent


def delta_items(lines, sent, allowed):
    """lines: [{name, qty, opts, pid, categ}]; allowed: tập id nhóm món hoặc None (in mọi món)."""
    cur = {}
    for l in lines:
        k = (l["pid"] or l["name"], l["opts"])
        if k in cur:
            cur[k]["qty"] += l["qty"]
        else:
            cur[k] = dict(l)
    out = []
    for k, l in cur.items():
        if allowed is not None and l["categ"] not in allowed:
            continue
        extra = l["qty"] - sent.get(k, 0)
        if extra > 0:
            out.append({"name": l["name"], "qty": extra, "opts": l["opts"], "pid": l["pid"]})
    return out
