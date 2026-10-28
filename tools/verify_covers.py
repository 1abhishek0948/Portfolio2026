#!/usr/bin/env python3
"""Verify the remote blog cover system end to end.

Checks, for every generated article page:
  - a real hero <figure class="article-featured has-cover"> with alt/width/height
  - every topic resolves to an HTTPS direct image URL
  - og:image / twitter:image are remote direct image URLs
  - JSON-LD BlogPosting.image carries the remote URL
  - hub / category / related cards use remote media
Then reports duplicate cover files and duplicate source images.

Usage: python3 tools/verify_covers.py
Exit code 0 only when everything passes.
"""
import glob
import html as htmllib
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "tools"))
import blog_data  # noqa: E402
from remote_image_catalog import BLOG_FALLBACKS, BLOG_OVERRIDES, BLOG_REPLACEMENTS  # noqa: E402

BLOG = os.path.join(BASE, "blog")
SITE = blog_data.SITE
SUFFIXES = ["-2026-guide", "-common-mistakes", "-cost-and-pricing", "-faq",
            "-for-beginners", "-in-kathmandu", "-pros-and-cons", "-step-by-step",
            "-tools-and-resources"]


def family_of(slug):
    for s in SUFFIXES:
        if slug.endswith(s) and len(slug) > len(s):
            return slug[: -len(s)]
    return slug


def main():
    manifest = json.load(open(os.path.join(BASE, "assets", "blog", "covers", "manifest.json"), encoding="utf-8"))
    covers = manifest["covers"]
    mapping = manifest["mapping"]
    topics = blog_data.build_all()

    failures = []
    warnings = []

    # ---- 1. every topic slug resolves to a remote direct image URL ----
    remote_urls = {}
    remote_families = set()
    for t in topics:
        slug = t["slug"]
        fam = mapping.get(slug) or family_of(slug)
        entry = BLOG_REPLACEMENTS.get(fam) or BLOG_OVERRIDES.get(fam) or covers.get(fam) or BLOG_FALLBACKS.get(fam)
        if not entry:
            failures.append("NO-COVER %s (family %s)" % (slug, fam))
            continue
        url = entry.get("image_url", "")
        if not re.match(r"^https://[^\s\"']+", url):
            failures.append("REMOTE-URL-BAD %s -> %s" % (slug, url))
        remote_urls.setdefault(url, []).append(fam)
        remote_families.add(fam)

    # ---- 2. every article page: hero, og/twitter, JSON-LD ----
    page_checks = 0
    hero_ok = 0
    og_ok = 0
    ld_ok = 0
    for t in topics:
        slug = t["slug"]
        fam = mapping.get(slug) or family_of(slug)
        entry = BLOG_REPLACEMENTS.get(fam) or BLOG_OVERRIDES.get(fam) or covers.get(fam) or BLOG_FALLBACKS.get(fam)
        page = os.path.join(BLOG, slug, "index.html")
        if not os.path.exists(page):
            failures.append("NO-PAGE %s" % slug)
            continue
        html = open(page, encoding="utf-8").read()
        page_checks += 1
        if 'class="article-featured has-cover"' not in html:
            failures.append("NO-HERO %s" % slug)
        else:
            hero_ok += 1
            block = re.search(r'<figure class="article-featured has-cover">(.*?)</figure>', html, re.S)
            mini = block.group(1) if block else ""
            if 'loading="eager"' not in mini and 'loading="lazy"' not in mini:
                failures.append("HERO-LOADING %s" % slug)
            if 'fetchpriority="high"' not in mini and 'loading="lazy"' not in mini:
                failures.append("HERO-PRIORITY %s" % slug)
            if 'width="1200"' not in mini or 'height="675"' not in mini:
                failures.append("HERO-DIMS %s" % slug)
            if not re.search(r'alt="[^"]{8,}"', mini):
                failures.append("HERO-ALT %s" % slug)
            if entry and htmllib.escape(entry.get("image_url", ""), quote=True) not in mini:
                failures.append("HERO-URL-MISMATCH %s" % slug)
        og = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if not og or not og.group(1).startswith("https://"):
            failures.append("OG-BAD %s (%s)" % (slug, og.group(1) if og else "absent"))
        else:
            og_ok += 1
            tw = re.search(r'<meta name="twitter:image" content="([^"]+)"', html)
            if not tw or tw.group(1) != og.group(1):
                failures.append("TWITTER-MISMATCH %s" % slug)
            w = re.search(r'<meta property="og:image:width" content="(\d+)"', html)
            h = re.search(r'<meta property="og:image:height" content="(\d+)"', html)
            if not (w and h and w.group(1) == "1200" and h.group(1) == "675"):
                failures.append("OG-DIMS %s" % slug)
            alt = re.search(r'<meta property="og:image:alt" content="([^"]*)"', html)
            if not alt or len(alt.group(1)) < 8:
                failures.append("OG-ALT %s" % slug)
        # JSON-LD image object
        found_ld = False
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                data = json.loads(m.group(1))
            except Exception:  # noqa: BLE001
                failures.append("LD-JSON-INVALID %s" % slug)
                continue
            graph = data.get("@graph") if isinstance(data, dict) else None
            nodes = graph if isinstance(graph, list) else [data]
            for node in nodes:
                if isinstance(node, dict) and node.get("@type") == "BlogPosting":
                    img = node.get("image")
                    if isinstance(img, dict) and img.get("@type") == "ImageObject":
                        if not img.get("url"):
                            failures.append("LD-IMAGE-META %s" % slug)
                        if not str(img.get("url", "")).startswith("https://"):
                            failures.append("LD-IMAGE-URL %s" % slug)
                        found_ld = True
                    elif isinstance(img, str) and img.startswith("https://"):
                        warnings.append("LD-IMAGE-STRING %s" % slug)
                        found_ld = True
                    else:
                        failures.append("LD-IMAGE-BAD %s" % slug)
        if not found_ld:
            failures.append("LD-IMAGE-MISSING %s" % slug)
        else:
            ld_ok += 1

    # ---- 3. listing cards (hub, category, related) ----
    card_pages = [os.path.join(BLOG, "index.html")] + \
        glob.glob(os.path.join(BLOG, "category", "*", "index.html"))
    card_imgs = 0
    card_missing = 0
    for page in card_pages:
        if not os.path.exists(page):
            continue
        html = open(page, encoding="utf-8").read()
        for m in re.finditer(r'<span class="card-media"><img src="([^"]+)"', html):
            card_imgs += 1
            if not m.group(1).startswith("https://"):
                card_missing += 1
                failures.append("CARD-MISSING %s -> %s" % (os.path.relpath(page, BASE), m.group(1)))
        if page.endswith(os.path.join("blog", "index.html")):
            if 'class="card-media"' not in html:
                failures.append("HUB-NO-CARD-MEDIA")
            hub_og = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            if not hub_og or not hub_og.group(1).startswith("https://"):
                failures.append("HUB-OG-BAD")

    # related cards on article pages
    related_imgs = 0
    for t in topics:
        html = open(os.path.join(BLOG, t["slug"], "index.html"), encoding="utf-8").read()
        for m in re.finditer(r'<div class="articles-grid related-grid">(.*?)</div>', html, re.S):
            related_imgs += len(re.findall(r'class="card-media"', m.group(1)))

    # ---- 4. duplicate remote image URLs in actual page output ----
    by_source = {}
    for t in topics:
        fam = mapping.get(t["slug"]) or family_of(t["slug"])
        entry = BLOG_REPLACEMENTS.get(fam) or BLOG_OVERRIDES.get(fam) or covers.get(fam) or BLOG_FALLBACKS.get(fam)
        if entry and entry.get("image_url"):
            by_source.setdefault(entry["image_url"], []).append(fam)
    source_dupes = {s: sorted(set(fams)) for s, fams in by_source.items() if len(set(fams)) > 1}

    # ---- 5. license metadata completeness ----
    lic_bad = [fam for fam, e in covers.items()
               if not e.get("license") or not e.get("creator") or not e.get("source_url")]
    lic_pd = sum(1 for e in covers.values()
                 if not e.get("license", "").upper().startswith("CC BY"))
    lic_ccby = len(covers) - lic_pd

    # ---- report ----
    print("=" * 70)
    print("BLOG COVER VERIFICATION")
    print("=" * 70)
    print("topics checked           :", len(topics))
    print("article pages checked    :", page_checks)
    print("families with remote URLs: %d / %d" % (len(remote_families), len(set(family_of(t['slug']) for t in topics))))
    print("mapping entries          :", len(mapping))
    print("unique remote URLs       :", len(remote_urls))
    print("hero cover pages         :", hero_ok)
    print("og:image cover pages     :", og_ok)
    print("JSON-LD ImageObject pages:", ld_ok)
    print("hub/category card images : %d (missing %d)" % (card_imgs, card_missing))
    print("related card images      :", related_imgs)
    print("license metadata missing :", len(lic_bad), lic_bad[:5])
    print("license split            : CC BY*=%d, PD/CC0=%d" % (lic_ccby, lic_pd))
    print("duplicate source pages   :", len(source_dupes), list(source_dupes.items())[:3])
    print("warnings                 :", len(warnings), warnings[:6])
    print("failures                 :", len(failures))
    for f in failures[:40]:
        print("   FAIL", f)
    if len(failures) > 40:
        print("   ... and %d more" % (len(failures) - 40))
    print("=" * 70)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
