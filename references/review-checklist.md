# Shopify app design review checklist

> **Derived summary, not a mirror.** Every check below condenses a rule from a mirrored article and names the file and
> section it comes from. When a check matters for a decision, open the source article and quote it — the source is
> authoritative, this list is a lookup aid. Regenerating the mirror does not update this file; re-verify it against
> `requirements/built-for-shopify-requirements.md` after a refresh.

Use it to review an existing App Home UI, a screenshot, or a design spec. Report each failed check with its ID, the
evidence, and the source section. "BFS" = Built for Shopify; BFS checks list the concrete reasons Shopify rejects an app.

## 1. Familiar: looks and behaves like the Shopify admin

Source: `requirements/built-for-shopify-requirements.md` §4.1, `guidelines/visual-design.md`, `guidelines/layout.md`

- [ ] **F1** UI is polished: no content flicker, repeated loading in/out, or excessive layout shift. (BFS 4.1.1 #1)
- [ ] **F2** Most content lives in admin-style card containers (`s-section`); no paragraphs directly on the page background. (BFS 4.1.1 #2; guidelines/layout.md "Containers")
- [ ] **F3** Button styles match the admin — primary buttons are not recolored (for example green or purple). (BFS 4.1.1 #3)
- [ ] **F4** No serif or script font for most content; body text size matches the admin. (BFS 4.1.1 #4–5)
- [ ] **F5** App background matches the admin (no black or strongly colored page background). (BFS 4.1.1 #6)
- [ ] **F6** Tabs change only the content below them, never above; tabs don't wrap or shift position. (BFS 4.1.1 #7; guidelines/navigation.md "App nav")
- [ ] **F7** Icons are used consistently in lists and groups — all items or none. (BFS 4.1.1 #8; guidelines/visual-design.md "Icons")
- [ ] **F8** Spacing follows the admin's 4px grid; information density doesn't change within a page. (BFS 4.1.1 #9; guidelines/layout.md "Spacing", "Information density")
- [ ] **F9** Text meets WCAG 2.1 AA contrast (4.5:1 for body text). (BFS 4.1.1 #10; guidelines/visual-design.md "Color")
- [ ] **F10** Every sub-page offers a Back button or breadcrumb to its parent. (BFS 4.1.1 #11; guidelines/navigation.md "Information architecture")
- [ ] **F11** Mobile: no page-wide horizontal scroll, no unreachable content, multi-column layouts stack. (BFS 4.1.2)
- [ ] **F12** App name in the admin nav doesn't truncate (20 characters max, no description in the name). (BFS 4.1.3; guidelines/navigation.md "App name")
- [ ] **F13** Primary navigation uses `s-app-nav` — no custom sidebar/top bar inside the app body; sub-pages highlight their parent item; no separate "Home" item duplicating the app name; no emojis in nav items. (BFS 4.1.4; guidelines/navigation.md; guidelines/app-structure.md "App body")
- [ ] **F14** Forms save through the contextual save bar; merchants can't leave a dirty form without choosing Save or Discard; no auto-save or continuous validation. (BFS 4.1.5; guidelines/forms.md)
- [ ] **F15** `s-modal` uses its `heading` property and `primary-action` / `secondary-actions` slots for its buttons; full-screen work uses `s-app-window`, not the deprecated Fullscreen bar. (BFS 4.1.6)
- [ ] **F16** App window launches from a button in the app body, never from the app nav. (guidelines/app-structure.md "App window")

## 2. Helpful: easy to set up and use

Source: `requirements/built-for-shopify-requirements.md` §4.2, `guidelines/app-home-page.md`, `guidelines/alerts.md`, `guidelines/content*.md`

- [ ] **H1** No prominent spelling or grammar errors in headings, nav items, or button labels; labels have enough context (for example a "Time" field states its unit). (BFS 4.2.1)
- [ ] **H2** Onboarding is concise (five steps or fewer), easy to find, guides to completion, can be finished later, and its UI can be removed once complete. (BFS 4.2.2; guidelines/app-home-page.md "Onboarding")
- [ ] **H3** Onboarding never implies another app must be installed, and every question explains why it's asked. (BFS 4.2.2 #4–5)
- [ ] **H4** Homepage shows whether the app is set up and working (including theme app block/embed status), shows relevant metrics, and isn't only static content after dismissals. (BFS 4.2.3; guidelines/app-home-page.md "Purpose")
- [ ] **H5** Errors are red, sit next to the relevant field, appear only after interaction (on blur, not while typing), and never auto-dismiss — no error toasts except persistent connection errors. (BFS 4.2.4; guidelines/alerts.md "Error")
- [ ] **H6** In a group of related actions, the most logical next action is the visually dominant one; each page and card has at most one primary action. (BFS 4.2.5; guidelines/navigation.md "Primary and secondary actions"; guidelines/layout.md "Using sections")
- [ ] **H7** Visual customization has a live preview that's visible alongside the controls on desktop (two-column layout). (BFS 4.2.6; guidelines/layout.md "Two-column layout")
- [ ] **H8** Toasts confirm success only, in three words or fewer; success banners only when feedback is delayed, persistent, or has a CTA. (guidelines/alerts.md "Success")
- [ ] **H9** Banners are dismissible unless critical, and dismissed banners stay hidden for the session. (guidelines/alerts.md "Informational banner")
- [ ] **H10** Copy uses plain language (US grade 7 target), no jargon or idioms, one term per concept, `{verb}+{noun}` CTAs in sentence case. (guidelines/content.md; guidelines/navigation.md; guidelines/content-grammar-and-mechanics.md)
- [ ] **H11** No duplicated content: no page title repeated under the title bar, no horizontal nav duplicating the app nav, no "quick links" card repeating nav items. (guidelines/content.md "Product content"; guidelines/navigation.md "App nav")

## 3. User-friendly: doesn't mislead, pressure, distract, or overwhelm

Source: `requirements/built-for-shopify-requirements.md` §4.3, `guidelines/alerts.md` "Promotion"

- [ ] **U1** No promised outcomes ("increase your sales by 18%") and no inaccurate ratings for promoted apps. (BFS 4.3.1)
- [ ] **U2** No countdown timers, guilt or shame wording ("No thanks, I prefer less sales"), or rewards for 5-star reviews. (BFS 4.3.2)
- [ ] **U3** No modals or popovers that open on page load, after a delay, or from an unrelated action; no attention-seeking animation; red only for errors and destructive actions. (BFS 4.3.3)
- [ ] **U4** Long forms are split into titled groups (sections or cards for more than five inputs); never two banners close together; no multi-paragraph text blocks. (BFS 4.3.4; guidelines/forms.md)
- [ ] **U5** Nothing could be mistaken for Shopify: no Shopify logo, first-party-style icon, Sidekick icon, or Shopify's magic purple for AI features. (BFS 4.3.5; guidelines/visual-design.md "App icon")
- [ ] **U6** Promotions are dismissible, stay dismissed for that user, sit at the bottom of the homepage or on a dedicated page, and aren't repeated on every page. (BFS 4.3.6; guidelines/alerts.md "Promotion")
- [ ] **U7** Plan-gated features are visually and functionally disabled and name the plan that unlocks them; Plus-only features are hidden from non-Plus stores. (BFS 4.3.7; guidelines/alerts.md "Promotion")
- [ ] **U8** Admin UI extensions (blocks, actions) contain no promotions, ads, or review requests. (guidelines/app-structure.md "Admin UI extensions")

## 4. Admin UI extensions

Source: `guidelines/app-structure.md` "Admin UI extensions"

- [ ] **E1** Admin blocks stay under 600px tall (paginate if needed), keep inputs visible, and have an informative empty state.
- [ ] **E2** Admin block inputs use the extension `form` component so the contextual save bar works.
- [ ] **E3** Admin action content stays under 1200px with no more than two steps of pagination; complex flows route into the app with an admin link instead.
- [ ] **E4** Blocks and actions don't duplicate each other's content.

## 5. Accessibility

Source: `requirements/accessibility.md`, `guidelines/visual-design.md`, `guidelines/alerts.md`

- [ ] **A1** Status is never conveyed by color alone — warnings and errors pair text with an icon.
- [ ] **A2** Color roles express state, not categories (badge `tone` follows the status; categories use neutral chips or text). (guidelines/visual-design.md "Color")
- [ ] **A3** Each table row carries at most one severity signal; row actions are tertiary or icon-only buttons or a menu, never primary buttons. (guidelines/layout.md "Using tables")
- [ ] **A4** Icon-only buttons have an `accessibilityLabel`; disabled buttons explain why; `loading` is used for in-progress actions. (components/actions/button.md "Best practices", "Limitations")
- [ ] **A5** Keyboard, headings, forms, and modal behavior follow `requirements/accessibility.md`.
