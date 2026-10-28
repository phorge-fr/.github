# Security policy

## Reporting a vulnerability

Please **do not open a public issue** for a security problem.

Report it privately, with either:

- the **"Report a vulnerability"** button in the *Security* tab of the affected repository (GitHub private security advisories), or
- an e-mail to `contact@phorge.fr` with `[security]` in the subject.

Include what you found, where, how to reproduce it, and the impact you see. Do not include real secrets or other people's data.

You can expect an acknowledgement within **5 working days** and a first assessment within **15**. We will keep you informed, credit
you if you wish once the fix is out, and publish a sanitized advisory afterwards. Please give us a reasonable time to fix before
disclosing.

## Scope

In scope: the code, configuration and documentation in the `phorge-fr` repositories, and the Phorge services we operate
(`*.phorge.fr`). Out of scope: denial of service, social engineering, physical attacks, and third-party software that has its
own project (report it upstream; tell us if our configuration makes it worse).

Please do not run automated scanners against production without asking first.

## How we handle findings

Phorge is public and transparent, so audit **scope, method and status** are public issues. Raw findings (live addresses,
exploitable details) are kept in private advisories or git-ignored `reports/` folders until they are fixed, then published
sanitized. Never commit a real weakness to a public repository.

## Supported versions

The project is pre-1.0 and rolling: only the latest `main` and the latest release of each component are supported.
