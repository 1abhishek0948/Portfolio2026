#!/usr/bin/env python3
"""Generate the 1,000-page Nepal blog library under ./blog.

- 20 money-keyword posts are rendered in full from content/blog/<slug>.md
- 980 planned guides are rendered as noindex outline pages
- plus a hub, 8 category pages, client search index, RSS and sitemap
"""
import os
import re
import json
import csv
import io
import zlib
import html as htmllib
from datetime import datetime

import yaml
import markdown
from PIL import Image, ImageDraw, ImageFont

import blog_data
from remote_image_catalog import BLOG_ALT_OVERRIDES, BLOG_FALLBACKS, BLOG_OVERRIDES, BLOG_REPLACEMENTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = blog_data.SITE
OUT = os.path.join(ROOT, "blog")
CONTENT = os.path.join(ROOT, "content", "blog")
PRIORITY80_SET = set(blog_data.priority80_slugs())
ALL_TOPICS = blog_data.build_all()

CLUSTER_COLORS = {
    "payments": "#0F62FE",
    "freelancing": "#1F9D55",
    "web": "#D97706",
    "marketing": "#DB2777",
    "business": "#7C3AED",
    "career": "#0891B2",
    "travel": "#4F46E5",
    "ai": "#DC2626",
}
DEFAULT_REMOTE_IMAGE = next(iter(BLOG_FALLBACKS.values()))["image_url"]

# ---------------------------------------------------------------------------
# Blog covers — assets/blog/covers/manifest.json written by tools/source_covers.py
# ---------------------------------------------------------------------------
COVER_MANIFEST_PATH = os.path.join(ROOT, "assets", "blog", "covers", "manifest.json")
_COVERS = {"covers": {}, "mapping": {}}
try:
    with open(COVER_MANIFEST_PATH, encoding="utf-8") as _fh:
        _COVERS = json.load(_fh)
    if "covers" not in _COVERS or "mapping" not in _COVERS:
        _COVERS = {"covers": {}, "mapping": {}}
except Exception:
    _COVERS = {"covers": {}, "mapping": {}}

_ANGLE_SUFFIXES = (
    "-2026-guide", "-common-mistakes", "-cost-and-pricing", "-faq",
    "-for-beginners", "-in-kathmandu", "-pros-and-cons", "-step-by-step",
    "-tools-and-resources",
)


def cover_family(slug):
    """Resolve a page slug to its topic family (cover key)."""
    if slug in _COVERS["mapping"]:
        return _COVERS["mapping"][slug]
    root = slug
    for suffix in _ANGLE_SUFFIXES:
        if root.endswith(suffix) and len(root) > len(suffix):
            root = root[: -len(suffix)]
            break
    return root


def cover_for(slug):
    """Remote cover entry for a slug, or None."""
    family = cover_family(slug)
    entry = (
        BLOG_REPLACEMENTS.get(family)
        or BLOG_OVERRIDES.get(family)
        or _COVERS["covers"].get(family)
        or BLOG_FALLBACKS.get(family)
    )
    if entry and family in BLOG_ALT_OVERRIDES:
        entry = dict(entry)
        entry["alt"] = BLOG_ALT_OVERRIDES[family]
    return entry


def cluster_cover(key):
    """First covered family of a cluster — representative og:image for hub/category."""
    seen = set()
    for t in ALL_TOPICS:
        if t["cluster"] != key:
            continue
        fam = cover_family(t["slug"])
        if fam in seen:
            continue
        seen.add(fam)
        entry = _COVERS["covers"].get(fam)
        if entry:
            return entry
    return None


def cover_og(entry):
    """Direct remote image URL for a cover entry."""
    if not entry:
        return None
    return entry.get("image_url")


def cover_image_object(entry, title):
    """schema.org ImageObject carrying verbatim license + creator metadata."""
    if not entry:
        return None
    data = {
        "@type": "ImageObject",
        "url": cover_og(entry),
        "contentUrl": cover_og(entry),
        "width": 1200,
        "height": 675,
        "caption": entry.get("alt") or title,
        "creditText": "%s (%s)" % (entry.get("creator", "Unknown creator"), entry.get("provider", "Wikimedia Commons").split(" (")[0]),
        "creator": {"@type": "Person", "name": entry.get("creator", "Unknown creator")},
    }
    if entry.get("license_url"):
        data["license"] = entry["license_url"]
    return data


def card_media(root, slug):
    """Remote cover media block for listing/related cards."""
    entry = cover_for(slug)
    if not entry:
        return ""
    image_url = entry.get("image_url")
    if not image_url:
        return ""
    alt = htmllib.escape(entry.get("alt", ""), quote=True)
    return ('<span class="card-media"><img src="%s" '
            'width="480" height="270" alt="%s" loading="lazy" decoding="async" /></span>'
            % (htmllib.escape(image_url, quote=True), alt))


def hero_cover_figure(root, slug, eager=True):
    """Article hero cover using the source's direct remote image URL."""
    entry = cover_for(slug)
    image_url = entry.get("image_url") if entry else None
    if not image_url:
        return None
    alt = htmllib.escape(entry.get("alt", ""), quote=True)
    loading = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    figcaption = cover_figcaption(entry)
    return ('<figure class="article-featured has-cover">\n'
            '            <img src="%s" width="1200" height="675" '
            'alt="%s"%s decoding="async" />%s\n'
            '          </figure>' % (htmllib.escape(image_url, quote=True), alt, loading, figcaption))


def cover_figcaption(entry):
    """Visible attribution line for attribution-required licenses (CC BY*)."""
    lic = entry.get("license", "")
    if not lic.upper().startswith("CC BY"):
        return ""  # CC0 / Public Domain: attribution not required; metadata only
    def link(href, text):
        text = (text or "").strip()
        if not text:
            return ""
        if not href:
            return htmllib.escape(text)
        return '<a href="%s" rel="noopener">%s</a>' % (htmllib.escape(href, quote=True), htmllib.escape(text))
    creator = link(entry.get("creator_url", ""), entry.get("creator", "Unknown creator"))
    provider = link(entry.get("source_url", ""), "Wikimedia Commons" if entry.get("provider", "").startswith("Wikimedia") else entry.get("provider", ""))
    license_link = link(entry.get("license_url", ""), lic)
    parts = "".join('<span>%s</span>' % p for p in (creator, provider, license_link) if p)
    return '<figcaption class="cover-credit">%s</figcaption>' % parts


# ---------------------------------------------------------------------------
# HTML shell
# ---------------------------------------------------------------------------
SVG_SYMBOLS = """<svg xmlns="http://www.w3.org/2000/svg" style="display: none" aria-hidden="true">
    <defs>
      <symbol id="i-moon" viewBox="0 0 24 24"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" /></symbol>
      <symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4" /><path d="M12 2v2" /><path d="M12 20v2" /><path d="m4.93 4.93 1.41 1.41" /><path d="m17.66 17.66 1.41 1.41" /><path d="M2 12h2" /><path d="M20 12h2" /><path d="m6.34 17.66-1.41 1.41" /><path d="m19.07 4.93-1.41 1.41" /></symbol>
      <symbol id="i-arrow-up-right" viewBox="0 0 24 24"><line x1="7" y1="17" x2="17" y2="7" /><polyline points="7 7 17 7 17 17" /></symbol>
      <symbol id="i-arrow-left" viewBox="0 0 24 24"><line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" /></symbol>
      <symbol id="i-arrow-up" viewBox="0 0 24 24"><line x1="12" y1="12" x2="12" y2="19" /><polyline points="5 12 12 5 19 12" /></symbol>
      <symbol id="i-share" viewBox="0 0 24 24"><circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><line x1="8.59" y1="13.51" x2="15.42" y2="17.49" /><line x1="15.41" y1="6.51" x2="8.59" y2="10.49" /></symbol>
      <symbol id="i-home" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /><polyline points="9 22 9 12 15 12 15 22" /></symbol>
      <symbol id="i-user" viewBox="0 0 24 24"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" /></symbol>
      <symbol id="i-file-text" viewBox="0 0 24 24"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><line x1="10" y1="9" x2="8" y2="9" /></symbol>
      <symbol id="i-shield" viewBox="0 0 24 24"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" /></symbol>
      <symbol id="i-sparkles" viewBox="0 0 24 24"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z" /><path d="M20 3v4" /><path d="M22 5h-4" /><path d="M4 17v2" /><path d="M5 18H3" /></symbol>
      <symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 1.72 1.28 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" /></symbol>
    </defs>
  </svg>"""


def nav_top(root, active):
    links = [
        ("About", root + "#about", "about"),
        ("Capabilities", root + "#capabilities", "capabilities"),
        ("Services", root + "services/", "services"),
        ("Projects", root + "projects/", "projects"),
        ("Articles", root + "articles/", "articles"),
        ("Blog", root + "blog/", "blog"),
    ]
    out = []
    for label, href, key in links:
        if label in ("About", "Capabilities"):
            attr = ' data-target="%s"' % key
        else:
            attr = ""
        cur = ' class="top-nav-link active" aria-current="page"' if active == key else ' class="top-nav-link"'
        out.append('        <a%s href="%s"%s>%s</a>\n' % (cur, href, attr, label))
    return "".join(out)


def shell_head(root, title, description, robots, canonical, og_image, og_type, extra_meta="", extra_ld="", og_dims=(1200, 630), og_image_alt=""):
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>%s</title>
  <meta name="description" content="%s">
  <meta name="robots" content="%s">
  <meta name="author" content="%s">
  <meta name="theme-color" content="#f5f5f2">
  <link rel="canonical" href="%s">
  <link rel="alternate" hreflang="en" href="%s">
  <link rel="alternate" hreflang="x-default" href="%s">
  <link rel="icon" type="image/png" href="%sassets/favicon.png" sizes="48x48">
  <link rel="apple-touch-icon" href="%sassets/apple-touch-icon.png">
  <link rel="stylesheet" href="%sstyle.css">
  <link rel="stylesheet" href="%sarticles/articles.css">
  <link rel="stylesheet" href="%sarticles/article.css">
  <link rel="stylesheet" href="%sblog.css">
  <meta property="og:locale" content="en_US">
  <meta property="og:type" content="%s">
  <meta property="og:site_name" content="Abhishek Thakur">
  <meta property="og:title" content="%s">
  <meta property="og:description" content="%s">
  <meta property="og:url" content="%s">
  <meta property="og:image" content="%s">
  <meta property="og:image:width" content="%d">
  <meta property="og:image:height" content="%d">
  <meta property="og:image:alt" content="%s">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%s">
  <meta name="twitter:description" content="%s">
  <meta name="twitter:image" content="%s">
%s%s
__GA__
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
%s""" % (
        htmllib.escape(title), htmllib.escape(description), robots, blog_data.AUTHOR,
        canonical, canonical, canonical, root, root, root, root, root, root,
        og_type, htmllib.escape(title), htmllib.escape(description), canonical, og_image,
        og_dims[0], og_dims[1], htmllib.escape(og_image_alt or title),
        htmllib.escape(title), htmllib.escape(description), og_image,
        extra_ld, extra_meta, SVG_SYMBOLS,
    )


def shell_body_open(root, active):
    return """  <div class="app">
    <header class="site-header">
      <a class="brand-logo" href="%s" aria-label="Abhishek Thakur home">
        <img src="%sassets/abhishek-thakur-logo.webp" alt="Abhishek Thakur" width="152" height="100" />
      </a>
      <nav class="top-nav" aria-label="Site navigation">
%s      </nav>
      <div class="header-right">
        <a class="top-nav-cta" href="%s#contact">Start a project</a>
        <button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false">
          <svg class="icon" aria-hidden="true"><use href="#i-moon"></use></svg>
        </button>
      </div>
      <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-menu">
        <span></span><span></span><span></span>
      </button>
    </header>

    <div class="menu-backdrop" aria-hidden="true"></div>
    <nav class="menu-drawer" id="site-menu" aria-label="Main navigation" aria-hidden="true" inert>
      <div class="menu-drawer-header"><span class="menu-drawer-kicker">Portfolio navigation</span></div>
      <div class="menu-drawer-links">
        <a class="menu-drawer-link" href="%sservices/"><span class="menu-drawer-number" aria-hidden="true">01</span><span class="menu-drawer-copy"><strong>Services</strong><span>What I can design, build, and ship</span></span><svg class="icon menu-drawer-arrow" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
        <a class="menu-drawer-link" href="%sprojects/"><span class="menu-drawer-number" aria-hidden="true">02</span><span class="menu-drawer-copy"><strong>Projects</strong><span>Selected products and experiments</span></span><svg class="icon menu-drawer-arrow" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
        <a class="menu-drawer-link" href="%sarticles/"%s><span class="menu-drawer-number" aria-hidden="true">03</span><span class="menu-drawer-copy"><strong>Articles</strong><span>Long-form engineering guides</span></span><svg class="icon menu-drawer-arrow" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
        <a class="menu-drawer-link" href="%sblog/"%s><span class="menu-drawer-number" aria-hidden="true">04</span><span class="menu-drawer-copy"><strong>Blog</strong><span>Nepal money, marketing & tech guides</span></span><svg class="icon menu-drawer-arrow" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
      </div>
      <div class="menu-drawer-footer"><span class="menu-drawer-footnote">Have an idea worth building well?</span><a class="menu-drawer-cta" href="mailto:111abhishek.04367@gmail.com"><span>Start a conversation</span><svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a></div>
    </nav>

    <main id="main" class="content-section">
""" % (
        root, root, nav_top(root, active), root,
        root, root, root, ('aria-current="page"' if active == "articles" else ""),
        root, ('aria-current="page"' if active == "blog" else ""),
    )


def shell_close(root):
    return """    </main>

    <!-- Floating Bottom Navigation -->
    <nav class="bottom-nav" aria-label="Primary navigation">
      <a class="nav-item" href="%s" aria-label="Home"><svg class="icon" aria-hidden="true"><use href="#i-home"></use></svg></a>
      <a class="nav-item" href="%s#about" aria-label="About"><svg class="icon" aria-hidden="true"><use href="#i-user"></use></svg></a>
      <a class="nav-item" href="%sservices/" aria-label="Services"><svg class="icon" aria-hidden="true"><use href="#i-sparkles"></use></svg></a>
      <a class="nav-item" href="%sprojects/" aria-label="Projects"><svg class="icon" aria-hidden="true"><use href="#i-shield"></use></svg></a>
      <a class="nav-item" href="%sarticles/" aria-label="Articles"><svg class="icon" aria-hidden="true"><use href="#i-file-text"></use></svg></a>
      <a class="nav-item" href="%s#contact" aria-label="Contact"><svg class="icon" aria-hidden="true"><use href="#i-phone"></use></svg></a>
    </nav>
  </div>

  <script src="%sscript.js" defer></script>
  <script src="%sblog.js" defer></script>
</body>
</html>""" % (root, root, root, root, root, root, root, root)


def footer_block(root):
    return """      <footer class="site-footer">
        <span>&copy; 2026 Abhishek Thakur Barhi</span>
        <a href="%sservices/">Services</a>
        <a href="%sprojects/">Projects</a>
        <a href="%sarticles/">Articles</a>
        <a href="%sblog/">Blog</a>
        <a href="#main">Back to top<svg class="icon" aria-hidden="true"><use href="#i-arrow-up"></use></svg></a>
      </footer>""" % (root, root, root, root)


def ga_snippet():
    return """  <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LKDSVM9N74"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-LKDSVM9N74');
</script>
"""


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------
def md_to_html(body):
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    html_body = md.convert(body)
    html_body = add_heading_ids(html_body)
    return html_body


def add_heading_ids(html_body):
    def repl_h2(m):
        text = re.sub(r"<[^>]+>", "", m.group(1))
        slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")
        slug = slug or "section"
        return '<h2 id="%s">%s</h2>' % (slug, m.group(1))

    html_body = re.sub(r"<h2>(.*?)</h2>", repl_h2, html_body)
    return html_body


def reading_time(text):
    words = len(re.findall(r"\w+", text))
    return max(1, round(words / 210))


# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------
def related_cards(root, slugs, index):
    cards = []
    for s in slugs[:3]:
        e = index.get(s)
        if not e:
            continue
        cards.append(
            '<a class="card" href="%s%s/">%s'
            '<span class="label">%s</span>'
            '<h2>%s</h2>'
            '<span class="card-date">%s</span>'
            '<span class="card-action">Read guide<svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></span>'
            '</a>' % (
                root + "blog/", s, card_media(root, s),
                htmllib.escape(blog_data.CLUSTERS[e["cluster"]]),
                htmllib.escape(e["title"]),
                e.get("date", blog_data.PUBLISH_DATE),
            )
        )
    return "\n".join(cards)


def render_full_post(topic, index):
    slug = topic["slug"]
    path = os.path.join(CONTENT, slug + ".md")
    if not os.path.exists(path):
        return None
    raw = open(path, encoding="utf-8").read()
    fm, body = split_front_matter(raw)
    cluster = fm.get("category", topic["cluster"])
    title = fm.get("title", topic["title"])
    desc = fm.get("description", "")
    kw = fm.get("primary", topic["keyword"])
    secondary = fm.get("secondary", [])
    tags = fm.get("tags", [])
    date = fm.get("date", blog_data.PUBLISH_DATE)
    updated = fm.get("updated", date)
    faqs = fm.get("faqs", [])
    related = fm.get("related", [])
    og_image = fm.get("og_image", DEFAULT_REMOTE_IMAGE)
    featured = fm.get("featured_image", DEFAULT_REMOTE_IMAGE)
    if not str(og_image).startswith("https://"):
        og_image = DEFAULT_REMOTE_IMAGE
    if not str(featured).startswith("https://"):
        featured = DEFAULT_REMOTE_IMAGE

    body_html = md_to_html(body)
    minutes = reading_time(re.sub(r"<[^>]+>", "", body))
    root = "../../"
    canonical = "%s/blog/%s/" % (SITE, slug)
    cover = cover_for(slug)
    if cover:
        # curated, licensed cover wins over the generated text-card og_image
        og_abs = cover_og(cover)
        og_dims, og_alt = (1200, 675), cover.get("alt", title)
        image_ld = cover_image_object(cover, title)
    else:
        og_abs = og_image
        og_dims, og_alt = (1200, 630), None
        image_ld = og_abs
    figure_html = hero_cover_figure(root, slug) or (
        '          <figure class="article-featured">\n'
        '            <img src="%s" alt="%s" width="1200" height="675" loading="eager" fetchpriority="high" decoding="async" />\n'
        '          </figure>\n' % (featured, htmllib.escape(title)))

    date_fmt = human_date(date)
    updated_fmt = human_date(updated)

    # schema
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": canonical + "#webpage",
                "url": canonical,
                "name": title,
                "description": desc,
                "inLanguage": "en",
                "isPartOf": {"@id": SITE + "/#website"},
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                        {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                        {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                    ],
                },
            },
            {
                "@type": "BlogPosting",
                "@id": canonical + "#post",
                "headline": title,
                "description": desc,
                "image": image_ld,
                "datePublished": date,
                "dateModified": updated,
                "inLanguage": "en",
                "articleSection": blog_data.CLUSTERS[cluster],
                "author": {"@id": SITE + "/#person"},
                "publisher": {"@id": SITE + "/#person"},
                "mainEntityOfPage": canonical + "#webpage",
                "keywords": ", ".join([kw] + secondary),
                "isAccessibleForFree": True,
            },
            {"@type": "Person", "@id": SITE + "/#person", "name": blog_data.AUTHOR, "url": SITE + "/"},
        ],
    }
    if faqs:
        graph["@graph"].append({
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in faqs
            ],
        })
    graph["@graph"].append({
        "@type": "SpeakableSpecification",
        "cssSelector": ["h1", ".article-lede"],
    })
    schema_ld = '<script type="application/ld+json">%s</script>\n' % json.dumps(graph, ensure_ascii=False)

    tag_html = "\n".join('<span>%s</span>' % htmllib.escape(t) for t in tags)
    faq_html = ""
    if faqs:
        items = []
        for f in faqs:
            fid = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", f["q"].lower())).strip("-")
            items.append('<h3 id="faq-%s">%s</h3>\n<p>%s</p>' % (fid, htmllib.escape(f["q"]), htmllib.escape(f["a"])))
        faq_html = '<h2 id="faq">FAQ</h2>\n' + "\n".join(items)

    body_html = body_html + ("\n" + faq_html if faq_html else "")

    # AEO/GEO: a short, source-tagged "how to verify" block at the end of every full post.
    verify = blog_data.CLUSTER_CONTEXT.get(cluster, {}).get("verify") or \
        "Confirm the current rules, fees and what each provider supports before you rely on a specific number, because these change. This is general information, not financial, legal or medical advice."
    body_html += (
        '\n<h2 id="how-to-verify">Sources and how to verify</h2>\n'
        '<p>%s</p>' % htmllib.escape(verify))

    page = shell_head(root, title, desc, "index, follow, max-image-preview:large, max-snippet:-1", canonical, og_abs, "article", extra_ld=schema_ld, og_dims=og_dims, og_image_alt=og_alt or "")
    page += shell_body_open(root, "blog")
    page += """      <div class="article-shell">
        <div class="reading-progress" aria-hidden="true"></div>
        <nav class="breadcrumbs" aria-label="Breadcrumb"><ol>
          <li><a href="%s">Home</a></li>
          <li><a href="%sblog/">Blog</a></li>
          <li><a href="%sblog/category/%s/">%s</a></li>
          <li><span aria-current="page">%s</span></li>
        </ol></nav>

        <article class="article">
          <header class="article-head">
            <span class="chip">%s</span>
            <h1>%s</h1>
            <p class="article-lede">%s</p>
            <div class="article-meta">
              <img class="avatar" src="%sassets/abhishek-thakur-profile.jpeg" alt="" width="96" height="96" loading="eager" decoding="async" />
              <div>
                <a class="meta-name" href="%sabout/">Abhishek Thakur</a>
                <span class="meta-details">Published <time datetime="%s">%s</time> &middot; Updated <time datetime="%s">%s</time><span data-reading-time hidden>&middot; <span data-reading-minutes>%d</span> min read</span></span>
              </div>
            </div>
            <div class="article-share">
              <button class="share-btn" type="button" data-share="share" aria-label="Share this guide"><svg class="icon" aria-hidden="true"><use href="#i-share"></use></svg><span data-share-label>Share</span></button>
              <button class="share-btn" type="button" data-share="copy" aria-label="Copy link to this guide"><span data-share-label>Copy link</span></button>
            </div>
          </header>

%s

          <div class="article-layout">
            <div class="article-body" id="article-body">
%s
            </div>
            <aside class="sticky-rail">
              <nav id="toc" aria-label="On this page">
                <span class="rail-label">On this page</span>
                <ol class="toc-list" id="toc-list"></ol>
              </nav>
            </aside>
          </div>

          <footer class="article-foot">
            <div class="article-tags">%s</div>
            <div class="author-box">
              <img class="avatar" src="%sassets/abhishek-thakur-profile.jpeg" alt="Portrait of Abhishek Thakur" width="96" height="120" loading="lazy" decoding="async" />
              <div>
                <span class="author-name">Abhishek Thakur</span>
                <span class="author-role">Software Engineer &middot; Full Stack Developer &middot; Lahan, Nepal</span>
                <p class="author-bio">I take products from rough idea to reliable working experience &mdash; Django backend, React frontend, PostgreSQL and deployment. Currently completing a B.Tech in Computer Science at Parul University.</p>
                <div class="author-links">
                  <a href="%sabout/">About me<svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
                  <a href="%sservices/">Services<svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
                  <a href="%s#contact">Contact<svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
                </div>
              </div>
            </div>
          </footer>
        </article>
      </div>

      <div class="articles-shell">
        <section class="related" id="related">
          <span class="section-label">Keep reading</span>
          <h2>Related guides</h2>
          <div class="articles-grid related-grid">
%s
          </div>
        </section>
        <div class="articles-cta">
          <div>
            <span class="section-label">Need a hand?</span>
            <h2>Let&rsquo;s turn an <em>idea</em> into a plan.</h2>
            <p>Share what you are building and I&rsquo;ll help you choose the right technical and business decisions.</p>
          </div>
          <div class="cta-actions">
            <a class="cta-primary" href="%s#contact">Start a conversation<svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
            <a class="cta-secondary" href="%sservices/">Explore services</a>
          </div>
        </div>
      </div>
""" % (
        root, root, root, cluster, blog_data.CLUSTERS[cluster], htmllib.escape(title),
        blog_data.CLUSTERS[cluster], htmllib.escape(title), htmllib.escape(desc),
        root, root, date, date_fmt, updated, updated_fmt, minutes,
        figure_html,
        body_html,
        tag_html,
        root, root, root, root,
        related_cards(root, related, index),
        root, root,
    )
    page += footer_block(root)
    page += shell_close(root)
    page = page.replace("__GA__", ga_snippet())
    out_dir = os.path.join(OUT, slug)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
    return {"slug": slug, "title": title, "date": date}


def render_outline(topic, index):
    slug = topic["slug"]
    cluster = topic["cluster"]
    angle = topic.get("angle", "")
    root = "../../"
    canonical = "%s/blog/%s/" % (SITE, slug)
    cover = cover_for(slug)
    if cover:
        og_abs = cover_og(cover)
        og_dims, og_alt = (1200, 675), cover.get("alt", topic["title"])
        image_ld = cover_image_object(cover, topic["title"])
    else:
        og_abs = DEFAULT_REMOTE_IMAGE
        og_dims, og_alt = (1200, 630), None
        image_ld = og_abs
    figure_html = hero_cover_figure(root, slug, eager=False) or ""
    cluster_name = blog_data.CLUSTERS[cluster]

    base_title = topic["title"]
    kw = topic["keyword"]
    ctx = blog_data.CLUSTER_CONTEXT.get(cluster, {})
    actx = blog_data.ANGLE_CONTEXT.get(angle, {})
    suggested = blog_data._ANGLE_SUGGESTED.get(angle, "")
    learn = actx.get("learn", ["What this means for you", "The requirements you need", "A realistic process", "Mistakes to avoid", "Tools that work locally"])
    items = ctx.get("items", ["Confirm the current position with the relevant authority", "Keep a dated, sourced record at each step", "Match the method to your actual situation"])
    intro = ctx.get("intro", "This is a practical, Nepal-specific guide.")

    # de-duplicate the angle phrase out of the H1
    title = base_title

    learn_html = "\n".join("                <li>%s</li>" % htmllib.escape(l) for l in learn)
    items_html = "\n".join("                <li>%s</li>" % htmllib.escape(i) for i in items)

    # angle-specific FAQ (unique per page because kw varies)
    faqs = [
        {"q": "What should I check first about %s in Nepal?" % kw,
         "a": "Start with the documents and the current local position: %s" % htmllib.escape(items[0].lower())},
        {"q": "How much does %s typically cost?" % kw,
         "a": "It varies by scale and provider. Budget the whole cost, not the sticker, and confirm the current NPR figure with the relevant party before you commit."},
        {"q": "What is the most common mistake with %s?" % kw,
         "a": "Skipping the checks that are cheap to do early and expensive to undo. Keep a dated, sourced record at every step, and fix the paper trail before the money moves."},
        {"q": "Is %s different in Nepal than abroad?" % kw,
         "a": "Often yes: local rules, banks, platforms and connections shape it. Confirm the current local position before relying on a generic answer, because the local detail is usually what decides it."},
    ]
    faq_html = "\n".join(
        '                <h3>%s</h3>\n                <p>%s</p>' % (htmllib.escape(f["q"]), f["a"])
        for f in faqs)
    faq_ld = json.dumps({"@type": "FAQPage", "@id": canonical + "#faq",
                         "mainEntity": [{"@type": "Question", "name": f["q"],
                                         "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]})

    related = [t["slug"] + "/" for t in index_live(cluster, index)[:3]]
    rel_cards = related_cards(root, [r.rstrip("/") for r in related], index)

    schema_ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title,
         "description": intro, "inLanguage": "en",
         "isPartOf": {"@id": SITE + "/#website"},
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
             {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
             {"@type": "ListItem", "position": 3, "name": title, "item": canonical}]}},
        {"@type": "BlogPosting", "@id": canonical + "#post", "headline": title, "description": intro,
         "image": image_ld, "datePublished": blog_data.PUBLISH_DATE, "dateModified": blog_data.PUBLISH_DATE,
         "inLanguage": "en", "author": {"@id": SITE + "/#person"}, "publisher": {"@id": SITE + "/#person"},
         "mainEntityOfPage": canonical + "#webpage", "keywords": kw},
        {"@type": "Person", "@id": SITE + "/#person", "name": blog_data.AUTHOR, "url": SITE + "/"},
        json.loads(faq_ld),
    ]}, ensure_ascii=False)

    body = f"""              <p>{intro}</p>
              <h2 id="what-you-ll-learn">What you&rsquo;ll learn</h2>
              <ul>
{learn_html}
              </ul>
              <h2 id="key-points">Key points</h2>
              <ul>
{items_html}
              </ul>
              <h2 id="the-local-reality">The local reality</h2>
              <p>{intro.split('. ')[0].rstrip('.')} is not just a checklist: it is a set of local constraints, and the ones that matter are named in the key points above. The practical move is to confirm each one for your specific situation before you spend money, because the local detail is usually what decides the outcome.</p>
              <h2 id="how-to-approach">How to approach it</h2>
              <p>Work through: {htmllib.escape(suggested)}</p>
              <h2 id="related-guides">Related live guides</h2>
              <p>If you are ready to act, these are fully written, live in the same section:</p>
              <h2 id="faq">FAQ</h2>
{faq_html}
              <h2 id="verify">Verify before you rely on this</h2>
              <p>This is a practical, planned guide. Fees, limits and what each platform or bank supports change, so confirm the current position with the relevant authority or provider before you act. This is general information, not financial, legal or medical advice.</p>"""

    desc = intro
    schema_head = '<script type="application/ld+json">%s</script>\n' % schema_ld

    page = shell_head(root, title, desc, "index, follow, max-image-preview:large, max-snippet:-1", canonical, og_abs, "article", extra_ld=schema_head, og_dims=og_dims, og_image_alt=og_alt or "")
    page += shell_body_open(root, "blog")
    page += f"""      <div class="article-shell">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><ol>
          <li><a href="{root}">Home</a></li>
          <li><a href="{root}blog/">Blog</a></li>
          <li><a href="{root}blog/category/{cluster}/">{htmllib.escape(cluster_name)}</a></li>
          <li><span aria-current="page">{htmllib.escape(title)}</span></li>
        </ol></nav>

        <article class="article">
          <header class="article-head">
            <span class="chip">{htmllib.escape(cluster_name)}</span>
            <h1>{htmllib.escape(title)}</h1>
            <p class="article-lede">{htmllib.escape(desc)}</p>
            <div class="article-meta">
              <img class="avatar" src="{root}assets/abhishek-thakur-profile.jpeg" alt="" width="96" height="96" loading="eager" decoding="async" />
              <div>
                <a class="meta-name" href="{root}about/">Abhishek Thakur</a>
                <span class="meta-details">On schedule &middot; <time datetime="{blog_data.PUBLISH_DATE}">{human_date(blog_data.PUBLISH_DATE)}</time></span>
              </div>
            </div>
          </header>

{figure_html}

          <div class="article-layout">
            <div class="article-body" id="article-body">
              <blockquote class="planned-note"><strong>Full guide in progress.</strong> This planned guide for &ldquo;{htmllib.escape(title)}&rdquo; is on the writing schedule. The structure below is already live; the related guides are written today.</blockquote>
{body}
            </div>
            <aside class="sticky-rail">
              <nav id="toc" aria-label="On this page"><span class="rail-label">On this page</span><ol class="toc-list" id="toc-list"></ol></nav>
            </aside>
          </div>

          <footer class="article-foot">
            <div class="author-box">
              <img class="avatar" src="{root}assets/abhishek-thakur-profile.jpeg" alt="Portrait of Abhishek Thakur" width="96" height="120" loading="lazy" decoding="async" />
              <div>
                <span class="author-name">Abhishek Thakur</span>
                <span class="author-role">Software Engineer &middot; Lahan, Nepal</span>
                <div class="author-links">
                  <a href="{root}blog/">Browse the blog<svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
                  <a href="{root}#contact">Get in touch<svg class="icon" aria-hidden="true"><use href="#i-arrow-up-right"></use></svg></a>
                </div>
              </div>
            </div>
          </footer>
        </article>
      </div>

      <div class="articles-shell">
        <section class="related" id="related">
          <span class="section-label">Keep reading</span>
          <h2>Related guides</h2>
          <div class="articles-grid related-grid">
{rel_cards}
          </div>
        </section>
      </div>
"""
    page += footer_block(root)
    page += shell_close(root)
    page = page.replace("__GA__", ga_snippet())
    out_dir = os.path.join(OUT, slug)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)


def index_live(cluster, index):
    """Return 'live' topics in this cluster (full, or authored priority80)."""
    live = [t for t in ALL_TOPICS
            if t["cluster"] == cluster and (t["full"] or t["slug"] in PRIORITY80_SET)]
    live.sort(key=lambda t: t["slug"])
    return live


# ---------------------------------------------------------------------------
# Hub + category pages
# ---------------------------------------------------------------------------
def grid_card(root, t, index, kind):
    s = t["slug"]
    e = index.get(s)
    title = (e or {}).get("title", t["title"])
    cluster = (e or {}).get("cluster", t["cluster"])
    badge = "Published" if kind == "full" else "Planned"
    return ('<a class="card%s" href="%s%s/">%s<span class="label">%s</span>'
            '<h2>%s</h2><span class="card-badge %s">%s</span>'
            '<span class="card-action">%s</span></a>') % (
        " full" if kind == "full" else "", root + "blog/", s, card_media(root, s),
        htmllib.escape(blog_data.CLUSTERS[cluster]), htmllib.escape(title),
        "published" if kind == "full" else "planned", badge,
        "Read guide" if kind == "full" else "Planned")


def cluster_sections(root, index, full_by_cluster):
    blocks = []
    for key, name in blog_data.CLUSTERS.items():
        fulls = full_by_cluster.get(key, [])
        if not fulls:
            continue
        cards = "\n".join(grid_card(root, {"slug": f["slug"], "title": f["title"], "cluster": key, "kind": "full"}, index, "full") for f in fulls)
        blocks.append(
            '<details class="library-group" open><summary><span class="library-phase">%s</span>'
            '<span class="library-name">%s</span><span class="library-count">%d live guide%s</span></summary>'
            '<div class="articles-grid">%s</div></details>' % (
                key.upper(), htmllib.escape(name), len(fulls), "" if len(fulls) == 1 else "s", cards))
    return "\n".join(blocks)


def render_hub(index, fulls):
    root = "../"
    canonical = SITE + "/blog/"
    hub_cover = next((cluster_cover(key) for key in blog_data.CLUSTERS
                      if cluster_cover(key) is not None), None)
    if hub_cover:
        og_abs, og_dims, og_alt = cover_og(hub_cover), (1200, 675), hub_cover.get("alt", "")
    else:
        og_abs, og_dims, og_alt = DEFAULT_REMOTE_IMAGE, (1200, 675), ""
    full_by_cluster = {}
    for f in fulls:
        full_by_cluster.setdefault(f["cluster"], []).append(f)
    total = len(blog_data.build_all())
    page = shell_head(root, "Blog — Practical Guides for Money, Marketing & Tech in Nepal",
                      "Practical Nepal guides on dollar cards, freelancing, website development, digital marketing, business, career, travel and AI. %d topics, %d live guides." % (total, len(fulls)),
                      "index, follow, max-image-preview:large, max-snippet:-1", canonical, og_abs, "website", og_dims=og_dims, og_image_alt=og_alt)
    page += shell_body_open(root, "blog")
    page += """      <div class="articles-shell">
        <span class="section-label">Blog &middot; Nepal</span>
        <h1>Practical guides for earning, marketing and building in Nepal</h1>
        <p class="lede">Hands-on, Nepal-specific answers to the money questions: getting a dollar card, getting paid as a freelancer, choosing a web or marketing partner, and growing a local business online. Search the library or jump into a topic below.</p>

        <div class="blog-search" role="search">
          <input id="blog-search" type="search" placeholder="Search %d guides — try &ldquo;dollar card&rdquo; or &ldquo;freelance&rdquo;" aria-label="Search blog" autocomplete="off" />
        </div>
        <p class="blog-search-hint" id="blog-search-count" aria-live="polite"></p>

        <div id="blog-library">
%s
        </div>
        <p class="articles-support">Every live guide is written for the Nepali market, with local banks, platforms and costs. The %d remaining topics are on the writing schedule. New in the engineering notes: <a href="%sarticles/">Articles</a>.</p>
      </div>
""" % (
        total,
        cluster_sections(root, index, full_by_cluster),
        total - len(fulls), root,
    )
    page += footer_block(root)
    page += shell_close(root)
    page = page.replace("__GA__", ga_snippet())
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)


def render_category(key, name, index, fulls):
    root = "../../../"
    canonical = "%s/blog/category/%s/" % (SITE, key)
    cat_cover = cluster_cover(key)
    if cat_cover:
        og_abs, og_dims, og_alt = cover_og(cat_cover), (1200, 675), cat_cover.get("alt", "")
    else:
        og_abs, og_dims, og_alt = DEFAULT_REMOTE_IMAGE, (1200, 675), ""
    cluster_fulls = [f for f in fulls if f["cluster"] == key]
    cluster_fulls.sort(key=lambda f: f.get("date", ""), reverse=True)
    cards = "\n".join(grid_card(root, {"slug": f["slug"], "title": f["title"], "cluster": key, "kind": "full"}, index, "full") for f in cluster_fulls) if cluster_fulls else '<p class="library-empty">Live guides for this topic are coming soon.</p>'
    page = shell_head(root, "%s — Nepal Blog" % name, "All %s guides from the Abhishek Thakur blog, written for the Nepali market." % name,
                      "index, follow, max-image-preview:large, max-snippet:-1", canonical, og_abs, "website", og_dims=og_dims, og_image_alt=og_alt)
    page += shell_body_open(root, "blog")
    page += """      <div class="articles-shell">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><ol>
          <li><a href="%s">Home</a></li><li><a href="%sblog/">Blog</a></li><li><span aria-current="page">%s</span></li>
        </ol></nav>
        <span class="section-label">Category</span>
        <h1>%s</h1>
        <p class="lede">Every %s guide, from live articles to the planned backlog. Live guides are published; planned guides are on the writing schedule.</p>
        <div class="articles-grid">%s</div>
      </div>
%s""" % (root, root, htmllib.escape(name), htmllib.escape(name), htmllib.escape(name.lower()), cards, "")
    page += footer_block(root)
    page += shell_close(root)
    page = page.replace("__GA__", ga_snippet())
    cdir = os.path.join(OUT, "category", key)
    os.makedirs(cdir, exist_ok=True)
    open(os.path.join(cdir, "index.html"), "w", encoding="utf-8").write(page)


# ---------------------------------------------------------------------------
# search index / rss / sitemap
# ---------------------------------------------------------------------------
def write_search_index(index, fulls):
    rows = [
        {"slug": f["slug"], "title": f["title"], "kw": f.get("primary", ""), "cluster": f["cluster"]}
        for f in fulls
    ]
    for t in blog_data.build_all():
        if t["full"]:
            continue
        e = index.get(t["slug"])
        rows.append({"slug": t["slug"], "title": t["title"], "kw": t["keyword"], "cluster": t["cluster"]})
    with open(os.path.join(OUT, "search-index.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)


def write_rss(fulls):
    items = []
    for f in sorted(fulls, key=lambda x: x.get("date", ""), reverse=True):
        items.append(
            "    <item>\n"
            "      <title>%s</title>\n"
            "      <link>%s/blog/%s/</link>\n"
            "      <guid isPermaLink=\"true\">%s/blog/%s/</guid>\n"
            "      <description>%s</description>\n"
            "      <pubDate>%s</pubDate>\n"
            "    </item>" % (
                htmllib.escape(f["title"]), SITE, f["slug"], SITE, f["slug"],
                htmllib.escape(f.get("description", "")), rss_date(f.get("date", blog_data.PUBLISH_DATE))))
    feed = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Abhishek Thakur — Nepal Blog</title>
    <link>%s/blog/</link>
    <atom:link href="%s/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Practical Nepal guides on payments, freelancing, web development, marketing, business, career and AI.</description>
    <language>en</language>
    <lastBuildDate>%s</lastBuildDate>
%s
  </channel>
</rss>
""" % (SITE, SITE, rss_date(blog_data.PUBLISH_DATE), "\n".join(items))
    open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8").write(feed)


def _lastmod(slug, offset_days=0):
    from datetime import timedelta
    d = datetime.strptime(blog_data.PUBLISH_DATE, "%Y-%m-%d") - timedelta(days=(zlib.crc32(slug.encode()) % 90 + offset_days))
    return d.strftime("%Y-%m-%d")


def write_cluster_sitemaps(fulls):
    """Core sitemap (hub + 8 categories) + one sitemap per cluster + a sitemap index.

    All 1,000 post pages are indexable; waves are controlled by which cluster
    sitemaps are submitted to GSC, in the order given by OFFSITE-PLAYBOOK.md.
    """
    def url(loc, lm):
        return ("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
                "    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>" % (loc, lm))

    files = []
    # core: hub + categories
    rows = [url(SITE + "/blog/", blog_data.PUBLISH_DATE)]
    for key in blog_data.CLUSTERS:
        rows.append(url("%s/blog/category/%s/" % (SITE, key), blog_data.PUBLISH_DATE))
    _write_sitemap(os.path.join(ROOT, "sitemap-blog-core.xml"), "\n".join(rows))
    files.append("sitemap-blog-core.xml")

    # per-cluster (every post in that cluster, indexable)
    for key in blog_data.CLUSTERS:
        rows = [url("%s/blog/%s/" % (SITE, t["slug"]), _lastmod(t["slug"]))
                for t in ALL_TOPICS if t["cluster"] == key]
        _write_sitemap(os.path.join(ROOT, "sitemap-blog-%s.xml" % key), "\n".join(rows))
        files.append("sitemap-blog-%s.xml" % key)

    # index
    idx = "\n".join('    <sitemap>\n      <loc>%s</loc>\n    </sitemap>' % (SITE + "/" + f) for f in files)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + idx + "\n</sitemapindex>\n")
    open(os.path.join(ROOT, "sitemap-blog-index.xml"), "w", encoding="utf-8").write(xml)


def _write_sitemap(path, body):
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + body + "\n</urlset>\n")
    open(path, "w", encoding="utf-8").write(xml)


# ---------------------------------------------------------------------------
# OG images
# ---------------------------------------------------------------------------
def gen_og():
    """Keep image generation disabled; blog images are remote-only."""
    print("Skipping local OG image generation; using remote image URLs")
    return

    out_dir = os.path.join(ROOT, "assets", "blog")
    os.makedirs(out_dir, exist_ok=True)
    font_path = None
    fonts = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
             "/System/Library/Fonts/Supplemental/Arial.ttf",
             "/Library/Fonts/Arial Bold.ttf"]
    for p in fonts:
        if os.path.exists(p):
            font_path = p
            break
    def draw_card(path, cluster, title):
        img = Image.new("RGB", (1200, 630), CLUSTER_COLORS.get(cluster, "#111111"))
        d = ImageDraw.Draw(img)
        # subtle panel
        d.rectangle([0, 0, 1200, 14], fill="white")
        brand = "Abhishek Thakur  ·  Nepal Blog"
        f1 = ImageFont.truetype(font_path, 34) if font_path else ImageFont.load_default()
        f2 = ImageFont.truetype(font_path, 30) if font_path else ImageFont.load_default()
        d.text((64, 70), brand, font=f2, fill="white")
        # wrapped title
        words = title.split()
        lines, cur = [], ""
        for w in words:
            if len(cur) + len(w) > 34:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        y = 250
        for ln in lines[:4]:
            d.text((64, y), ln, font=f1, fill="white")
            y += 56
        d.text((64, 560), "abhishek-thakur.com.np/blog", font=f2, fill=(255, 255, 255))
        img.save(path, "JPEG", quality=82)

    for t in blog_data.MONEY_POSTS:
        e = CONTENT_TITLE.get(t["slug"], "")
        if e:
            draw_card(os.path.join(out_dir, t["slug"] + ".jpg"), t["cat"], e)
    draw_card(os.path.join(out_dir, "default.jpg"), "payments", "Practical guides for money, marketing and tech in Nepal")
    print("OG images:", len(blog_data.MONEY_POSTS) + 1)


# ---------------------------------------------------------------------------
# front matter
# ---------------------------------------------------------------------------
def split_front_matter(text):
    fm = {}
    body = text
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        body = text[m.end():]
    return fm, body


def human_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return d.strftime("%b %d, %Y").replace(" 0", " ")


def rss_date(iso):
    from email.utils import formatdate
    d = datetime.strptime(iso, "%Y-%m-%d")
    import time
    t = time.mktime(d.timetuple())
    return formatdate(timeval=t, localtime=False)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
CONTENT_TITLE = {}


def main():
    global CONTENT_TITLE
    # index for cross-linking / related; titles from content where present
    index = {}
    fulls = []
    for t in ALL_TOPICS:
        index[t["slug"]] = {"slug": t["slug"], "title": t["title"], "cluster": t["cluster"], "date": blog_data.PUBLISH_DATE}
    for t in ALL_TOPICS:
        p = os.path.join(CONTENT, t["slug"] + ".md")
        if os.path.exists(p):
            fm, _ = split_front_matter(open(p, encoding="utf-8").read())
            e = {"slug": t["slug"], "title": fm.get("title", t["title"]), "cluster": t["cluster"],
                 "primary": fm.get("primary", t["keyword"]), "date": fm.get("date", blog_data.PUBLISH_DATE),
                 "updated": fm.get("updated", fm.get("date", blog_data.PUBLISH_DATE)),
                 "description": fm.get("description", ""), "related": fm.get("related", [])}
            fulls.append(e)
            index[t["slug"]] = {"slug": t["slug"], "title": e["title"], "cluster": e["cluster"], "date": e["date"]}
            CONTENT_TITLE[t["slug"]] = e["title"]

    gen_og()

    for t in ALL_TOPICS:
        if os.path.exists(os.path.join(CONTENT, t["slug"] + ".md")):
            render_full_post(t, index)
        else:
            render_outline(t, index)

    render_hub(index, fulls)
    for key, name in blog_data.CLUSTERS.items():
        render_category(key, name, index, fulls)
    write_search_index(index, fulls)
    write_rss(fulls)
    write_cluster_sitemaps(fulls)

    print("Live (full) posts: %d  |  upgraded outlines: %d  |  sitemaps: core + 8 clusters + index"
          % (len(fulls), len(ALL_TOPICS) - len(fulls)))


if __name__ == "__main__":
    main()
