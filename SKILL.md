---
name: shopify-app-design-skill
description: Provides Shopify's App Design Guidelines and Polaris for designing, building, and reviewing Shopify app UI/UX in the Shopify admin (App Home, admin UI extensions), checkout, customer accounts, and the online store. Covers app structure, navigation, layout, visual design, content and voice, alerts, onboarding, forms and the save bar; Polaris web components (s-page, s-section, s-button, s-table, s-modal, fields); App Bridge (s-app-nav, s-app-window, ui-save-bar, toast, resource picker); App Home templates and compositions; Built for Shopify and App Store requirements with rejection reasons; accessibility; and migrating from Polaris React. Use whenever the user designs, builds, or reviews UI for a Shopify app, picks Polaris components, asks what Shopify recommends for an interaction or visual element, prepares for Built for Shopify review, writes merchant-facing copy, or migrates from @shopify/polaris — even without saying "Polaris" explicitly.
metadata:
  content-source: "shopify.dev markdown exports (App Design Guidelines, App Home / Polaris reference, Built for Shopify requirements)"
  content-owner: "Shopify Inc."
---

# Shopify App Design (App Design Guidelines + Polaris)

This skill works from a local mirror of Shopify's app design documentation under `references/`, built from the official
markdown exports on shopify.dev (every page is available at `<url>.md`). It is an unofficial copy; all content belongs
to Shopify Inc. Ground answers in these files rather than general or training knowledge: Shopify's guidance is
specific, changes often (Polaris moved from React to web components, and Polaris 2.0 restyles the admin), and Built
for Shopify reviews cite exact rules.

## First-time setup

The mirrored documentation isn't distributed with the skill. If `references/topic-index.md` doesn't exist, build the
mirror before answering (Python 3.9+, standard library only, about 30 seconds):

```
python scripts/update_mirror.py
```

Run it from the skill's own folder. If the command can't run (no Python or no network), tell the user and fall back to
the live pages on shopify.dev (each page is also available as markdown at `<url>.md`), saying clearly that the answer
isn't grounded in the local mirror.

## Coverage

Eight sections are mirrored under `references/`:

| Section | Path | Covers |
|---|---|---|
| Getting started | `references/getting-started/` | App Home (iframe model vs. App Home UI extension), Polaris overview, using Polaris web components (properties, events, slots, responsive values, styling), Polaris 2.0, versioning |
| App Design Guidelines | `references/guidelines/` | The core guidelines: app structure, navigation, layout, visual design, content (voice and tone, grammar and mechanics), messages and feedback (alerts), App Home and onboarding, forms and saving |
| Components | `references/components/` | Polaris web components for App Home in 7 categories (actions, feedback and status indicators, forms, layout and structure, media and visuals, overlays, typography and content) plus App Bridge web components (app nav, title bar, save bar, app window) |
| Patterns | `references/patterns/` | App Home **templates** (homepage, resource index, details, settings) and **compositions** (account connection, app card, callout card, footer help, index table, interstitial nav, media card, metrics card, resource list, setup guide), each with full example markup |
| Interactions | `references/interactions/` | App Bridge UI APIs: toast, modal, save bar, loading, navigation, resource picker, picker, intents, reviews, support, sidekick, tools |
| Surfaces | `references/surfaces/` | UX guidelines outside App Home: checkout (fields, payments, delivery, pickup points, product offers, chat, announcement bar), customer accounts, theme app extensions and theme design/accessibility, discounts, subscriptions and preorder/try-before-you-buy |
| Requirements | `references/requirements/` | Built for Shopify overview and requirements (design section §4 lists concrete rejection reasons), App Store requirements, accessibility best practices, privacy requirements |
| Migration | `references/migration/` | Polaris React (`@shopify/polaris`) → Polaris web components: process overview plus one mapping page per React component (Card, DataTable, IndexTable, Modal, Page, Toast, TopBar, …) |

Every section has an `index.md` landing page. **Components, Patterns, and Surfaces have an extra nesting level** — their
`index.md` lists category folders, each with its own `index.md` plus the articles. The other sections are flat.

`references/review-checklist.md` is the one hand-written file: a condensed review checklist derived from the Built for
Shopify design requirements and the guidelines, with the source of every check. It's a lookup aid, not a source.

### Key concepts

- **App Home** — the app's main page inside the Shopify admin, rendered in an iframe. One frontend serves desktop and
  the Shopify mobile app. See `getting-started/app-home.md`.
- **Polaris web components** — the current Polaris: framework-agnostic custom elements prefixed `s-` (`<s-page>`,
  `<s-section>`, `<s-button>`), loaded from Shopify's CDN. They render in shadow DOM, so app CSS can't restyle their
  internals. Polaris React (`@shopify/polaris`) is the legacy library — see `references/migration/`.
- **App Bridge** — the SDK that controls the admin chrome *around* the iframe: `<s-app-nav>` (sidebar nav), the title
  bar (`<s-page>` heading/actions/breadcrumbs), `<ui-save-bar>` / `data-save-bar` (contextual save bar),
  `<s-app-window>` (full-screen), and APIs such as `shopify.toast.show()`. App Bridge isn't versioned with Polaris.
- **Admin UI extensions** — admin blocks, admin actions, admin links, and bulk actions that place app UI on native admin
  pages. Design rules live in `guidelines/app-structure.md`.
- **Built for Shopify (BFS)** — Shopify's quality badge. `requirements/built-for-shopify-requirements.md` §4 (Design)
  turns the guidelines into pass/fail checks with "reasons for rejection".

## Finding the right article

1. **Fast path**: grep `references/topic-index.md` — a flattened list of every article with its path, one-line
   description, component tag, and source URL slug. Search by tag, React component name, topic, or synonym:
   ```
   grep -i "s-modal\|modal" references/topic-index.md
   grep -i "save bar" references/topic-index.md
   grep -i "DataTable" references/topic-index.md
   ```
2. **Following a shopify.dev link inside an article**: mirrored articles keep absolute shopify.dev links. Grep
   `topic-index.md` for the last one or two URL segments (for example `layout-and-structure/section` or
   `templates/homepage`) to find the local copy. Links appear in several equivalent forms —
   `/docs/api/app-home/web-components/…`, `/docs/api/app-home/latest/web-components/…`, and
   `/docs/api/app-home/polaris-web-components/…` all point to the same component page. Links to pages that aren't in
   the mirror (Admin GraphQL, admin extension components, polaris.shopify.com) aren't available locally.
3. **Browse path**: if keyword search doesn't find a clear match, read the relevant section's `index.md` (for
   Components, Patterns, or Surfaces, read the section `index.md` first, then the category's `index.md`).
4. Read the matched article in full before answering. Guideline articles are short; component and pattern pages are
   longer because they include property tables and examples — read the description, use cases, and **Best practices**
   / **Limitations** sections at minimum, and the properties you actually rely on.

The rest of this file assumes a single question with a single answer. The next sections cover generative tasks —
designing a component, a page, or reviewing an app — which synthesize several articles into one deliverable.

## Designing a new component

Use this workflow for requests like "design a plan-upgrade card" or "create a status column for our orders table":

1. Find the closest existing Polaris web component (`components/`) or composition (`patterns/compositions/`) via
   `topic-index.md` — extend it; don't invent a component from scratch. Shopify's guidance consistently prefers
   documented compositions over custom wrappers.
2. Pull in the guidelines that shape it: `guidelines/visual-design.md` (color roles, typography, icons, branding),
   `guidelines/layout.md` (containers, spacing, density, tables), `guidelines/alerts.md` (if it communicates status),
   and `guidelines/content.md` (labels and copy).
3. Check accessibility: `requirements/accessibility.md`, the color-contrast and color-not-alone rules in
   `guidelines/visual-design.md`, and the component's own **Best practices** section (for example `accessibilityLabel`
   on icon-only buttons in `components/actions/button.md`).
4. Check the matching Built for Shopify rules in `requirements/built-for-shopify-requirements.md` §4 (or
   `references/review-checklist.md` for a quick map).
5. Produce the deliverable using this template:

   ```markdown
   # <Component name>

   **Base component / composition:** <name + references/ path>
   **Purpose:** <what it's for, which merchant task it serves>

   ## Anatomy
   <parts that make up the component, mapped to Polaris components and slots>

   ## States & variants
   <default, hover/focus, loading, disabled (with reason), empty, error, success; tones and variants used>

   ## Layout & spacing
   <container choice, stack/grid direction and gap values, responsive behavior; values from the article, not invented>

   ## Color & tone
   <tone per state, following the color roles in guidelines/visual-design.md>

   ## Content
   <labels, headings, helper and error text following guidelines/content*.md>

   ## Accessibility
   <contrast, labels, keyboard and focus behavior, color-not-alone>

   ## Built for Shopify notes
   <requirements this design must satisfy, with section numbers>

   ## Implementation note
   <example markup only if it's taken from or verified against the component's reference page; otherwise describe intent>
   ```

## Designing a page

Use this workflow for requests like "build a settings page" or "design the app homepage". Shopify ships full-page
**templates**, so start from one instead of decomposing from scratch.

1. Pick the template: `patterns/templates/homepage.md`, `resource-index.md`, `details.md`, or `settings.md`. Each
   includes complete markup that meets Built for Shopify requirements.
2. Decide the shell:
   - **Navigation** — `components/app-bridge/app-nav.md` and `guidelines/navigation.md` (nouns, seven items max before
     "View more", the app name already links home, no duplicate nav in the body).
   - **Page header** — title bar via `<s-page>` (`components/app-bridge/title-bar.md`,
     `components/layout-and-structure/page.md`): one primary action per page, breadcrumbs or Back on sub-pages.
   - **Layout** — `guidelines/layout.md`: single column (`inlineSize` base) for most pages, `large` for resource index
     and dashboards, two columns for visual editors with live preview, the settings layout for settings.
3. Fill the body with compositions from `patterns/compositions/` (setup guide, metrics card, index table, resource
   list, account connection, footer help, …) and supporting guidance (`guidelines/app-home-page.md` for homepage and
   onboarding, `guidelines/forms.md` for forms and saving, `guidelines/alerts.md` for feedback).
4. Cover every state: loading (`components/feedback-and-status-indicators/spinner.md`, `interactions/loading-api.md`),
   empty (`components/feedback-and-status-indicators/empty-state.md`), error, and populated.
5. Produce the deliverable using this template:

   ```markdown
   # <Page name>

   **Purpose:** <what the page is for>
   **Template:** <patterns/templates/… path, or "custom" with reason>
   **Surface:** <App Home / admin block / admin action / checkout / customer account / theme app extension>

   ## Navigation & header
   <app nav entry, page title, primary + secondary actions, breadcrumbs>

   ## Layout
   <inlineSize, columns, aside usage, mobile stacking>

   ## Content
   <sections and compositions used, with references/ paths>

   ## Feedback & saving
   <save bar, toasts, banners, inline errors>

   ## States
   <loading / empty / error / populated / plan-gated>

   ## Accessibility
   <notable considerations beyond the per-component notes>

   ## Built for Shopify notes
   <requirements this page must satisfy, with section numbers>
   ```

For surfaces outside App Home, start from that surface's article in `references/surfaces/` instead. Those pages are
written for buyers rather than merchants — for example `surfaces/checkout/ux-for-checkout.md` (maintain trust, reduce
friction, test scenarios), `surfaces/customer-accounts/ux-for-customer-accounts.md` (fulfillment and payment statuses,
banners), and `surfaces/online-store/theme-app-extensions-ux.md` (app blocks, app embeds, onboarding, uninstalling).

## Reviewing an app UI

Use this for "review this screen", "will this pass Built for Shopify?", or a screenshot/code audit:

1. Read `references/review-checklist.md` and walk every check against the actual UI or code.
2. For each failed or uncertain check, open the cited source section and confirm the rule before reporting it.
3. Report findings grouped by severity: **Blocking** (matches a BFS "reason for rejection" or App Store requirement),
   **Should fix** (contradicts an App Design Guideline), **Consider** (best-practice suggestion from a component page).
   For each: check ID, evidence (file/line or screenshot area), the rule quoted from the source, and the fix.
4. Say what you couldn't verify (for example mobile behavior or performance from a static screenshot).

## Apps that don't use Polaris components

Many apps render App Home with their own React/Vue/Tailwind components. The guidelines still apply — Built for
Shopify judges the result, not the library:

- Match the admin visually: card-style containers, admin button styles (no recolored primary buttons), admin body text
  size, sans-serif type, admin background, 4px spacing grid, WCAG AA contrast (BFS §4.1.1).
- The admin chrome is still App Bridge: use `s-app-nav`, the title bar, the contextual save bar, `s-app-window`, and
  `shopify.toast` even if the body uses custom components. Never rebuild the admin sidebar, top bar, or search inside
  the app body (`guidelines/app-structure.md`).
- When the admin restyles (Polaris 2.0), custom components don't follow automatically —
  `getting-started/polaris-2.md` "Step 2: Audit your app" explains how to find CSS built on Polaris token values and
  compare custom components against Polaris ones.
- Prefer moving toward Polaris web components; `references/migration/` maps each Polaris React component.

## Writing merchant-facing copy

Use `guidelines/content.md`, `guidelines/content-voice-and-tone.md`, and `guidelines/content-grammar-and-mechanics.md`:
plain language (US grade 7 target), sentence case, `{verb}+{noun}` button labels, nouns for nav items, one term per
concept, no idioms or jargon, toasts of three words or fewer, errors that say what happened and how to fix it. Refer to
the app by name first, then "we".

## Answering

- Cite what the article actually says, with its path. Don't invent guidance that isn't there.
- State which **surface** the answer applies to — App Home, admin UI extension, checkout, customer accounts, or theme
  app extension. Rules differ (for example admin blocks have a 600px height limit and can't show promotions; App Home
  can, within the promotion rules).
- Distinguish **requirements** (Built for Shopify / App Store — pass/fail) from **guidelines** (recommended) from
  **component best practices** (advice on a reference page). Say which one you're citing.
- When a question spans more than one section (for example "how should I show a failed sync?" touches
  `guidelines/alerts.md`, `components/feedback-and-status-indicators/banner.md`, and BFS §4.2.4), check more than one
  file rather than stopping at the first match.
- Component and API names, properties, slots, and events **are** documented in this mirror (unlike design-only
  guidelines) — use the exact names from the reference page and don't guess properties that aren't listed. Check
  the Polaris version (`getting-started/web-components-versioning.md`) if a property seems missing.
- If the question falls outside the mirrored content (Admin GraphQL, Shopify Functions logic, admin extension component
  APIs, POS UI, theme Liquid), say so explicitly and fall back to general knowledge or the live docs rather than
  presenting a guess as Shopify guidance.
- Images are real shopify.dev asset URLs with descriptive alt text. Fetch/view them when a visual detail matters more
  than the prose.

## Gotchas

- **Polaris React vs. web components**: polaris.shopify.com and `@shopify/polaris` describe the legacy React library.
  New App Home work uses Polaris web components (`s-*`). Use `references/migration/` to translate React advice.
- **Title bar = `<s-page>`**: the App Bridge title bar is set through the `<s-page>` component's heading, actions, and
  breadcrumbs. Don't add a second visible page title in the body (`guidelines/content.md` "Product content").
- **Save bar**: use either `data-save-bar` on a form or the Save Bar API on a page — not both. Inside `<s-app-window>`,
  put `data-save-bar` on a form inside the window; a parent-page save bar renders behind the window
  (`components/app-bridge/save-bar.md`).
- **App nav home link**: the app name already links to the home route. Add an `s-link rel="home"` only to change the
  home path; never add a visible "Home"/"Dashboard" item that duplicates it (`components/app-bridge/app-nav.md`, BFS
  §4.1.4).
- **Setup guide**: `guidelines/app-home-page.md` still says there's no ready-made setup guide pattern, but
  `patterns/compositions/setup-guide.md` now exists — use the composition.
- **React 18**: controlled Polaris web component fields need React 19; React 18 lacks the custom-element property and
  event handling they rely on (`migration/overview.md` "Requirements"). Server-rendered React 18 also writes boolean
  `false` as the string `"false"` — pass `undefined` instead (`getting-started/using-polaris-web-components.md`
  "Boolean properties in server-rendered React 18 apps").
- **Shadow DOM**: `.Polaris-*` selectors and custom CSS can't style inside web components. Use documented properties,
  and keep custom CSS on app-owned wrapper elements (`migration/overview.md`).
- **Polaris 1 vs. 2**: same components and properties, different appearance. `polaris-1.js` and unversioned
  `polaris.js` serve Polaris 1; `polaris-2.js` serves 2.0 (`getting-started/polaris-2.md`). Load exactly one bundle.
- **App Home iframe vs. App Home UI extension**: the UI extension model (`getting-started/app-home-ui-extensions.md`)
  runs in a Preact runtime and is limited to custom distribution — guidance about App Bridge scripts and iframes
  doesn't transfer one-to-one.
- This is a static content mirror, not a compliance checker. Reason about the user's actual UI against the matched
  article; don't claim an app "passes Built for Shopify" — only Shopify's review decides that.

## Keeping the mirror fresh

Each mirrored file records its `source` URL and fetch `timestamp` in front matter. To refresh everything (pages are
re-selected from the live sitemap, so new components and patterns are picked up), run:

```
python scripts/update_mirror.py          # fetch all pages + rebuild indexes
python scripts/update_mirror.py --index  # rebuild index.md files and topic-index.md only
```

After a refresh, re-check `references/review-checklist.md` against `requirements/built-for-shopify-requirements.md` §4,
because the checklist is hand-written.
