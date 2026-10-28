#!/usr/bin/env python3
"""Report open issues that are probably finished, or whose tracking is inconsistent.

    issue_hygiene.py report ORG [--post REPO#N]    print the report (and post it as a comment)
    issue_hygiene.py siblings REPO#N [REPO#N ...]  open sub-issues next to the given issues (run before a pull request)
    issue_hygiene.py selftest

Three findings, each a question for a person, never an automatic close:
  epic-done        an open issue whose sub-issues are all closed
  siblings-done    an open sub-issue whose siblings are all closed
  referenced       an open issue named by a merged pull request without a closing keyword,
                   and by no open pull request
"""
import json
import re
import subprocess
import sys

CLOSING = r"(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)"
SOFT = r"(?:part of|refs?|related to)"
REF = re.compile(rf"\b(?P<kw>{CLOSING}|{SOFT})[: ]+(?:(?P<repo>[\w.-]+/[\w.-]+))?#(?P<num>\d+)", re.I)


def gh(*args):
    out = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if out.returncode:
        return None
    return json.loads(out.stdout) if out.stdout.strip() else None


def refs(body, default_repo):
    """[(repo, number, closing)] named in a pull request description."""
    found = []
    for m in REF.finditer(body or ""):
        closing = re.fullmatch(CLOSING, m["kw"], re.I) is not None
        found.append((m["repo"] or default_repo, int(m["num"]), closing))
    return found


def collect(org):
    repos = [r["full_name"] for r in gh(f"orgs/{org}/repos?per_page=100&type=public") if not r["fork"] and not r["archived"]]
    issues, merged, opened = {}, {}, {}
    for repo in repos:
        for i in gh(f"repos/{repo}/issues?state=open&per_page=100") or []:
            if "pull_request" not in i:
                issues[(repo, i["number"])] = i
        for pr in gh(f"repos/{repo}/pulls?state=closed&per_page=60") or []:
            if pr.get("merged_at"):
                for r, n, closing in refs(pr["body"], repo):
                    merged.setdefault((r, n), []).append((repo, pr["number"], closing, pr["merged_at"]))
        for pr in gh(f"repos/{repo}/pulls?state=open&per_page=100") or []:
            for r, n, _ in refs(pr["body"], repo):
                opened.setdefault((r, n), []).append((repo, pr["number"]))
    return issues, merged, opened


def findings(issues, merged, opened, subs, parents):
    """subs[(repo,n)] = [(repo,n,state)], parents[(repo,n)] = (repo,n) or None."""
    out = []
    for key, issue in sorted(issues.items()):
        label = f"{key[0]}#{key[1]} {issue['title']}"
        children = subs.get(key, [])
        if children and all(s == "closed" for _, _, s in children):
            out.append(("epic-done", label, f"all {len(children)} sub-issues are closed: close it, or add what is left"))
        parent = parents.get(key)
        if parent:
            siblings = [c for c in subs.get(parent, []) if (c[0], c[1]) != key]
            if siblings and all(s == "closed" for _, _, s in siblings):
                out.append(("siblings-done", label, f"all its siblings under {parent[0]}#{parent[1]} are closed"))
        soft = [(r, n) for r, n, closing, _ in merged.get(key, []) if not closing]
        if soft and not any(closing for _, _, closing, _ in merged.get(key, [])) and not opened.get(key):
            out.append(("referenced", label, "named without a closing keyword by merged " + ", ".join(f"{r}#{n}" for r, n in soft[:3])))
    return out


def siblings(keys):
    """Lines naming, for each issue, the other open sub-issues under its parent epic."""
    lines = []
    for key in keys:
        repo, num = key.split("#")
        parent = gh(f"repos/{repo}/issues/{num}/parent")
        if not parent:
            continue
        prepo = parent["repository"]["full_name"]
        open_ones = [s for s in gh(f"repos/{prepo}/issues/{parent['number']}/sub_issues?per_page=100") or []
                     if s["state"] == "open" and (s["repository"]["full_name"], s["number"]) != (repo, int(num))]
        if open_ones:
            lines.append(f"{key} is under {prepo}#{parent['number']} ({parent['title']}). Other open sub-issues, does this change finish one? "
                         + "; ".join(f"{s['repository']['full_name']}#{s['number']} {s['title']}" for s in open_ones))
    return lines


def report(org):
    issues, merged, opened = collect(org)
    subs, parents = {}, {}
    for (repo, n), issue in issues.items():
        if issue.get("sub_issues_summary", {}).get("total"):
            subs[(repo, n)] = [(s["repository"]["full_name"], s["number"], s["state"]) for s in gh(f"repos/{repo}/issues/{n}/sub_issues?per_page=100") or []]
        if (p := gh(f"repos/{repo}/issues/{n}/parent")):
            parents[(repo, n)] = (p["repository"]["full_name"], p["number"])
    for parent in set(parents.values()):
        if parent not in subs:
            subs[parent] = [(s["repository"]["full_name"], s["number"], s["state"]) for s in gh(f"repos/{parent[0]}/issues/{parent[1]}/sub_issues?per_page=100") or []]
    found = findings(issues, merged, opened, subs, parents)
    if not found:
        return "No open issue looks finished or inconsistently tracked."
    lines = ["Open issues that probably need a decision (each is a question, nothing is closed automatically):", ""]
    for kind, label, why in found:
        lines.append(f"- **{kind}** {label}: {why}")
    return "\n".join(lines)


def selftest():
    assert refs("Closes #3 and part of phorge-fr/.github#17, fixes phorge-fr/Hangar#9", "o/r") == [("o/r", 3, True), ("phorge-fr/.github", 17, False), ("phorge-fr/Hangar", 9, True)]
    assert refs("nothing here", "o/r") == [] and refs(None, "o/r") == []
    issues = {("o/r", 30): {"title": "madr"}, ("o/r", 27): {"title": "epic"}, ("o/r", 5): {"title": "open, referenced"}}
    subs = {("o/r", 27): [("o/r", 28, "closed"), ("o/r", 30, "open")]}
    parents = {("o/r", 30): ("o/r", 27)}
    merged = {("o/r", 5): [("o/r", 9, False, "2026-10-01T00:00:00Z")]}
    got = {(k, l.split()[0]) for k, l, _ in findings(issues, merged, {}, subs, parents)}
    assert got == {("siblings-done", "o/r#30"), ("referenced", "o/r#5")}, got
    assert findings(issues, merged, {("o/r", 5): [("o/r", 11)]}, subs, parents)[0][0] == "siblings-done"
    print("ok")


def main():
    if sys.argv[1:] == ["selftest"]:
        return selftest()
    if sys.argv[1:2] == ["siblings"]:
        print("\n".join(siblings(sys.argv[2:])) or "No open sibling sub-issues.")
        return
    if len(sys.argv) < 3 or sys.argv[1] != "report":
        sys.exit(__doc__)
    text = report(sys.argv[2])
    print(text)
    if "--post" in sys.argv:
        repo, num = sys.argv[sys.argv.index("--post") + 1].split("#")
        subprocess.run(["gh", "api", "-X", "POST", f"repos/{repo}/issues/{num}/comments", "-f", f"body={text}"], check=True, capture_output=True)


if __name__ == "__main__":
    main()
