#!/usr/bin/env python3
"""Time tracking from `/time` comments (see GOVERNANCE.md).

  time_tracking.py total   OWNER/REPO NUMBER        print the hours logged on an issue or pull request
  time_tracking.py project OWNER/REPO NUMBER        write that total to the `Spent (h)` field of its project items
  time_tracking.py sync-all ORG                     recompute `Spent (h)` for every item that has time entries
  time_tracking.py selftest                         check the `/time` parser
  time_tracking.py report  ORG [--since D] [--until D] [--out FILE]   markdown report (default: the last 7 days)

Needs the `gh` CLI. `project` and `sync-all` need a token with project write access.
Standard library only.
"""
import argparse
import collections
import datetime as dt
import json
import re
import subprocess
import sys

FIELD = "Spent (h)"
ENTRY = re.compile(
    r"^/time\s+(?:(\d+)h(?:\s*(\d+)m?)?|(\d+)m)\b(?:\s+@(\d{4}-\d{2}-\d{2}))?\s*(.*)$"
)


def gh(*args, paginate=False, input_=None):
    cmd = ["gh", "api", *args]
    if paginate:
        cmd.insert(2, "--paginate")
    out = subprocess.run(cmd, check=True, capture_output=True, text=True, input=input_).stdout
    if paginate:  # --paginate concatenates JSON arrays: "[..][..]"
        dec, i, items = json.JSONDecoder(), 0, []
        while i < len(out):
            if out[i].isspace():
                i += 1
                continue
            obj, i = dec.raw_decode(out, i)
            items.extend(obj if isinstance(obj, list) else [obj])
        return items
    return json.loads(out) if out.strip() else None


def parse_entries(body, created_at):
    """Yield (minutes, date, text) for each `/time` line outside code fences."""
    fenced = False
    for line in (body or "").splitlines():
        line = line.strip()
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = ENTRY.match(line)
        if not m:
            continue
        h, mm, only_m, date, text = m.groups()
        minutes = int(h or 0) * 60 + int(mm or 0) + int(only_m or 0)
        if minutes:
            yield minutes, date or created_at[:10], text.strip()


def comments_of(repo, number):
    return gh(f"repos/{repo}/issues/{number}/comments?per_page=100", paginate=True)


def item_minutes(repo, number):
    return sum(
        m for c in comments_of(repo, number) for m, _, _ in parse_entries(c["body"], c["created_at"])
    )


def fmt(minutes):
    return f"{minutes / 60:.2f}".rstrip("0").rstrip(".")


QUERY = """
query($id: ID!) { node(id: $id) {
  ... on Issue { projectItems(first: 20) { nodes { id project { id title } } } }
  ... on PullRequest { projectItems(first: 20) { nodes { id project { id title } } } }
} }"""
FIELDS = """
query($id: ID!) { node(id: $id) { ... on ProjectV2 {
  field(name: "%s") { ... on ProjectV2Field { id dataType } } } } }""" % FIELD
SET = """
mutation($p: ID!, $i: ID!, $f: ID!, $v: Float!) { updateProjectV2ItemFieldValue(input:
  {projectId: $p, itemId: $i, fieldId: $f, value: {number: $v}}) { projectV2Item { id } } }"""


def graphql(query, **variables):
    args = ["graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, float) else "-f", f"{k}={v}"]
    return gh(*args)["data"]


def node_id(repo, number):
    issue = gh(f"repos/{repo}/issues/{number}")
    if "pull_request" in issue:  # the issues endpoint returns an Issue node for a PR
        return gh(f"repos/{repo}/pulls/{number}")["node_id"]
    return issue["node_id"]


def set_spent(repo, number, minutes):
    done = 0
    items = graphql(QUERY, id=node_id(repo, number))["node"]["projectItems"]["nodes"]
    for it in items:
        field = graphql(FIELDS, id=it["project"]["id"])["node"]["field"]
        if not field or field.get("dataType") != "NUMBER":
            print(f"warning: project {it['project']['title']!r} has no Number field {FIELD!r}", file=sys.stderr)
            continue
        graphql(SET, p=it["project"]["id"], i=it["id"], f=field["id"], v=round(minutes / 60, 2))
        done += 1
    return done


def org_repos(org):
    repos = gh(f"orgs/{org}/repos?per_page=100&type=public", paginate=True)
    return sorted(r["full_name"] for r in repos if not r["archived"])


def all_entries(org, since):
    """Yield dicts for every time entry on an org issue/PR comment created since `since` (ISO date)."""
    for repo in org_repos(org):
        for c in gh(f"repos/{repo}/issues/comments?per_page=100&since={since}T00:00:00Z", paginate=True):
            if c["created_at"][:10] < since:
                continue
            number = int(c["issue_url"].rsplit("/", 1)[1])
            for minutes, date, text in parse_entries(c["body"], c["created_at"]):
                yield dict(repo=repo, number=number, user=c["user"]["login"], minutes=minutes, date=date, text=text)


def cmd_report(args):
    until = args.until or dt.date.today().isoformat()
    since = args.since or (dt.date.fromisoformat(until) - dt.timedelta(days=6)).isoformat()
    entries = [e for e in all_entries(args.org, since) if since <= e["date"] <= until]
    meta = {}

    def info(repo, number):
        if (repo, number) not in meta:
            i = gh(f"repos/{repo}/issues/{number}")
            kind = "PR" if "pull_request" in i else ((i.get("type") or {}).get("name") or "Issue")
            meta[(repo, number)] = (kind, i["title"])
        return meta[(repo, number)]

    total = sum(e["minutes"] for e in entries)
    by_item, by_user, by_day = (collections.Counter() for _ in range(3))
    for e in entries:
        by_item[(e["repo"], e["number"])] += e["minutes"]
        by_user[e["user"]] += e["minutes"]
        by_day[e["date"]] += e["minutes"]
    lines = [f"# Time report {since} to {until}", "", f"Total: **{fmt(total)} h** in {len(entries)} entries.", ""]
    lines += ["## By author", "", "| Author | Hours |", "| --- | ---: |"]
    lines += [f"| @{u} | {fmt(m)} |" for u, m in by_user.most_common()]
    lines += ["", "## By day", "", "| Day | Hours |", "| --- | ---: |"]
    lines += [f"| {d} | {fmt(m)} |" for d, m in sorted(by_day.items())]
    lines += ["", "## By issue and pull request", "", "| Item | Kind | Title | Hours |", "| --- | --- | --- | ---: |"]
    for (repo, number), m in by_item.most_common():
        kind, title = info(repo, number)
        lines.append(f"| [{repo}#{number}](https://github.com/{repo}/issues/{number}) | {kind} | {title.replace('|', '/')} | {fmt(m)} |")
    text = "\n".join(lines) + "\n"
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
    else:
        print(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("total", "project"):
        p = sub.add_parser(name)
        p.add_argument("repo")
        p.add_argument("number", type=int)
    p = sub.add_parser("sync-all")
    p.add_argument("org")
    sub.add_parser("selftest")
    p = sub.add_parser("report")
    p.add_argument("org")
    p.add_argument("--since")
    p.add_argument("--until")
    p.add_argument("--out")
    args = ap.parse_args()

    if args.cmd == "selftest":
        body = "/time 1h30 a\n/time 45m\n```\n/time 9h\n```\n> /time 1h\n/time 1h 15m @2026-10-27 b\n/time 2h text"
        got = [(m, d) for m, d, _ in parse_entries(body, "2026-10-28T00:00:00Z")]
        assert got == [(90, "2026-10-28"), (45, "2026-10-28"), (75, "2026-10-27"), (120, "2026-10-28")], got
        print("ok")
    elif args.cmd == "total":
        print(fmt(item_minutes(args.repo, args.number)))
    elif args.cmd == "project":
        minutes = item_minutes(args.repo, args.number)
        print(f"{args.repo}#{args.number}: {fmt(minutes)} h on {set_spent(args.repo, args.number, minutes)} project item(s)")
    elif args.cmd == "sync-all":
        totals = collections.Counter()
        for e in all_entries(args.org, "2000-01-01"):
            totals[(e["repo"], e["number"])] += e["minutes"]
        for (repo, number), minutes in sorted(totals.items()):
            print(f"{repo}#{number}: {fmt(minutes)} h on {set_spent(repo, number, minutes)} project item(s)")
    else:
        cmd_report(args)


if __name__ == "__main__":
    main()
