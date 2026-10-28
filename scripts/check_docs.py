#!/usr/bin/env python3
"""Check the layout and the header of every page under docs/ against docs/reference/documentation-standard.md.

    check_docs.py [REPO_ROOT]     check REPO_ROOT/docs (default: the current directory)
    check_docs.py selftest

Errors are printed as GitHub annotations and make the exit status 1; warnings do not.
"""
import datetime as dt
import pathlib
import re
import sys
import tempfile

FOLDER_TYPE = {"tutorials": "tutorial", "how-to": "how-to", "reference": "reference", "explanation": "explanation"}
DECISIONS = "decisions"
STATUS = re.compile(r"^(proposed|accepted|rejected|deprecated|superseded by .+)$")
DECISION_NAME = re.compile(r"^\d{4}-[a-z0-9]+(-[a-z0-9]+)*\.md$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STALE_DAYS = 180


def front_matter(text):
    """Return (dict, body) for a leading ---/--- block of `key: value` lines, or (None, text)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            meta = {}
            for line in lines[1:i]:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                key, sep, value = line.partition(":")
                if sep:
                    meta[key.strip()] = re.sub(r"\s+#.*$", "", value).strip().strip("\"'")
            return meta, "\n".join(lines[i + 1:])
    return None, text


def headings(body):
    """Level-1 headings outside fenced code blocks."""
    fenced, found = False, []
    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"^# \S", line):
            found.append(line)
    return found


def check(root, today=None):
    today = today or dt.date.today()
    errors, warnings = [], []
    docs = pathlib.Path(root) / "docs"
    if not docs.is_dir():
        return [f"{docs}: no docs/ directory"], []
    for page in sorted(docs.rglob("*.md")):
        rel = page.relative_to(docs)
        name = str(page)
        if page.name == "README.md":
            continue
        folder = rel.parts[0] if len(rel.parts) > 1 else ""
        if folder not in FOLDER_TYPE and folder != DECISIONS:
            errors.append(f"{name}: a page lives in one of docs/{{{','.join([*FOLDER_TYPE, DECISIONS])}}}/")
            continue
        meta, body = front_matter(page.read_text())
        if meta is None:
            errors.append(f"{name}: missing front matter header")
            continue
        if len(headings(body)) != 1:
            errors.append(f"{name}: needs exactly one level-1 title")
        if folder == DECISIONS:
            if not DECISION_NAME.match(page.name):
                errors.append(f"{name}: decision files are named NNNN-short-title.md")
            if not STATUS.match(meta.get("status", "")):
                errors.append(f"{name}: status must be proposed, accepted, rejected, deprecated or superseded by ...")
            if not DATE.match(meta.get("date", "")):
                errors.append(f"{name}: date must be YYYY-MM-DD")
            if not meta.get("decision-makers"):
                errors.append(f"{name}: decision-makers is required")
            continue
        if meta.get("type") != FOLDER_TYPE[folder]:
            errors.append(f"{name}: type must be '{FOLDER_TYPE[folder]}' in docs/{folder}/ (found '{meta.get('type', '')}')")
        if not meta.get("audience"):
            errors.append(f"{name}: audience is required")
        verified = meta.get("verified", "")
        if verified:
            try:
                day = dt.date.fromisoformat(verified)
            except ValueError:
                errors.append(f"{name}: verified must be YYYY-MM-DD")
            else:
                if day > today:
                    errors.append(f"{name}: verified is in the future")
                elif (today - day).days > STALE_DAYS:
                    warnings.append(f"{name}: last verified {(today - day).days} days ago, check it again")
        elif FOLDER_TYPE[folder] in ("tutorial", "how-to"):
            errors.append(f"{name}: verified is required for a {FOLDER_TYPE[folder]}")
    return errors, warnings


def selftest():
    good = "---\ntype: how-to\naudience: operator\nverified: 2026-10-01\n---\n\n# Do it\n\n```\n# not a title\n```\n"
    adr = "---\nstatus: accepted\ndate: 2026-10-01\ndecision-makers: l-nmch\n---\n\n# Choose X\n"
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / "docs"
        (d / "how-to").mkdir(parents=True)
        (d / "decisions").mkdir()
        (d / "README.md").write_text("# index\n")
        (d / "how-to" / "a.md").write_text(good)
        (d / "decisions" / "0001-x.md").write_text(adr)
        errors, warnings = check(tmp, dt.date(2026, 10, 28))
        assert not errors and not warnings, (errors, warnings)
        (d / "how-to" / "b.md").write_text(good.replace("how-to", "reference"))
        (d / "how-to" / "c.md").write_text(good.replace("verified: 2026-10-01\n", ""))
        (d / "how-to" / "d.md").write_text("# no header\n")
        (d / "stray.md").write_text(good)
        (d / "decisions" / "bad.md").write_text(adr)
        (d / "how-to" / "e.md").write_text(good.replace("2026-10-01", "2026-01-01"))
        errors, warnings = check(tmp, dt.date(2026, 10, 28))
        joined = "\n".join(errors)
        for needle in ("b.md: type must be", "c.md: verified is required", "d.md: missing front matter",
                       "stray.md: a page lives in", "bad.md: decision files are named"):
            assert needle in joined, (needle, joined)
        assert any("e.md" in w for w in warnings), warnings
    print("ok")


def main():
    if sys.argv[1:] == ["selftest"]:
        selftest()
        return
    errors, warnings = check(sys.argv[1] if len(sys.argv) > 1 else ".")
    for w in warnings:
        print(f"::warning::{w}")
    for e in errors:
        print(f"::error::{e}")
    if errors:
        sys.exit(1)
    print("docs layout and headers ok")


if __name__ == "__main__":
    main()
