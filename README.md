# Shopify App Design skill

An agent skill that grounds AI coding agents in Shopify's own app design documentation, so they design, build, and
review Shopify app UI the way Shopify expects — instead of guessing from training data.

It covers the [App Design Guidelines](https://shopify.dev/docs/apps/design), Polaris web components and App Bridge for
App Home, App Home page templates and compositions, UX guidelines for checkout, customer accounts, and theme app
extensions, the Built for Shopify and App Store requirements, accessibility, and migrating from Polaris React.

> **Unofficial.** This project isn't affiliated with or endorsed by Shopify. The documentation it downloads belongs to
> Shopify Inc. and isn't included in this repository.

## What the agent can do with it

- **Answer design questions** from the source: "Should a failed sync be a toast or a banner?", "How many items fit in
  the app nav?"
- **Design a page or component** starting from Shopify's templates (homepage, index, details, settings) and
  compositions (setup guide, metrics card, index table…).
- **Review an app UI** against a checklist built from the Built for Shopify design requirements, citing the exact rule
  behind each finding.
- **Write merchant-facing copy** that follows Shopify's voice, tone, and grammar guidelines.
- **Migrate from `@shopify/polaris`** using one mapping page per React component.

## Install

With the `skills` CLI (works with Claude Code, Cursor, GitHub Copilot, Codex, and other agents that support skills):

```bash
npx skills add ahmed-m-hussain/Shopify-App-Design-Skill        # current project
npx skills add ahmed-m-hussain/Shopify-App-Design-Skill -g     # all projects
```

Or clone it into your agent's skills folder:

```bash
git clone https://github.com/ahmed-m-hussain/Shopify-App-Design-Skill.git shopify-app-design-skill
```

## First run: download the documentation

The skill needs a local copy of the docs. Run this once from the skill folder (Python 3.9+, no dependencies, about
30 seconds):

```bash
python scripts/update_mirror.py
```

If you skip this step, the agent will run it the first time it uses the skill. Run it again whenever you want the
latest version of Shopify's docs.

The script reads the live shopify.dev sitemap, downloads about 230 pages through Shopify's official markdown exports,
and builds the indexes the agent uses to find the right page quickly.

## What gets downloaded

| Folder | Contents |
|---|---|
| `references/guidelines/` | App Design Guidelines: structure, navigation, layout, visual design, content, alerts, onboarding, forms |
| `references/components/` | Polaris web components (`s-*`) and App Bridge components (app nav, title bar, save bar, app window) |
| `references/patterns/` | App Home templates and compositions, with example markup |
| `references/interactions/` | App Bridge APIs: toast, modal, save bar, resource picker, navigation… |
| `references/surfaces/` | UX guidelines for checkout, customer accounts, theme app extensions, discounts, subscriptions |
| `references/requirements/` | Built for Shopify, App Store requirements, accessibility, privacy |
| `references/migration/` | Polaris React to Polaris web components |
| `references/getting-started/` | App Home, Polaris, using web components, Polaris 2.0, versioning |

`references/review-checklist.md` is the only reference file in this repository. It's a hand-written summary of the
Built for Shopify design checks, and every item points to the Shopify page it comes from.

## Repository layout

```
SKILL.md                      instructions the agent reads
scripts/update_mirror.py      downloads the docs and builds the indexes
references/review-checklist.md
```

## License

The skill's own files (`SKILL.md`, `scripts/`, `references/review-checklist.md`, and this README) are released under
the [MIT License](LICENSE). Downloaded Shopify documentation remains subject to Shopify's terms. See [NOTICE](NOTICE).
