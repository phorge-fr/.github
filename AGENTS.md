# Phorge: onboarding for humans and coding agents

This file is the entry point for anyone (a person or an AI agent) who works on a repository of the
[`phorge-fr`](https://github.com/phorge-fr) organization. It is tool-agnostic. Each repository has its own `AGENTS.md`
with the details of that repository; read this one first, then that one.

Phorge is an open-source cloud provider initiative: a transparent, auditable, self-hostable platform from the network to the
console, built on Kubernetes, Crossplane and Incus. Everything is public, so write every file, issue and comment as if a
stranger will read it.

## Repositories

| Repository | Role |
| --- | --- |
| [Hangar](https://github.com/phorge-fr/Hangar) | FluxCD GitOps for the three k0s clusters (`control`, `core`, `svc`): manifests, Crossplane XRDs and compositions, the OpenFGA model, docs. |
| [Network](https://github.com/phorge-fr/Network) | OpenTofu for the MikroTik router: VLANs, firewall, DNS, NAT, the edge HAProxy. |
| [Ansible](https://github.com/phorge-fr/Ansible) | Everything that is not Kubernetes: the storage node, HPC/GPU nodes, Incus compute nodes. |
| [phorge-api](https://github.com/phorge-fr/phorge-api) | The Go REST API that creates `phorge.fr/v1alpha1` objects (Tenant, Image, Instance, Membership, ApiKey) on the `control` cluster. |
| [.github](https://github.com/phorge-fr/.github) | This repository: organization profile, community files, shared workflows, org-wide epics. |
| [gitea-phorge-theme](https://github.com/phorge-fr/gitea-phorge-theme) | Theme for Gitea/Forgejo. |

The Crossplane providers (`provider-incus`, `provider-openfga`, `provider-authentik`) still live under a personal account and
are not yet part of the organization. Their migration is planned and tracked on the roadmap.

### How they depend on each other

The clusters rely on infrastructure the other repositories own. A change often spans several repositories:

- A new network flow between a cluster and anything outside it needs a matching `accept` rule in **Network**; the router is
  default-deny between workload VLANs and a missing rule shows up as a silent timeout.
- Storage (NFS, S3-compatible object storage) is provisioned by **Ansible** and consumed by **Hangar**.
- The API (**phorge-api**) only creates objects; the XRDs, compositions, RBAC and OpenFGA model that give them meaning are in
  **Hangar**. A platform change needed by the API is a Hangar pull request, never an edit on a live cluster.

Before closing a cross-cutting issue, check that each repository concerned has its part.

## How work is tracked

Read [GOVERNANCE.md](GOVERNANCE.md) for the full rules. In short:

1. **Every topic is an issue**, in the repository it changes. Cross-repository topics are an `Epic` in this repository with
   sub-issues in the others.
2. An issue has exactly one **type** (Epic, Feature, Task, Bug, Chore, Security, Docs), one `area/*` label, a **priority**
   (P0 to P3) and an **estimate in hours** (project fields), an assignee, a milestone and a project.
3. Work happens on a **branch** (`feat/...`, `fix/...`, `docs/...`, `chore/...`) and reaches `main` through a **pull request**
   that references its issue (`Closes #N`). Nobody pushes to `main`. Renovate, Dependabot and release-please pull requests are exempt
   from the issue requirement.
4. **Time** is logged in a comment, `/time 1h30 what was done`, on the issue or the pull request.
5. Issues, pull requests, commits and code comments are written in **English**.
6. Roadmaps are public GitHub Projects, listed in the [organization profile](profile/README.md).

## Rules that apply everywhere

- **No secret in git, ever.** Not in a commit, an issue, a log or a screenshot. Secrets are encrypted (SOPS+age in Hangar,
  Ansible Vault in Ansible) or come from the environment. If one leaks, treat it as compromised and rotate it.
- **No exploitable weakness in a public place.** Security audit and pentest findings, live IPs, MAC addresses and the like go to a
  private [security advisory](SECURITY.md) or a git-ignored `reports/` folder, and are published sanitized once fixed. Public issues
  describe scope, method and status only.
- **Use the repository's own tool.** Flux for Kubernetes, `tofu` for the router, Ansible for hosts, `k0sctl` for the clusters.
  Do not replace them with ad-hoc SSH or `kubectl edit`; Flux reverts live edits anyway. Test against real infrastructure by
  following each repository's documented procedure.
- **Every new workload ships its network policy** in the same pull request (the clusters are default-deny).
- **Ask before anything shared or hard to reverse**: merging to `main`, `tofu apply`, force pushes, deleting data, changing
  production credentials. A pull request is the place to ask.
- **Be honest in reports**: say what was tested and how, what failed, and what was skipped.
- Keep it simple. Phorge values minimal configuration and low power consumption over cleverness.

## For AI agents specifically

- Read the `AGENTS.md` of the repository you are in, and the docs it points to, before changing anything.
- Prefer small pull requests, one issue each. Open an issue for any finding that is not fixed in the current change instead of
  leaving a remark in a comment or a chat.
- Log your own working time with `/time` like any contributor.
- Do not invent facts about the infrastructure; check the repository or the live state. If something is missing or ambiguous
  (host names, who may do what), ask.
- Do not add tool or vendor attribution to commits and pull requests unless the maintainers of the repository ask for it.
- On your own branch you may commit, push and open the pull request without asking. **Merging into `main` waits for the maintainer** (a merge in Hangar is a deployment), and so does anything applied to production by hand-run tools (`tofu apply`, `k0sctl apply`). You may write issues and comments freely, following [GOVERNANCE.md](GOVERNANCE.md); deleting a project or closing an epic is the maintainers' call.
- Never delete files you did not create in the session; report their path instead.
- Close issues through `Closes #N` in the pull request, and open a new issue for any leftover *before* the pull request.

## Contact

Maintainer: [@l-nmch](https://github.com/l-nmch). General contact: `contact@phorge.fr`. Vulnerabilities: see [SECURITY.md](SECURITY.md).
