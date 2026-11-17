"""Refresh the local mirror of Shopify's app design documentation.

Downloads the current shopify.dev sitemap, selects the design-related pages
(App Design Guidelines, Polaris web components, App Bridge components and APIs,
App Home patterns, surface UX guidelines, Built for Shopify / App Store
requirements, and the Polaris React migration guide), fetches each page's
official markdown export (`<url>.md`), and regenerates every generated
`index.md` plus `references/topic-index.md`.

Hand-written files (`SKILL.md`, `references/review-checklist.md`) are never
touched.

Usage:
    python scripts/update_mirror.py            # refresh everything
    python scripts/update_mirror.py --index    # only rebuild indexes from files on disk
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import gzip
import pathlib
import re
import sys
import time
import urllib.request

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
REFS = SKILL_DIR / "references"
BASE = "https://shopify.dev/"
SITEMAP_INDEX = BASE + "sitemap.xml"
USER_AGENT = "shopify-app-design-skill-mirror/1.0"

# ---------------------------------------------------------------------------
# Section definitions
# ---------------------------------------------------------------------------

GUIDELINES = [
    ("docs/apps/design", "guidelines/overview.md"),
    ("docs/apps/design/app-structure", "guidelines/app-structure.md"),
    ("docs/apps/design/navigation", "guidelines/navigation.md"),
    ("docs/apps/design/layout", "guidelines/layout.md"),
    ("docs/apps/design/visual-design", "guidelines/visual-design.md"),
    ("docs/apps/design/content", "guidelines/content.md"),
    ("docs/apps/design/content/voice-and-tone", "guidelines/content-voice-and-tone.md"),
    ("docs/apps/design/content/grammar-and-mechanics", "guidelines/content-grammar-and-mechanics.md"),
    ("docs/apps/design/user-experience/alerts", "guidelines/alerts.md"),
    ("docs/apps/design/user-experience/app-home-page", "guidelines/app-home-page.md"),
    ("docs/apps/design/user-experience/forms", "guidelines/forms.md"),
]

GETTING_STARTED = [
    ("docs/apps/build/app-home", "getting-started/app-home.md"),
    ("docs/api/app-home", "getting-started/app-home-reference.md"),
    ("docs/api/polaris", "getting-started/polaris.md"),
    ("docs/api/polaris/using-polaris-web-components", "getting-started/using-polaris-web-components.md"),
    ("docs/apps/build/app-home/polaris2", "getting-started/polaris-2.md"),
    ("docs/apps/build/app-home/app-home-ui-extensions", "getting-started/app-home-ui-extensions.md"),
    ("docs/api/app-home/latest/web-components/versioning", "getting-started/web-components-versioning.md"),
]

SURFACES = [
    ("docs/apps/build/checkout/ux-for-checkout", "surfaces/checkout/ux-for-checkout.md"),
    ("docs/apps/build/checkout/fields-banners/ux-for-fields", "surfaces/checkout/ux-for-fields.md"),
    ("docs/apps/build/checkout/payments/ux-for-payments", "surfaces/checkout/ux-for-payments.md"),
    ("docs/apps/build/checkout/chat/ux-for-chat", "surfaces/checkout/ux-for-chat.md"),
    ("docs/apps/build/checkout/delivery-shipping/delivery-methods/ux-for-delivery-methods", "surfaces/checkout/ux-for-delivery-methods.md"),
    ("docs/apps/build/checkout/delivery-shipping/delivery-methods/ux-for-pickup-points", "surfaces/checkout/ux-for-pickup-points.md"),
    ("docs/apps/build/checkout/delivery-shipping/delivery-options/ux-for-delivery-options", "surfaces/checkout/ux-for-delivery-options.md"),
    ("docs/apps/build/checkout/product-offers/ux-for-pre-purchase-product-offers", "surfaces/checkout/ux-for-pre-purchase-product-offers.md"),
    ("docs/apps/build/checkout/product-offers/ux-for-post-purchase-product-offers", "surfaces/checkout/ux-for-post-purchase-product-offers.md"),
    ("docs/apps/build/checkout/product-offers/ux-for-post-purchase-subscriptions", "surfaces/checkout/ux-for-post-purchase-subscriptions.md"),
    ("docs/apps/build/checkout/thank-you-order-status/ux-for-announcement-bar", "surfaces/checkout/ux-for-announcement-bar.md"),
    ("docs/apps/build/customer-accounts/ux", "surfaces/customer-accounts/ux-for-customer-accounts.md"),
    ("docs/apps/build/customer-accounts/full-page-extensions/ux-for-full-pages", "surfaces/customer-accounts/ux-for-full-pages.md"),
    ("docs/apps/build/customer-accounts/order-action-extensions/ux-for-order-actions", "surfaces/customer-accounts/ux-for-order-actions.md"),
    ("docs/apps/build/customer-accounts/editor-extension-collections/editor-extension-collections-ux-guidelines", "surfaces/customer-accounts/editor-extension-collections-ux.md"),
    ("docs/apps/build/online-store/theme-app-extensions/ux", "surfaces/online-store/theme-app-extensions-ux.md"),
    ("docs/storefronts/themes/best-practices/design", "surfaces/online-store/theme-design.md"),
    ("docs/storefronts/themes/best-practices/design/color-system", "surfaces/online-store/theme-color-system.md"),
    ("docs/storefronts/themes/best-practices/accessibility", "surfaces/online-store/theme-accessibility.md"),
    ("docs/apps/build/discounts/ux-for-discounts", "surfaces/discounts/ux-for-discounts.md"),
    ("docs/apps/build/purchase-options/subscriptions/migrate-to-subscriptions-api/ux-for-migration", "surfaces/subscriptions/ux-for-subscriptions-migration.md"),
    ("docs/storefronts/themes/pricing-payments/subscriptions/subscription-ux-guidelines", "surfaces/subscriptions/subscription-ux-guidelines.md"),
    ("docs/storefronts/themes/pricing-payments/preorder-tbyb/preorder-tbyb-ux-guidelines", "surfaces/subscriptions/preorder-tbyb-ux-guidelines.md"),
]

REQUIREMENTS = [
    ("docs/apps/launch/built-for-shopify", "requirements/built-for-shopify.md"),
    ("docs/apps/launch/built-for-shopify/requirements", "requirements/built-for-shopify-requirements.md"),
    ("docs/apps/launch/shopify-app-store/app-store-requirements", "requirements/app-store-requirements.md"),
    ("docs/apps/build/accessibility", "requirements/accessibility.md"),
    ("docs/apps/launch/privacy-requirements", "requirements/privacy-requirements.md"),
]

COMPONENT_CATEGORIES = [
    ("actions", "Actions", "Buttons, links, menus, and clickable surfaces that start tasks or navigate."),
    ("feedback-and-status-indicators", "Feedback and status indicators", "Badges, banners, empty states, progress, and spinners that communicate status."),
    ("forms", "Forms", "Inputs, pickers, and choice controls for collecting merchant data."),
    ("layout-and-structure", "Layout and structure", "Page, section, stack, grid, box, table, and lists for arranging content."),
    ("media-and-visuals", "Media and visuals", "Avatars, icons, images, and thumbnails."),
    ("overlays", "Overlays", "Modals and popovers layered above the page."),
    ("typography-and-content", "Typography and content", "Headings, paragraphs, text, numbers, chips, and tooltips."),
    ("app-bridge", "App Bridge web components", "Admin chrome around the app: app nav, title bar, save bar, and app window. Not versioned with Polaris."),
]

PATTERN_GROUPS = [
    ("templates", "Templates", "Full-page layouts: homepage, resource index, details, and settings."),
    ("compositions", "Compositions", "Reusable multi-component building blocks such as setup guides, metrics cards, index tables, and account connection."),
]

SURFACE_GROUPS = [
    ("checkout", "Checkout", "UX guidelines for checkout UI extensions, payments, delivery, product offers, chat, and announcement bars."),
    ("customer-accounts", "Customer accounts", "UX guidelines for customer account UI extensions: full pages, order actions, and editor collections."),
    ("online-store", "Online store", "Theme app extension UX plus the theme design, color system, and accessibility practices app blocks render into."),
    ("discounts", "Discounts", "UX guidelines for discount function apps in the Shopify admin."),
    ("subscriptions", "Subscriptions and purchase options", "Subscription, preorder, and try-before-you-buy UX guidelines."),
]

SECTIONS = [
    ("getting-started", "Getting started", "How App Home works, what Polaris is, how to use Polaris web components, Polaris 2.0, App Home UI extensions, and versioning."),
    ("guidelines", "App Design Guidelines", "Shopify's App Design Guidelines: app structure, navigation, layout, visual design, content, alerts, App Home and onboarding, and forms."),
    ("components", "Components", "Polaris web components for App Home (s-*) in 7 categories, plus App Bridge web components for the admin chrome."),
    ("patterns", "Patterns", "App Home templates (full pages) and compositions (multi-component building blocks), with complete example markup."),
    ("interactions", "Interactions", "App Bridge user-interface APIs: toast, modal, save bar, loading, navigation, resource picker, picker, intents, reviews, support, and more."),
    ("surfaces", "Surfaces", "UX guidelines for app surfaces outside App Home: checkout, customer accounts, online store / theme app extensions, discounts, subscriptions."),
    ("requirements", "Requirements", "Built for Shopify requirements (including design rejection reasons), App Store requirements, accessibility, and privacy requirements."),
    ("migration", "Migration", "Polaris React (@shopify/polaris) to Polaris web components migration guide, with one mapping page per React component."),
]

GUIDELINE_ORDER = [d for _, d in GUIDELINES]
TAG_OVERRIDES = {"components/app-bridge/title-bar.md": "s-page (title bar)", "components/app-bridge/save-bar.md": "ui-save-bar"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def http_get(url: str) -> bytes:
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - retry any transport failure
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


def sitemap_paths() -> list[str]:
    index = http_get(SITEMAP_INDEX).decode("utf-8")
    paths: set[str] = set()
    for loc in re.findall(r"<loc>([^<]+)</loc>", index):
        raw = http_get(loc)
        if loc.endswith(".gz"):
            raw = gzip.decompress(raw)
        for url in re.findall(r"<loc>([^<]+)</loc>", raw.decode("utf-8")):
            if url.startswith(BASE):
                paths.add(url[len(BASE):].rstrip("/"))
    return sorted(paths)


def build_manifest(paths: list[str]) -> dict[str, str]:
    manifest: dict[str, str] = {}
    for src, dest in GUIDELINES + GETTING_STARTED + SURFACES + REQUIREMENTS:
        manifest[src] = dest
    manifest["docs/api/app-home/latest/web-components"] = "components/overview.md"
    manifest["docs/api/app-home/latest/app-bridge-web-components"] = "components/app-bridge/overview.md"
    manifest["docs/api/app-home/latest/patterns"] = "patterns/overview.md"
    manifest["docs/apps/build/app-home/migrate-from-polaris-react"] = "migration/overview.md"
    rules = [
        (r"docs/api/app-home/latest/web-components/([a-z\-]+)/([a-z0-9\-]+)", "components/{0}/{1}.md"),
        (r"docs/api/app-home/latest/app-bridge-web-components/([a-z0-9\-]+)", "components/app-bridge/{0}.md"),
        (r"docs/api/app-home/latest/patterns/(compositions|templates)/([a-z0-9\-]+)", "patterns/{0}/{1}.md"),
        (r"docs/api/app-home/latest/apis/user-interface-and-interactions/([a-z0-9\-]+)", "interactions/{0}.md"),
        (r"docs/apps/build/app-home/migrate-from-polaris-react/([a-z0-9\-]+)", "migration/{0}.md"),
    ]
    for path in paths:
        for pattern, template in rules:
            match = re.fullmatch(pattern, path)
            if match:
                manifest[path] = template.format(*match.groups())
    return manifest


FRONT_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def parse_front(text: str) -> tuple[dict[str, str], str]:
    match = FRONT_RE.match(text)
    if not match:
        return {}, text
    data: dict[str, str] = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        key_match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if key_match:
            key, value = key_match.group(1), key_match.group(2).strip()
            if value in (">-", ">", "|", "|-"):
                buf = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                    buf.append(lines[i].strip())
                    i += 1
                data[key] = " ".join(b for b in buf if b)
                continue
            data[key] = value.strip("'\"").replace('\\"', '"')
        i += 1
    return data, text[match.end():]


def yaml_str(value: str) -> str:
    return '"' + (value or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def fetch_page(src: str, dest: str) -> None:
    text = http_get(BASE + src + ".md").decode("utf-8")
    meta, body = parse_front(text)
    title = meta.get("title") or dest.rsplit("/", 1)[-1].removesuffix(".md")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    front = (
        "---\n"
        f"title: {yaml_str(title)}\n"
        f"description: {yaml_str(meta.get('description', ''))}\n"
        f"source: {BASE}{src}\n"
        f"timestamp: {stamp}\n"
        "---\n\n"
    )
    out = REFS / dest
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(front + body.lstrip("\n"), encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# Index generation
# ---------------------------------------------------------------------------

class Doc:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.rel = path.relative_to(REFS).as_posix()
        meta, body = parse_front(path.read_text(encoding="utf-8"))
        self.title = meta.get("title", path.stem)
        self.description = meta.get("description", "")
        self.source = meta.get("source", "")
        self.body = body

    @property
    def slug(self) -> str:
        return self.source.replace(BASE, "/").replace("/latest/", "/")

    @property
    def short(self) -> str:
        text = re.sub(r"\s+", " ", self.description).strip()
        sentence = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
        return sentence if len(sentence) <= 240 else sentence[:237].rstrip() + "..."

    @property
    def tag(self) -> str:
        if self.rel in TAG_OVERRIDES:
            return TAG_OVERRIDES[self.rel]
        if not self.rel.startswith("components/") or self.path.stem == "overview":
            return ""
        for prefix in ("s-", "ui-"):
            candidate = prefix + self.path.stem
            if f"<{candidate}" in self.body:
                return candidate
        return ""

    def label(self) -> str:
        return f"{self.title} (`<{self.tag}>`)" if self.tag and not self.tag.startswith("s-page (") else (
            f"{self.title} (`<s-page>` title bar)" if self.tag else self.title
        )


def docs_in(folder: pathlib.Path) -> list[Doc]:
    return [Doc(p) for p in sorted(folder.glob("*.md")) if p.name != "index.md"]


def write(path: pathlib.Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def list_lines(docs: list[Doc], base: pathlib.Path) -> list[str]:
    lines = []
    for doc in docs:
        rel = doc.path.relative_to(base).as_posix()
        lines.append(f"- [{doc.label()}]({rel}) - {doc.short}")
    return lines


def overview_first(docs: list[Doc]) -> list[Doc]:
    return sorted(docs, key=lambda d: (d.path.stem != "overview", d.path.stem))


def build_indexes() -> None:
    section_meta = {key: (title, desc) for key, title, desc in SECTIONS}

    def header(title: str, desc: str, crumb: str) -> list[str]:
        return [f"# {title}", "", f"**Navigation:** {crumb}", "", f"> {desc}", ""]

    # Guidelines (ordered like shopify.dev navigation)
    folder = REFS / "guidelines"
    docs = {d.rel: d for d in docs_in(folder)}
    ordered = [docs[r] for r in GUIDELINE_ORDER if r in docs] + [d for r, d in docs.items() if r not in GUIDELINE_ORDER]
    title, desc = section_meta["guidelines"]
    write(folder / "index.md", "\n".join(header(title, desc, "[Topic index](../topic-index.md)") + list_lines(ordered, folder)))

    # Flat sections
    for key in ("getting-started", "interactions", "requirements"):
        folder = REFS / key
        title, desc = section_meta[key]
        write(folder / "index.md", "\n".join(header(title, desc, "[Topic index](../topic-index.md)") + list_lines(overview_first(docs_in(folder)), folder)))

    # Migration: overview first, then a compact alphabetical list
    folder = REFS / "migration"
    title, desc = section_meta["migration"]
    lines = header(title, desc, "[Topic index](../topic-index.md)")
    all_docs = overview_first(docs_in(folder))
    lines += ["Start with [overview.md](overview.md) for the migration process, then open the page for the React component you're replacing.", ""]
    for doc in all_docs[1:]:
        name = re.sub(r"^Migrate (.*) from Polaris React$", r"\1", doc.title)
        lines.append(f"- [{name}]({doc.path.name})")
    write(folder / "index.md", "\n".join(lines))

    # Nested sections
    nested = {
        "components": COMPONENT_CATEGORIES,
        "patterns": PATTERN_GROUPS,
        "surfaces": SURFACE_GROUPS,
    }
    for key, groups in nested.items():
        folder = REFS / key
        title, desc = section_meta[key]
        lines = header(title, desc, "[Topic index](../topic-index.md)")
        overview = folder / "overview.md"
        if overview.exists():
            lines += [f"Section overview (mirrored): [overview.md](overview.md)", ""]
        for sub, sub_title, sub_desc in groups:
            sub_folder = folder / sub
            if not sub_folder.exists():
                continue
            count = len(docs_in(sub_folder))
            lines.append(f"- [{sub_title}]({sub}/index.md) - {sub_desc} ({count} articles)")
            sub_lines = header(sub_title, sub_desc, f"[{title}](../index.md) / [Topic index](../../topic-index.md)")
            write(sub_folder / "index.md", "\n".join(sub_lines + list_lines(overview_first(docs_in(sub_folder)), sub_folder)))
        write(folder / "index.md", "\n".join(lines))

    # Topic index
    out = [
        "# Topic index",
        "",
        "Flattened lookup of every article mirrored under `references/`. Grep this file for a component tag (`s-button`),",
        "a React component name (`DataTable`), a topic, or the tail of a shopify.dev URL (`overlays/modal`) before browsing",
        "section `index.md` files. Format: **Name** — `path` — one-line description — source slug.",
        "",
        "Source slugs drop the `/latest/` version segment, so they match links both with and without it.",
        "",
        "- **Review checklist (derived, not mirrored)** — `references/review-checklist.md` — Condensed Built for Shopify design checks and App Design Guidelines rules for reviewing an app UI, each with its source file.",
        "",
    ]
    for key, title, _ in SECTIONS:
        folder = REFS / key
        out.append(f"## {title} (`references/{key}/`)")
        out.append("")
        docs_all = sorted(
            (Doc(p) for p in folder.rglob("*.md") if p.name != "index.md"),
            key=lambda d: (GUIDELINE_ORDER.index(d.rel) if d.rel in GUIDELINE_ORDER else 999, d.rel),
        )
        current_sub = None
        for doc in docs_all:
            parts = doc.rel.split("/")
            sub = parts[1] if len(parts) > 2 else None
            if sub != current_sub and sub is not None:
                out.append("")
                out.append(f"### {key}/{sub}")
                out.append("")
            current_sub = sub
            out.append(f"- **{doc.label()}** — `references/{doc.rel}` — {doc.short} — `{doc.slug}`")
        out.append("")
    write(REFS / "topic-index.md", "\n".join(out))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if "--index" not in sys.argv:
        print("Reading sitemap...")
        manifest = build_manifest(sitemap_paths())
        print(f"Fetching {len(manifest)} pages...")
        errors: dict[str, str] = {}
        with cf.ThreadPoolExecutor(max_workers=6) as pool:
            futures = {pool.submit(fetch_page, src, dest): src for src, dest in manifest.items()}
            for future in cf.as_completed(futures):
                try:
                    future.result()
                except Exception as exc:  # noqa: BLE001
                    errors[futures[future]] = str(exc)
        for src, err in sorted(errors.items()):
            print(f"ERROR {src}: {err}")
        print(f"Fetched {len(manifest) - len(errors)} / {len(manifest)} pages.")
    build_indexes()
    print("Indexes rebuilt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
