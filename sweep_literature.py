import csv
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import urlopen, Request


BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, "docs")
OUT = os.path.join(DOCS, "related_work_matrix.csv")
META = os.path.join(DOCS, "sweep_meta.json")

QUERIES = [
    "robot invariance",
    "robot equivariance",
    "robot auditing",
    "robot foundation model manipulation",
    "robot world model",
    "embodied intelligence invariance",
    "sim to real robotics",
    "robot tactile perception",
    "robot control learning",
    "robot planning learning",
    "robot representation learning",
    "robot manipulation learning",
    "robot 3D perception",
    "robot state estimation learning",
    "robot dynamics learning",
]

KEYWORDS = [
    "robot", "manipulation", "control", "planning", "equivariance", "invariance",
    "embodied", "tactile", "world model", "sim-to-real", "locomotion", "grasp",
    "navigation", "perception", "policy", "foundation", "learning", "vision",
]


def fetch_json(url, timeout=30):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def clean(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def crossref_search(query, rows=100, offset=0):
    params = urlencode({
        "query.title": query,
        "rows": rows,
        "offset": offset,
        "select": "DOI,title,author,container-title,created,abstract,type,URL",
    })
    return fetch_json("https://api.crossref.org/works?" + params)


def score_item(item):
    blob = " ".join([
        item.get("title", ""),
        item.get("container_title", ""),
        item.get("abstract", ""),
    ]).lower()
    score = 0
    for kw in KEYWORDS:
        if kw in blob:
            score += 1
    if "robot" in blob:
        score += 2
    return score


def main():
    os.makedirs(DOCS, exist_ok=True)
    seen = {}
    rows = []
    errors = []
    for q in QUERIES:
        for offset in range(0, 200, 100):
            try:
                data = crossref_search(q, rows=100, offset=offset)
                items = data.get("message", {}).get("items", [])
            except Exception as e:
                errors.append({"query": q, "offset": offset, "error": repr(e)})
                continue
            for it in items:
                title = clean((it.get("title") or [""])[0])
                if not title:
                    continue
                doi = clean(it.get("DOI", "")).lower()
                key = doi or norm_title(title)
                if key in seen:
                    continue
                authors = it.get("author", [])
                author0 = ""
                if authors:
                    a = authors[0]
                    author0 = " ".join(filter(None, [a.get("given", ""), a.get("family", "")])).strip()
                year = ""
                created = it.get("created", {}).get("date-parts", [])
                if created and created[0]:
                    year = str(created[0][0])
                row = {
                    "paper_id": str(len(rows) + 1),
                    "query_seed": q,
                    "title": title,
                    "year": year,
                    "venue": clean((it.get("container-title") or [""])[0]),
                    "author0": author0,
                    "doi": doi,
                    "url": clean(it.get("URL", "")),
                    "score": score_item({
                        "title": title,
                        "container_title": row.get("venue", "") if False else clean((it.get("container-title") or [""])[0]),
                        "abstract": clean(it.get("abstract", "")),
                    }),
                    "problem_claimed": "",
                    "mechanism": "",
                    "hidden_assumptions": "",
                    "fixed_variables": "",
                    "ignored_failures": "",
                    "less_novel": "",
                    "open_questions": "",
                }
                seen[key] = True
                rows.append(row)
            time.sleep(0.2)
    rows.sort(key=lambda r: (-r["score"], r["year"], r["title"]))
    for i, r in enumerate(rows, 1):
        r["paper_id"] = str(i)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows[:1200])
    with open(META, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "queries": QUERIES,
            "count": len(rows),
            "errors": errors[:20],
        }, f, indent=2)
    print(f"wrote {min(len(rows),1200)} rows to {OUT}")
    print(f"errors {len(errors)}")


if __name__ == "__main__":
    sys.exit(main())
