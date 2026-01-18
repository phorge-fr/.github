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

| Project                                                                             | Description                                                                            |
| ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **[FrontPlane](https://github.com/phorge-fr/FrontPlane)**                           | Main Kubernetes cluster hosting every services required for the infrastructure to run    |
| **[Ansible](https://github.com/phorge-fr/Ansible)**                                 | Infrastructure automation and base system provisioning                                 |
| **[Network](https://github.com/phorge-fr/Network)**                                 | Network design, configuration and tooling for routing, isolation, and service exposure |

## Other repositories

This Github organization hosts the main repository used to deploy the necessary components to run Phorge.

All other repositories used to run, build, or host apps can be found on [Phorge's Gitea](https://git.phorge.fr)

## Contact

Feel free to contact me by email: `contact@phorge.fr`
