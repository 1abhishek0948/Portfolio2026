# Off-Site Playbook — Getting the Nepal Guides Ranked

On-site work (SEO + AEO + GEO + all 1,000 guides indexable) is in the repo.
Ranking head terms needs the off-site levers below. You run these; I built the assets.

Ground truth to expect: new `.com.np` domain, low authority. Long-tail should move
in ~6-12 weeks; head terms ("digital marketing agency nepal", "website development
company nepal") take 6-12 months of links + consistency. No one can promise #1.

## 1. Google Search Console (week 1)
1. Add `abhishek-thakur.com.np` as a domain property; verify.
2. Submit these sitemaps (already in robots.txt):
   - https://www.abhishek-thakur.com.np/sitemap.xml
   - https://www.abhishek-thakur.com.np/sitemap-blog-index.xml
3. Request Indexing on the money pages first:
   - /blog/ , /blog/local-seo-kathmandu-businesses/ , /blog/how-to-get-dollar-card-nepal/
   - /blog/how-to-start-freelancing-nepal/ , /blog/digital-marketing-agency-nepal/
4. Set up a monthly note: Coverage -> Pages "Crawled - not indexed", "Duplicate,
   generic", and any "Scaled content abuse" report.

## 2. Sitemap waves (submit these sitemaps in order, ~2 weeks apart)
The index references 8 per-cluster sitemaps. In GSC, add them by wave so Google
discovers them in stages instead of a 1,000-page dump:
- Wave 1: sitemap-blog-payments.xml, sitemap-blog-freelancing.xml, sitemap-blog-marketing.xml
- Wave 2: sitemap-blog-web.xml, sitemap-blog-business.xml
- Wave 3: sitemap-blog-career.xml, sitemap-blog-ai.xml, sitemap-blog-travel.xml
- Core (anytime): sitemap-blog-core.xml

## 3. De-risk escape hatch
If GSC flags a cluster for scaled/duplicate content, back it off to noindex and drop
its sitemap from the active set:
    python3 tools/set_cluster_noindex.py <cluster>        # e.g. "travel"
Re-enable later with the "index" argument.

## 4. Links (10-20 quality links over 6 months)
The link engine is the data asset: /digital-pr/ (the Nepal cost & method index).
Pitch it, not the portfolio. Targets:
- Local business/tech directories and Lahan/Siraha listings (NAP-consistent).
- Guest posts on Nepali business, dev and marketing blogs.
- Partnerships: co-hosted tools/roundups with local dev shops, universities, fintech.
- Original-data PR: "Nepal Web & Freelance Cost Index" -> pitch to local business
  media and dev communities for the cited numbers.
Do NOT buy links or join link farms; those are the "duplicate/scam" signal that
suppresses the whole domain.

## 5. Entity + citations (GEO)
- Keep /llms.txt and /GEMINI.md current (they hold the citation facts + entity block).
- Keep NAP consistent everywhere (home, /about/, /services/, directories, GBP if you open one).
- sameAs is wired to GitHub/LinkedIn/Instagram in the homepage JSON-LD; keep them live.

## 6. Measurement (monthly)
- GSC: indexed pages, impressions, clicks, average position, and which queries the
  money pages are up for.
- Snippets/AI answers: spot-check whether the site shows in Google AI Overviews and in
  ChatGPT/Perplexity for 3-5 key questions (e.g. "dollar card nepal", "how do nepali
  freelancers get paid"). Note the source it cites.
- Ranks: update content/blog/keyword-tracker.csv monthly.
- Core Web Vitals: watch LCP on the blog (images are the usual culprit).

## 7. Content cadence
- 5 more guides/week from the queue in content/blog/QUEUE.md, authored then indexable.
- Refresh the 20 money guides when a fee/limit changes (the "Sources & how to verify"
  block is the spot to update).
