#!/usr/bin/env python3
"""Validate A&N programme-level records without inventing missing information.

Input: data/university-programmes.json (optional). This validator runs in CI.
Records without verifiable evidence remain incomplete and are never counted as verified.
"""
from __future__ import annotations
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import json
import sys

SOURCE = Path("data/university-programmes.json")
OUTPUT = Path("site/university-verification.json")
FIELDS = ("university_id", "university_name", "country", "programme_name", "level",
          "official_source", "checked_on")
FACTS = {
    "tuition": ("tuition_amount", "tuition_currency", "tuition_basis", "tuition_source"),
    "intake": ("intake", "intake_source"),
    "deadline": ("deadline", "deadline_source"),
    "entry": ("entry_requirements", "entry_source"),
    "english": ("english_requirements", "english_source"),
    "scholarship": ("scholarship_details", "scholarship_source"),
}
def https(value):
    try:
        parsed = urlparse(str(value))
        return parsed.scheme == "https" and bool(parsed.netloc)
    except (TypeError, ValueError):
        return False

def checked(value):
    try:
        d = date.fromisoformat(str(value))
        return d <= datetime.now(timezone.utc).date()
    except ValueError:
        return False

def present(value):
    return value is not None and value != "" and value != []

def validate(records):
    results = []
    for i, record in enumerate(records):
        if not isinstance(record, dict):
            results.append({"row": i + 1, "verified": False, "errors": ["Record is not an object"]})
            continue
        errors = [f"Missing {field}" for field in FIELDS if not present(record.get(field))]
        if present(record.get("official_source")) and not https(record["official_source"]):
            errors.append("Official source must be an HTTPS URL")
        if present(record.get("checked_on")) and not checked(record["checked_on"]):
            errors.append("Invalid or future checked_on date")
        facts = {}
        for name, fields in FACTS.items():
            populated = [present(record.get(field)) for field in fields]
            source_field = fields[-1]
            if any(populated) and not all(populated):
                errors.append(f"Incomplete {name}: provide all values and source")
            if all(populated) and not https(record[source_field]):
                errors.append(f"{name} source must be HTTPS")
            facts[name] = all(populated) and https(record.get(source_field))
        if facts["tuition"]:
            try:
                if float(record["tuition_amount"]) < 0:
                    errors.append("Tuition cannot be negative")
            except (TypeError, ValueError):
                errors.append("Tuition amount must be numeric")
        if facts["deadline"]:
            try:
                date.fromisoformat(str(record["deadline"]))
            except ValueError:
                errors.append("Deadline must be YYYY-MM-DD")
        results.append({"row": i + 1, "university_id": record.get("university_id"),
                        "programme_name": record.get("programme_name"),
                        "verified": not errors and all(facts.values()),
                        "verified_fields": [k for k, v in facts.items() if v],
                        "errors": errors})
    return results

def main():
    if SOURCE.exists():
        try:
            data = json.loads(SOURCE.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                raise ValueError("Programme data must be a JSON array")
        except (ValueError, OSError) as exc:
            print(f"Invalid programme data: {exc}", file=sys.stderr)
            return 1
    else:
        data = []
    results = validate(data)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "programme-level evidence completeness, not confirmation that linked sources are correct",
        "total_programme_records": len(data),
        "fully_evidenced_programmes": sum(r["verified"] for r in results),
        "incomplete_programmes": sum(not r["verified"] for r in results),
        "review": results,
        "notice": "A valid HTTPS link is not proof of official accuracy. Manual source checks are still required.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Programme records: {len(data)}; fully evidenced: {report['fully_evidenced_programmes']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
