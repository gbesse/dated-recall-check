#!/usr/bin/env python3
"""Compare temporal recall before and after a memory backend upgrade."""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

TEXT = {
    "en": {"title": "Dated recall before → after", "demo": "Offline fixture; use run for two live Hindsight endpoints.", "lost": "lost", "gain": "gained", "same": "unchanged"},
    "fr": {"title": "Rappel daté avant → après", "demo": "Exemple hors ligne ; utilisez run pour deux endpoints Hindsight.", "lost": "perdu", "gain": "gagné", "same": "inchangé"},
    "es": {"title": "Recuerdo fechado antes → después", "demo": "Ejemplo sin conexión; use run para dos endpoints Hindsight.", "lost": "perdido", "gain": "ganado", "same": "sin cambios"},
}


def result_ids(body):
    items = body.get("results", body.get("memories")) if isinstance(body, dict) else body
    if not isinstance(items, list):
        raise ValueError("response has no results/memories list")
    result = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("result item is not an object")
        value = item.get("id", item.get("memory_id", item.get("fact_id")))
        if not isinstance(value, str):
            raise ValueError("result item has no string id")
        result.append(value)
    return result


def recall(base_url, bank, case, token=None):
    path = f"/v1/default/banks/{urllib.parse.quote(bank, safe='')}/memories/recall"
    payload = {key: case[key] for key in ("query", "query_timestamp", "temporal_window", "types", "budget", "max_tokens") if key in case}
    if not payload.get("query"):
        raise ValueError("case has no query")
    headers = {"content-type": "application/json"}
    if token:
        headers["authorization"] = "Bearer " + token
    req = urllib.request.Request(base_url.rstrip("/") + path, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as response:
        return result_ids(json.load(response))


def score(expected, ids, k):
    relevant = set(expected)
    if not relevant:
        raise ValueError("expected_ids must be non-empty")
    return len(relevant.intersection(ids[:k])) / len(relevant)


def compare(cases, before, after, k):
    rows = []
    for case in cases:
        key = case["id"]
        old = score(case["expected_ids"], before[key], k)
        new = score(case["expected_ids"], after[key], k)
        rows.append({"id": key, "query": case["query"], "before": old, "after": new, "lost_ids": sorted(set(case["expected_ids"]) & set(before[key][:k]) - set(after[key][:k]))})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare dated memory recall on matched labelled cases.")
    ap.add_argument("command", choices=["demo", "run"])
    ap.add_argument("--lang", choices=TEXT, default="en")
    ap.add_argument("--cases", type=Path)
    ap.add_argument("--before-url")
    ap.add_argument("--after-url")
    ap.add_argument("--bank")
    ap.add_argument("--token-env")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.k < 1:
        ap.error("--k must be positive")
    if args.command == "demo":
        obj = json.loads((Path(__file__).parent / "fixtures" / "pair.json").read_text())
        cases, before, after = obj["cases"], obj["before"], obj["after"]
    else:
        if not all([args.cases, args.before_url, args.after_url, args.bank]):
            ap.error("run requires --cases, --before-url, --after-url and --bank")
        token = os.environ.get(args.token_env) if args.token_env else None
        if args.token_env and token is None:
            ap.error("token environment variable not set")
        cases = [json.loads(line) for line in args.cases.read_text().splitlines() if line.strip()]
        before = {case["id"]: recall(args.before_url, args.bank, case, token) for case in cases}
        after = {case["id"]: recall(args.after_url, args.bank, case, token) for case in cases}
    try:
        rows = compare(cases, before, after, args.k)
    except (KeyError, ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    summary = {"before": sum(row["before"] for row in rows) / len(rows), "after": sum(row["after"] for row in rows) / len(rows)} if rows else {"before": 0, "after": 0}
    if args.json:
        print(json.dumps({"simulated": args.command == "demo", "k": args.k, "summary": summary, "cases": rows}, ensure_ascii=False, indent=2))
    else:
        print(TEXT[args.lang]["title"])
        if args.command == "demo":
            print(TEXT[args.lang]["demo"])
        for row in rows:
            status = "lost" if row["after"] < row["before"] else ("gain" if row["after"] > row["before"] else "same")
            print(f"{row['id']}: {row['before']:.2f} → {row['after']:.2f} ({TEXT[args.lang][status]}) {','.join(row['lost_ids'])}")
        print(f"recall@{args.k}: {summary['before']:.3f} → {summary['after']:.3f}")
    return 1 if summary["after"] < summary["before"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
