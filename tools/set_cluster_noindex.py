#!/usr/bin/env python3
"""De-risk escape hatch: if Google flags a cluster for scaled/duplicate content,
flip that cluster's post pages back to noindex (and out of active sitemaps).

Usage:
    python3 tools/set_cluster_noindex.py payments
    python3 tools/set_cluster_noindex.py payments freelancing
    python3 tools/set_cluster_noindex.py payments index   # re-enable

Reads cluster->slug mapping from tools/blog_data.py and rewrites the generated
blog/<slug>/index.html robots meta. Idempotent.
"""
import os
import sys
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blog_data

INDEXED = 'name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"'
NOINDEX = 'name="robots" content="noindex, follow"'


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return
    clusters = [a for a in argv if a in blog_data.CLUSTERS]
    action = "index" if "index" in argv else "noindex"
    if not clusters:
        print("No valid cluster. Valid:", ", ".join(blog_data.CLUSTERS))
        return

    slugs = {t["slug"] for t in blog_data.ALL_TOPICS if t["cluster"] in clusters}
    flipped = 0
    for slug in slugs:
        p = os.path.join(ROOT, "blog", slug, "index.html")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if action == "noindex":
            s = s.replace(INDEXED, NOINDEX)
        else:
            s = s.replace(NOINDEX, INDEXED)
        open(p, "w", encoding="utf-8").write(s)
        flipped += 1
    print("%s -> %s on %d pages: %s" % (clusters, action, flipped, ", ".join(clusters)))
    if action == "noindex":
        print("Also remove this cluster from your active GSC sitemaps until resolved.")


if __name__ == "__main__":
    main()
