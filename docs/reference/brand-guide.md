---
type: reference
audience: contributor who writes text, builds an interface or makes a visual for Phorge
verified: 2026-11-05
---

# Brand guide

The visual identity of Phorge: how the name is written, the logo files, the colors with their contrast, the typeface and the positioning statement. The assets are in [brand/](../../brand/).

## Name

- In text (documentation, interface, legal notices, commit messages) the name is written **Phorge**.
- The φ is the logo and a monogram. It is not used as a letter in running text, because it is hard to type, to search for and to read with a screen reader.

## Logo

The logo is the φ mark, alone or followed by the letters "orge" (the wordmark).

| File | Use |
| --- | --- |
| [logo-wordmark-light.svg](../../brand/logo-wordmark-light.svg) | The wordmark on a light background |
| [logo-wordmark-dark.svg](../../brand/logo-wordmark-dark.svg) | The wordmark on a dark background |
| [logo-mark.svg](../../brand/logo-mark.svg) | The φ alone, where the width is small (avatar, icon) |

Rules:

- Use the variant that matches the background. Do not recolor the logo, stretch it, rotate it or add an effect.
- Do not set the name in another typeface to make a logo.
- Keep a clear space around the logo at least equal to the height of the letter o.

The letters of the wordmark are outlines of Source Sans 3 Regular, so the files need no font. The φ comes from the earlier logo, vectorized from its image; its redrawing is tracked in [#56](https://github.com/phorge-fr/.github/issues/56).

## Colors

The tokens are in [brand/tokens.css](../../brand/tokens.css). The light values are the default, the dark values follow the system, and `data-theme` on the root element forces one of them. The neutral colors come from the Phorge theme of Forgejo ([gitea-phorge-theme](https://github.com/phorge-fr/gitea-phorge-theme)).

The logo blue, `#39b5fb`, is 2.3:1 on white. It is used as a color for text, links and buttons on a dark background only; on a light background the interface uses the stronger blue.

### Light theme

| Token | Value | Use | Contrast |
| --- | --- | --- | --- |
| `--phorge-bg` | `#ffffff` | Page background | |
| `--phorge-surface` | `#f6f7fa` | Navigation, panels | |
| `--phorge-highlight` | `#ecf5fd` | Selected rows | |
| `--phorge-text` | `#181c21` | Body text | 17.1:1 on bg, 16.0:1 on surface |
| `--phorge-text-muted` | `#30363b` | Secondary text | 12.2:1 on bg, 11.1:1 on highlight |
| `--phorge-primary` | `#0475b5` | Links, button fill | 5.0:1 on bg, 4.7:1 on surface, 4.5:1 on highlight |
| `--phorge-on-primary` | `#ffffff` | Text on a primary fill | 5.0:1 on primary |
| `--phorge-accent` | `#0593e4` | Borders, icons, focus rings | 3.3:1 on bg, 3.1:1 on surface, 3.0:1 on highlight |
| `--phorge-wordmark-gray` | `#767676` | The letters "orge" | 4.5:1 on bg |

### Dark theme

| Token | Value | Use | Contrast |
| --- | --- | --- | --- |
| `--phorge-bg` | `#1b1f23` | Page background | |
| `--phorge-surface` | `#14171a` | Navigation, panels | |
| `--phorge-highlight` | `#1e2226` | Selected rows | |
| `--phorge-text` | `#d0d5da` | Body text | 11.2:1 on bg, 12.2:1 on surface |
| `--phorge-text-muted` | `#bcc3cb` | Secondary text | 9.3:1 on bg, 9.0:1 on highlight |
| `--phorge-primary` | `#39b5fb` | Links, button fill | 7.2:1 on bg, 7.9:1 on surface, 7.0:1 on highlight |
| `--phorge-on-primary` | `#01050a` | Text on a primary fill | 8.9:1 on primary |
| `--phorge-accent` | `#39b5fb` | Borders, icons, focus rings | 7.2:1 on bg |
| `--phorge-wordmark-gray` | `#a6a6a6` | The letters "orge" | 6.8:1 on bg |

Ratios are the WCAG 2 contrast ratio, computed from the hex values and rounded to one decimal. Body text needs 4.5:1 and large text, icons and borders need 3:1. The text of a logo has no minimum, and the wordmark gray still meets 4.5:1 on white.

## Typography

- **Typeface:** Source Sans 3, weights 400, 600 and 700, for the interface, the showcase site and the documents.
- **License:** SIL Open Font License 1.1, copyright Adobe. Get the files from the [upstream repository](https://github.com/adobe-fonts/source-sans).
- **Hosting:** the font files are served by Phorge itself. No page loads a font from a third-party host (see the [GDPR notes](https://github.com/phorge-fr/Hangar/blob/main/docs/reference/gdpr-personal-data.md)).
- **Code and identifiers:** the system monospace font stack. No monospace file is hosted.

## Positioning

Phorge is an open-source cloud provider where every line of configuration, automation and infrastructure logic is visible, auditable and open to contribution.

| Message | Meaning |
| --- | --- |
| Transparent | Everything is public, from the network to the console. There are no black boxes. |
| Auditable | Anyone can read how the platform is built and check it. |
| Self-hostable | The deployment is reproducible: anyone can re-create the system. |
| Minimal | Low power consumption and minimal configuration over cleverness. |

The messages come from the [organization profile](https://github.com/phorge-fr/.github/blob/main/profile/README.md).

## License

The assets in `brand/` are under the [Apache License 2.0](../../LICENSE), like the rest of this repository. That license grants no right to use the Phorge name or logo as a trademark (section 6). The wordmark letters are derived from Source Sans 3, under the SIL Open Font License 1.1.
