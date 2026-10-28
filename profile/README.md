# Welcome to φorge

Transparent, Open-Source Cloud Infrastructure

![Phorge logo](https://avatars.githubusercontent.com/u/187407936?s=200&v=4)

φorge (or phorge) is an open-source cloud provider initiative led by @l-nmch.

We aim to build a complete, transparent, and self-hostable cloud platform — from the network layer to the orchestration and user interface, powered by modern open technologies like Kubernetes and Incus.

Our mission is simple:

> Provide a cloud where every line of configuration, automation, and infrastructure logic is visible, auditable, and open to contribution.

# Philosophy

- Fully open infrastructure — no black boxes, no secret layers

- Reproducible deployment — anyone can re-create the system

- Community-driven evolution — transparency by default

- Modern cloud foundation — Kubernetes, Incus, automation, observability

- Stay minimalist - From Power consumption to configuration, Let's keep things simple !

This is an early-stage project, but the foundation is in place. The ambition is long-term.

# Core Components

| Project | Description |
| --- | --- |
| **[Hangar](https://github.com/phorge-fr/Hangar)** | GitOps (FluxCD) for the three Kubernetes clusters: manifests, Crossplane compositions, docs |
| **[Network](https://github.com/phorge-fr/Network)** | Router configuration as code (OpenTofu): VLANs, firewall, DNS, edge proxy |
| **[Ansible](https://github.com/phorge-fr/Ansible)** | Provisioning of everything that is not Kubernetes: storage, HPC/GPU and compute nodes |
| **[phorge-api](https://github.com/phorge-fr/phorge-api)** | The Phorge API: tenants, images, instances, memberships and API keys |
| **[Gitea-Phorge-Theme](https://github.com/phorge-fr/gitea-phorge-theme)** | Simple Gitea theme to match Phorge's design and colors |

The Crossplane providers (`provider-incus`, `provider-openfga`, `provider-authentik`) currently live under
[@l-nmch](https://github.com/l-nmch) and are planned to move here.

# Roadmap and how we work

Everything we do is a public issue in a public [GitHub Project](https://github.com/orgs/phorge-fr/projects):
the **Roadmap** (epics by quarter), **Platform**, **Cloud API & Providers**, **Security & Compliance** and **Community & Brand**.
Each issue has a type, a priority, an estimate and the time spent. Read [GOVERNANCE.md](https://github.com/phorge-fr/.github/blob/main/GOVERNANCE.md).

# Contribute

- [Contributing guide](https://github.com/phorge-fr/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/phorge-fr/.github/blob/main/CODE_OF_CONDUCT.md)
- [Security policy](https://github.com/phorge-fr/.github/blob/main/SECURITY.md): report vulnerabilities privately
- New here, or an AI agent? Start with [AGENTS.md](https://github.com/phorge-fr/.github/blob/main/AGENTS.md)

## Contact

Feel free to contact us by email: `contact@phorge.fr`
