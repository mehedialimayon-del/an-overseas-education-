#!/usr/bin/env python3
"""Generate a conservative, machine-readable inventory of A&N university data assets.
This is a source-file audit, NOT a claim that any student record is complete.
"""
from pathlib import Path
import json
import re
from datetime import datetime, timezone

root = Path("site")
assets = {
    "university_directory": "an-global-universities.js",
    "university_portfolio": "an-portfolio-2026.js",
    "eligibility_interface": "an-eligibility.js",
    "eligibility_rules": "an-eligibility-rules.js",
}
result = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "target_universities": 6210,
    "target_scholarships": 92,
    "audit_scope": "Source asset presence and basic content markers only",
    "fully_verified_universities": None,
    "verified_programme_fees": None,
    "verified_deadlines": None,
    "verified_intakes": None,
    "warning": "Targets are not completion counts. A file existing does not establish that any university record is complete.",
    "assets": {},
}
for name, relative in assets.items():
    p = root / relative
    if not p.is_file():
        result["assets"][name] = {"present": False}
        continue
    s = p.read_text(encoding="utf-8", errors="replace")
    result["assets"][name] = {
        "present": True,
        "bytes": p.stat().st_size,
        "mentions_verification": bool(re.search(r"verif|source|checked", s, re.I)),
    }
(root / "data-quality.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
print(json.dumps(result, indent=2))
