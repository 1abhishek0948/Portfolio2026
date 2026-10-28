#!/usr/bin/env python3
# Copyright-compliant blog cover sourcing.
#
# For every blog topic family (~118), find a freely licensed, topic-relevant
# cover photo, produce 16:9 WebP derivatives (1200 / 800 / 480 px) and write
# assets/blog/covers/manifest.json with source URL, creator and license.
#
# Sources (in order):
#   1. Wikimedia Commons API  - keyless, full license metadata, resizes for us.
#   2. Openverse API (Fallback) - restricted to CC0 / PDM / CC BY / CC BY-SA.
#
# License policy: CC0, Public Domain / PDM, CC BY*, CC BY-SA* only.
# Never NC / ND / GFDL / non-free. Credits are NEVER fabricated: every field
# comes verbatim from the provider API.

import json
import os
import re
import sys
import time
import html as html_mod
import ssl
import urllib.request
import urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "tools"))
import blog_data  # noqa: E402

OUT_DIR = os.path.join(BASE, "assets", "blog", "covers")
MANIFEST = os.path.join(OUT_DIR, "manifest.json")

UA = "PortfolioCoverBot/1.0 (personal blog abhishek-thakur.com.np; contact: 111abhishek.04367@gmail.com)"
CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem")

LICENSE_WHITELIST = re.compile(
    r"^(cc0|public domain|pdm|pd\b|pd[- ].*|cc by(-sa)?( \d+(\.\d+)?)?)$", re.I
)

# Title substrings that disqualify a candidate as a photo cover.
BANNED = [
    "map", "logo", "icon", "diagram", "screenshot", "coat of arms", "seal of",
    "flag of", "poster", "cover", "clipart", "cartoon", "catalog", "postage",
]

THUMB_WIDTH = 1200
SIZES = [(1200, 80), (800, 80), (480, 78)]

SUFFIXES = [
    "-2026-guide", "-common-mistakes", "-cost-and-pricing", "-faq",
    "-for-beginners", "-in-kathmandu", "-pros-and-cons", "-step-by-step",
    "-tools-and-resources",
]


def family_of(slug):
    root = slug
    for s in SUFFIXES:
        if root.endswith(s) and len(root) > len(s):
            root = root[: -len(s)]
            break
    return root


COVER_STEM_CACHE = {}


def build_family_map():
    """slug -> family root, family list grouped by cluster."""
    fam = {}
    order = []
    for t in blog_data.build_all():
        f = family_of(t["slug"])
        if f not in fam:
            fam[f] = []
            order.append(f)
        fam[f].append(t["slug"])
    return fam, order


# ---------------------------------------------------------------------------
# Curated search queries per family.
# q: list of Commons queries tried in order. Empty/failed -> Openverse with
#    the same queries (minus the filetype filter).
# alt: fallback alt text if the image title is too filename-ish.
# pref: exact Commons file to try first (brand logos etc.).
# ---------------------------------------------------------------------------
COVER_SPECS = {
    # ---------------- payments (14 base + 6 money) ----------------
    "bank-account-for-freelancers": {"q": ["bank branch Nepal building", "Nepal Investment Bank"], "alt": "A bank branch in Nepal"},
    "best-bank-dollar-card-nepal": {"q": ["Nepal rupee banknote", "US dollar banknotes"], "alt": "Nepali rupee banknotes fanned out"},
    "cross-border-payments-nepal": {"q": ["currency exchange counter money", "foreign currency banknotes"], "alt": "Currency exchange counter with banknotes"},
    "debit-vs-credit-card-nepal": {"q": ["credit card payment terminal", "paying with credit card"], "alt": "A card being used at a payment terminal"},
    "digital-payment-gateways-nepal": {"q": ["eSewa logo"], "alt": "eSewa logo", "pref": "File:Esewa logo.webp", "allow_logo": True},
    "dollar-card-charges-nepal": {"q": ["US dollar banknotes", "hundred dollar bills close up"], "alt": "US dollar banknotes", "provider": "commons"},
    "esewa-vs-khalti": {"q": ["eSewa logo"], "alt": "eSewa logo", "pref": "File:Esewa logo.webp", "allow_logo": True},
    "freelance-income-tax-nepal": {"q": ["tax form calculator", "income tax return form"], "alt": "Tax forms with calculator"},
    "how-to-get-dollar-card-nepal": {"q": ["credit card close up", "visa credit card"], "alt": "Plastic payment cards close up"},
    "ime-pay-guide": {"q": ["mobile money transfer", "mobile wallet phone"], "alt": "Mobile money transfer on a smartphone"},
    "mero-share-account": {"q": ["Nepal Stock Exchange", "stock exchange building India"], "alt": "A stock exchange building", "provider": "openverse"},
    "nepse-investing-basics": {"q": ["stock market chart screen", "financial chart monitor"], "alt": "Stock market chart on a screen"},
    "nrb-dollar-card-rules-nepal": {"q": ["Nepal Rastra Bank", "rupee banknote Nepal"], "alt": "Nepal Rastra Bank building"},
    "nrb-foreign-currency-rules": {"q": ["Nepal Rastra Bank building", "US dollar banknotes"], "alt": "Nepal Rastra Bank building"},
    "pay-foreign-hosting-from-nepal": {"q": ["data center server racks", "server room"], "alt": "Server racks in a data center"},
    "paypal-alternatives-nepal": {"q": ["PayPal logo"], "alt": "PayPal logo", "pref": "File:PayPal-Logo-2022.png", "allow_logo": True},
    "personal-income-tax-nepal": {"q": ["tax documents calculator form", "income tax paperwork desk"], "alt": "Tax paperwork and a calculator on a desk", "provider": "openverse"},
    "prabhu-pay-guide": {"q": ["mobile payment phone", "qr code payment"], "alt": "Making a mobile payment with a phone"},
    "receiving-remittance-nepal": {"q": ["giving cash to person", "handing money family"], "alt": "Cash handed over to a family member", "provider": "openverse"},
    "sending-money-abroad-from-nepal": {"q": ["bank transfer money", "money exchange converter"], "alt": "Money transfer concept photograph"},

    # ---------------- freelancing (14 base + 5 money) ----------------
    "avoid-freelance-scams": {"q": ["phishing computer identity theft", "padlock security"], "alt": "A padlock representing online security"},
    "best-freelance-jobs-nepal-students": {"q": ["students laptops studying campus", "student laptop study"], "alt": "Students studying with laptops", "provider": "openverse"},
    "client-communication-habits": {"q": ["video call laptop meeting", "business video conference laptop"], "alt": "A video call meeting on a laptop", "provider": "openverse"},
    "consistent-online-income-nepal": {"q": ["home office desk laptop", "work from home desk"], "alt": "A home office desk with a laptop"},
    "freelance-contracts-nepal": {"q": ["signing contract pen document", "sign document"], "alt": "Signing a contract with a pen"},
    "freelance-time-management": {"q": ["time management planner clock", "hourglass laptop desk"], "alt": "A clock and planner on a workspace desk", "provider": "openverse"},
    "freelancing-portfolio": {"q": ["design portfolio laptop", "website design portfolio screen"], "alt": "A design portfolio open on a laptop", "provider": "openverse"},
    "freelancing-pricing": {"q": ["calculator money invoice desk", "pricing calculator laptop"], "alt": "A calculator with money on a desk", "provider": "openverse"},
    "freelancing-proposals": {"q": ["laptop typing keyboard hands", "writing laptop"], "alt": "Hands typing on a laptop keyboard"},
    "high-demand-freelance-niches": {"q": ["programmer workstation monitors", "coding laptop desk"], "alt": "A programmer's multi-monitor workstation", "provider": "openverse"},
    "how-freelancers-nepal-get-paid": {"q": ["Nepal rupee banknote", "Nepalese banknotes"], "alt": "Nepali rupee banknotes"},
    "how-to-start-freelancing-nepal": {"q": ["Kathmandu laptop cafe", "person working laptop cafe"], "alt": "Working on a laptop in a cafe in Nepal"},
    "leading-remote-teams-nepal": {"q": ["team meeting video conference screen", "office team collaboration"], "alt": "A remote team joining over video conference"},
    "remote-jobs-for-nepalese": {"q": ["remote work home office", "laptop home working"], "alt": "Working remotely from a home office"},
    "selling-on-fiverr-nepal": {"q": ["gig economy freelancer laptop", "freelance creative workspace"], "alt": "A freelancer's creative workspace", "provider": "openverse"},
    "top-freelance-platforms-nepal": {"q": ["laptop marketplace website", "online job search laptop"], "alt": "Browsing an online marketplace on a laptop"},
    "top-specialist-platforms": {"q": ["software engineer laptop code", "developer laptop coding"], "alt": "A software engineer coding on a laptop", "provider": "openverse"},
    "upwork-profile-optimization": {"q": ["job search laptop", "resume desk laptop"], "alt": "Job searching on a laptop at a desk"},
    "upwork-to-nepali-bank-account": {"q": ["Nepal bank branch money", "Nepali banknote"], "alt": "Nepali banknotes"},

    # ---------------- web (12 base + 4 money) ----------------
    "accessible-website-checklist": {"q": ["braille reading hands", "accessible keyboard"], "alt": "Hands reading Braille", "provider": "openverse"},
    "choosing-web-tech-stack": {"q": ["programming code colorful screen", "code editor screen"], "alt": "Colorful programming code on a screen"},
    "custom-web-application-development-nepal": {"q": ["code editor screen", "software developer laptop code"], "alt": "A developer's code editor on a laptop", "provider": "openverse"},
    "ecommerce-website-development-nepal": {"q": ["online shopping laptop boxes", "ecommerce laptop package"], "alt": "An online store open on a laptop", "provider": "openverse"},
    "fast-website-nepal-network": {"q": ["network cables router", "fiber optic internet"], "alt": "Network cables plugged into a router"},
    "hire-freelance-web-developer-nepal": {"q": ["job interview handshake office", "client meeting laptop"], "alt": "A client meeting in an office", "provider": "openverse"},
    "landing-pages-that-convert": {"q": ["digital marketing laptop phone analytics", "marketing workspace laptop"], "alt": "A digital marketing workspace", "provider": "openverse"},
    "mobile-first-low-bandwidth": {"q": ["person smartphone field travel", "traveler using phone road"], "alt": "A traveler browsing on a smartphone", "provider": "openverse"},
    "registering-com-np-domain": {"q": ["keyboard typing close up", "typing hands keyboard"], "alt": "Hands typing on a keyboard", "provider": "openverse"},
    "static-site-vs-cms": {"q": ["code editor screen programming", "developer code editor laptop"], "alt": "A code editor with programming code", "provider": "openverse"},
    "web-hosting-in-nepal": {"q": ["data center server racks"], "alt": "Server racks in a data center"},
    "website-development-company-nepal": {"q": ["tech office team collaboration", "startup team office meeting"], "alt": "A startup team collaborating in an office", "provider": "openverse"},
    "website-maintenance-nepal": {"q": ["laptop repair screwdriver tools", "computer repair"], "alt": "Repair tools next to an open laptop"},
    "website-security-checklist": {"q": ["padlock laptop", "cyber security padlock"], "alt": "A padlock beside a laptop"},
    "when-to-redesign-website": {"q": ["website design concept laptop", "modern website design screen"], "alt": "A modern website design on a laptop", "provider": "openverse"},
    "wordpress-vs-custom": {"q": ["laptop code editor screen", "wordpress laptop screen"], "alt": "A code editor open on a laptop"},

    # ---------------- marketing (12 base + 5 money) ----------------
    "basic-seo-audit-nepal": {"q": ["google analytics laptop", "analytics laptop screen"], "alt": "Web analytics chart on a laptop"},
    "best-digital-marketing-company-nepal": {"q": ["marketing team whiteboard planning", "digital marketing team office"], "alt": "A marketing team planning at a whiteboard", "provider": "openverse"},
    "brand-voice-nepal": {"q": ["brand identity design color palette", "branding design desk"], "alt": "Brand identity design materials on a desk", "provider": "openverse", "pref_url": "https://live.staticflickr.com/65535/54517849410_c013e94b32_b"},
    "content-marketing-strategy": {"q": ["content writing notebook laptop", "writer notebook coffee"], "alt": "Writing content in a notebook beside a laptop"},
    "digital-marketing-agency-nepal": {"q": ["digital marketing office laptop", "modern creative office desk"], "alt": "A modern creative office workspace"},
    "digital-marketing-services-price-nepal": {"q": ["marketing budget calculator laptop", "accounting calculator invoice"], "alt": "A calculator over invoices and marketing documents", "provider": "openverse"},
    "earning-backlinks-nepal": {"q": ["metal chain links macro", "chain links close up"], "alt": "Interlocking metal chain links", "provider": "openverse"},
    "email-marketing-nepal": {"q": ["email inbox laptop", "envelope laptop desk"], "alt": "An email inbox open on a laptop", "provider": "openverse"},
    "facebook-ads-nepal": {"q": ["social media apps smartphone", "instagram phone hand"], "alt": "Social media apps on a smartphone", "provider": "openverse"},
    "ga4-measurement-nepal": {"q": ["analytics dashboard laptop", "google analytics dashboard screen"], "alt": "An analytics dashboard on a laptop", "provider": "openverse"},
    "google-ads-nepal": {"q": ["search engine laptop screen", "online advertising laptop"], "alt": "Search marketing work on a laptop", "provider": "openverse"},
    "local-seo-chitwan-terai": {"q": ["Bharatpur Chitwan city", "Chitwan district town"], "alt": "Bharatpur city in Chitwan, Nepal", "provider": "commons"},
    "local-seo-kathmandu-businesses": {"q": ["Kathmandu street shops", "Asan Kathmandu market"], "alt": "Street shops in Kathmandu"},
    "local-seo-patan-kathmandu": {"q": ["Patan Durbar Square", "Patan Nepal street"], "alt": "Patan Durbar Square in Kathmandu"},
    "on-page-seo-nepal": {"q": ["html code screen", "code editor html monitor"], "alt": "HTML source code on a monitor"},
    "social-media-marketing-agency-kathmandu": {"q": ["smartphone photography social", "phone social network hand"], "alt": "Using a social network on a phone"},
    "youtube-marketing-nepal": {"q": ["video camera content creator", "content creation camera ring light"], "alt": "A content creator's video setup", "provider": "openverse"},

    # ---------------- business (10 base) ----------------
    "business-website-essentials": {"q": ["shop sign Kathmandu street", "Nepal shop front"], "alt": "The front of a small shop in Nepal"},
    "e-invoicing-nepal": {"q": ["invoice tablet receipt desk", "digital invoice laptop"], "alt": "An invoice shown on a tablet", "provider": "openverse"},
    "ecommerce-logistics-nepal": {"q": ["delivery rider packages courier", "courier delivery boxes"], "alt": "A courier delivery rider with packages", "provider": "openverse"},
    "online-store-cost-nepal": {"q": ["online shopping cart laptop", "shopping boxes laptop"], "alt": "An online shopping cart on a laptop"},
    "pan-registration-nepal": {"q": ["official document stamp seal", "paperwork files desk"], "alt": "Stamped official paperwork on a desk"},
    "payment-gateway-setup": {"q": ["payment terminal checkout", "card payment machine"], "alt": "A card payment terminal at a checkout"},
    "private-limited-company-nepal": {"q": ["Kathmandu office building", "corporate glass building"], "alt": "An office building in Kathmandu"},
    "professional-invoices-nepal": {"q": ["invoice documents calculator", "accounting paperwork desk"], "alt": "Invoices and paperwork with a calculator", "provider": "openverse"},
    "sole-proprietorship-nepal": {"q": ["market stall vendor Nepal", "small shop Nepal owner"], "alt": "A vendor at a market stall in Nepal"},
    "vat-registration-nepal": {"q": ["Nepal tax office building", "government office Nepal paperwork"], "alt": "A government office in Nepal", "provider": "openverse"},

    # ---------------- career (12 base) ----------------
    "cs-internships-nepal": {"q": ["internship office young professionals", "intern working computer office"], "alt": "Interns working in an office", "provider": "openverse"},
    "cs-skill-roadmap": {"q": ["career planning whiteboard goals", "study roadmap notebook desk"], "alt": "A planning board for a career roadmap", "provider": "openverse"},
    "first-junior-dev-job-nepal": {"q": ["young programmer laptop", "developer laptop desk"], "alt": "A programmer working on a laptop"},
    "it-colleges-nepal": {"q": ["Pulchowk Engineering Campus", "university building Nepal"], "alt": "An engineering campus in Nepal", "provider": "commons"},
    "lok-sewa-computer-officer": {"q": ["exam hall students", "writing exam desk"], "alt": "Students taking an exam"},
    "pte-ielts-score-guide": {"q": ["exam paper pencil test", "english study dictionary"], "alt": "Answer sheet and pencil for an exam"},
    "study-in-australia-from-nepal": {"q": ["Sydney Opera House", "Melbourne skyline"], "alt": "The Sydney Opera House"},
    "study-in-europe-from-nepal": {"q": ["Prague old town", "European city street architecture"], "alt": "A historic European city street"},
    "study-in-japan-from-nepal": {"q": ["Tokyo Shibuya street", "Kyoto temple Japan"], "alt": "A busy street in Tokyo"},
    "technical-interview-prep": {"q": ["office meeting laptop discussion", "two programmers whiteboard"], "alt": "A technical discussion at a whiteboard"},
    "tribhuvan-kathmandu-pokhara-university": {"q": ["Kathmandu University", "Pulchowk campus building"], "alt": "A university building in the Kathmandu Valley", "provider": "commons"},
    "us-study-visa-from-nepal": {"q": ["USA Independence Hall", "White House Washington"], "alt": "A landmark in the United States", "provider": "openverse"},

    # ---------------- travel (12 base) ----------------
    "annapurna-base-camp-trek": {"q": ["Annapurna mountain range Nepal", "Machapuchare Annapurna"], "alt": "The Annapurna mountain range in Nepal"},
    "chhath-puja-traditions": {"q": ["Chhath puja", "diya lamps river festival"], "alt": "Lamps lit for Chhath Puja at a river"},
    "chitwan-wildlife-tour": {"q": ["Chitwan rhinoceros", "one horned rhinoceros Nepal"], "alt": "A rhinoceros in Chitwan National Park"},
    "dashain-traveler-guide": {"q": ["Dashain Nepal festival", "bamboo swing Nepal linge ping"], "alt": "A traditional Dashain bamboo swing in Nepal"},
    "everest-base-camp-trek": {"q": ["Everest Base Camp trek", "Mount Everest Nepal"], "alt": "Mount Everest seen from the Base Camp trail", "pref": "File:Everest, Himalayas.jpg"},
    "langtang-valley-trek": {"q": ["Langtang valley trek", "Langtang Lirung"], "alt": "The Langtang valley with Langtang Lirung above"},
    "mardi-himal-trek": {"q": ["Mardi Himal", "Mardi Himal trail"], "alt": "The Mardi Himal trek trail"},
    "nagarkot-weekend-trip": {"q": ["Nagarkot sunrise", "Nagarkot Himalayas"], "alt": "Sunrise over the Himalayas from Nagarkot"},
    "nepali-homestay-stays": {"q": ["Ghandruk village", "Nepal traditional village house"], "alt": "A traditional village homestay in Nepal"},
    "pokhara-weekend-trip": {"q": ["Phewa Lake Pokhara boats", "Pokhara lakeside"], "alt": "Boats on Phewa Lake in Pokhara"},
    "tihar-deepavali-guide": {"q": ["Tihar festival Nepal", "rangoli oil lamps Nepal"], "alt": "Oil lamps lit for Tihar in Nepal"},
    "upper-mustang-permit": {"q": ["Upper Mustang", "Lo Manthang"], "alt": "The walled city of Lo Manthang in Upper Mustang"},

    # ---------------- ai (12 base) ----------------
    "ai-content-and-seo": {"q": ["digital technology laptop screen", "tech workspace laptop desk"], "alt": "AI-powered content creation on a laptop", "provider": "openverse"},
    "ai-tools-for-digital-marketing-nepal": {"q": ["digital marketing analytics laptop", "data dashboard phone"], "alt": "A marketing analytics dashboard"},
    "ai-tools-for-freelancers-nepal": {"q": ["ai technology laptop abstract", "neural network technology"], "alt": "AI tools on a laptop workspace", "provider": "openverse"},
    "ai-website-builders-nepal": {"q": ["website development laptop screen", "web development laptop"], "alt": "Website development on a laptop", "provider": "openverse"},
    "chatgpt-for-small-business": {"q": ["chat assistant laptop business", "smart assistant phone workspace"], "alt": "Using an AI assistant on a laptop", "provider": "openverse"},
    "customer-chatbots-nepal": {"q": ["customer support headset laptop", "support agent headset"], "alt": "A customer support agent wearing a headset", "provider": "openverse"},
    "digital-transformation-smb": {"q": ["small business owner laptop Nepal", "tablet shop counter"], "alt": "A small business owner using a tablet at the counter"},
    "human-ai-content-workflow": {"q": ["hand writing notebook pen", "human robot hands"], "alt": "A hand writing next to a keyboard"},
    "llms-for-nepali-text": {"q": ["Devanagari script signboard", "Nepali language book"], "alt": "Devanagari script on a signboard in Nepal"},
    "seo-trends-in-nepal": {"q": ["business growth chart laptop", "analytics charts laptop desk"], "alt": "Growth charts on a laptop screen", "provider": "openverse"},
    "simple-business-automation": {"q": ["workstation office automation", "digital business desk tools"], "alt": "A modern small-business workstation", "provider": "openverse"},
    "tech-trends-nepal-2026": {"q": ["Kathmandu city modern view", "Kathmandu rooftop view"], "alt": "A modern view over Kathmandu city"},
}

# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------

def _get(url, timeout=40, retries=3):
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            if attempt < retries:
                time.sleep(4 + attempt * 5)
    raise last


def strip_html(s):
    s = html_mod.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()


def commons_search(q, limit=18):
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
           "&generator=search&gsrnamespace=6&gsrlimit=%d&gsrsearch=%s"
           "&prop=imageinfo&iiprop=url%%7Csize%%7Cmime%%7Cextmetadata&iiurlwidth=%d"
           % (limit, urllib.parse.quote(q), THUMB_WIDTH))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        d = json.load(r)
    pages = (d.get("query", {}).get("pages") or {})
    out = []
    for p in sorted(pages.values(), key=lambda x: x.get("index", 999)):
        ii = (p.get("imageinfo") or [{}])[0]
        if not ii:
            continue
        em = ii.get("extmetadata", {})
        lic = strip_html((em.get("LicenseShortName") or {}).get("value", ""))
        lic_url = strip_html((em.get("LicenseUrl") or {}).get("value", ""))
        artist_html = (em.get("Artist") or {}).get("value", "")
        m = re.search(r'href="([^"]+)"', artist_html or "")
        artist_url = ("https:" + m.group(1)) if m and m.group(1).startswith("//") \
            else (m.group(1) if m else "")
        out.append({
            "title": p.get("title", ""),
            "url": ii.get("url", ""),
            "thumburl": ii.get("thumburl") or ii.get("url", ""),
            "width": ii.get("width", 0),
            "height": ii.get("height", 0),
            "mime": ii.get("mime", ""),
            "license": lic,
            "license_url": lic_url or "",
            "creator": strip_html(artist_html) or "Unknown creator",
            "creator_url": artist_url,
            "desc_url": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p.get("title", "").replace(" ", "_"), safe=":/%"),
            "provider": "Wikimedia Commons",
            "src_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p.get("title", "").replace(" ", "_"), safe=":/%"),
        })
    return out


OV_LICENSE_URL = {
    "cc0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "pdm": "https://creativecommons.org/publicdomain/mark/1.0/",
}


def openverse_search(q, limit=20):
    q2 = re.sub(r"\s*\bfiletype:bitmap\b\s*", " ", q).strip() or "photography"
    qs = urllib.parse.urlencode({
        "q": q2, "page_size": limit, "license": "cc0,pdm,by,by-sa",
        "mature": "false",
    })
    data = _get("https://api.openverse.org/v1/images/?%s" % qs, timeout=40)
    d = json.loads(data.decode("utf-8"))
    out = []
    for r in d.get("results", []):
        v = (r.get("license_version") or "").replace(".0", "").strip()
        lic = r.get("license", "")
        if lic == "by":
            name = "CC BY %s" % v
        elif lic == "by-sa":
            name = "CC BY-SA %s" % v
        elif lic == "cc0":
            name = "CC0"
        elif lic == "pdm":
            name = "Public Domain Mark"
        else:
            continue
        lic_url = r.get("license_url") or OV_LICENSE_URL.get(lic, "")
        out.append({
            "title": r.get("title") or "Untitled",
            "url": r.get("url", ""),
            "thumburl": r.get("url", ""),
            "width": r.get("width") or 0,
            "height": r.get("height") or 0,
            "mime": "image/png" if r.get("url", "").lower().endswith(".png") else "image/jpeg",
            "license": name,
            "license_url": lic_url,
            "creator": r.get("creator") or "Unknown creator",
            "creator_url": r.get("creator_url") or "",
            "desc_url": r.get("foreign_landing_url") or "",
            "provider": "Openverse (%s)" % (r.get("source") or ""),
            "src_page": r.get("foreign_landing_url") or "",
        })
    return out


def passes(entry, allow_logo=None):
    allowed_logo = allow_logo or []
    title = html_mod.unescape(entry["title"]).replace("File:", "").replace("_", " ").lower()
    for word in BANNED:
        if word in title and not any(a.lower() in title for a in allowed_logo):
            return False
    if entry["mime"] not in ("image/jpeg", "image/png", "image/webp"):
        return False
    if not LICENSE_WHITELIST.match(entry["license"].strip()):
        return False
    w, h = entry["width"], entry["height"]
    if not w or not h:
        return False
    if w < 950 or h < 460:
        return False
    return True


def score(entry):
    w, h = entry["width"], entry["height"]
    aspect = w / float(h)
    if 1.25 <= aspect <= 2.05:
        s = 1.0
    elif 1.05 <= aspect < 1.25 or 2.05 < aspect <= 2.6:
        s = 0.55
    elif 0.9 <= aspect < 1.05:
        s = 0.35
    else:
        s = 0.0
    s += min(w, 4000) / 4000.0 * 0.8
    lic = entry["license"].lower()
    s += 0.15 if (lic.startswith("cc0") or lic.startswith("public domain") or lic == "pd") else 0.0
    return s


def choose(entries, allow_logo=None, pref_url=None, max_rank=6):
    """Pick the best of the first few RELEVANT results only.

    Commons/Openverse search order is relevance; scoring all 18 results let a
    nicely-sized but off-topic photo from rank 12 win (e.g. hockey players for
    a web-developer topic). Candidates are capped to the first `max_rank`
    results that pass the hard filters, then ranked by aspect/size.
    """
    if pref_url:
        for e in entries:
            if e["url"] == pref_url or e["desc_url"] == pref_url:
                if passes(e, allow_logo):
                    return e
    pool = [e for e in entries if passes(e, allow_logo)][:max_rank]
    best, best_s = None, -1.0
    for i, e in enumerate(pool):
        s = score(e) - i * 0.03
        if s > best_s:
            best, best_s = e, s
    return best


# ---------------------------------------------------------------------------
# Image processing
# ---------------------------------------------------------------------------
def crop_to_169(img):
    from PIL import Image
    w, h = img.size
    target = 16 / 9.0
    if w > h * target:
        cw = int(round(h * target))
        x0 = (w - cw) // 2
        img = img.crop((x0, 0, x0 + cw, h))
    else:
        ch = int(round(w / target))
        y0 = max(0, (h - ch) // 2 - int(h * 0.02))  # nudge up: keep sky/subjects
        y0 = min(y0, h - ch)
        img = img.crop((0, y0, w, y0 + ch))
    return img.convert("RGB")


def cover_stem(family, entry):
    """Stable family-based filename; a ?v=hash query in the manifest busts caches."""
    return re.sub(r"[^a-z0-9_-]", "", family).lower().strip("-")


def process(family, entry, force=False):
    from PIL import Image
    import io
    stem = cover_stem(family, entry)
    names = [f"{stem}.webp", f"{stem}-800.webp", f"{stem}-480.webp"]
    paths = {w: os.path.join(OUT_DIR, n) for (w, _), n in zip(SIZES, names)}
    if not force and all(os.path.exists(p) and os.path.getsize(p) > 400 for p in paths.values()):
        return paths, "cached"
    raw = _get(entry["thumburl"] or entry["url"], timeout=25)
    img = Image.open(io.BytesIO(raw))
    img.load()
    img = crop_to_169(img)
    for (w, q) in SIZES:
        path = paths[w]
        if img.size[0] >= w:
            out = img.resize((w, int(w * 9 / 16)), Image.LANCZOS)
        else:
            out = img  # original smaller than the target — keep native size
        out.save(path, "WEBP", quality=q, method=6)
        if not os.path.exists(path) or os.path.getsize(path) < 400:
            raise RuntimeError("WebP derivative failed to write: %s" % path)
    return paths, "written"


def clean_title_alt(entry, fallback):
    t = html_mod.unescape(entry["title"]).replace("File:", "")
    t = re.sub(r"\.(jpe?g|png|webp|JPE?G|PNG|WEBP)$", "", t).replace("_", " ")
    t = re.sub(r"[-—]+\s*$", "", re.sub(r"\b(19|20)\d{2}\b", "", t))  # drop year noise
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) >= 8 and re.search(r"[A-Za-z]", t):
        # still filename-ish when the only separators were dashes/underscores
        return t.replace("-", " ").replace("  ", " ").strip()
    return fallback


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def _write_manifest(manifest, fam_map, todo_all):
    """Write manifest.json (covers + full slug mapping + _meta). Idempotent."""
    for fam, slugs in fam_map.items():
        if fam in manifest["covers"]:
            manifest["mapping"][fam] = fam
    for slug in blog_data.build_all():
        f = family_of(slug["slug"])
        if f in manifest["covers"]:
            manifest["mapping"][slug["slug"]] = f
    # normalize cache-busting version hashes (entries written by older runs)
    import hashlib
    for fam, e in manifest["covers"].items():
        if not e.get("version"):
            key = e.get("image_url") or e.get("title") or e.get("source_url") or fam
            e["version"] = hashlib.md5(key.encode("utf-8")).hexdigest()[:8]
    manifest["_meta"] = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "policy": "CC0 / Public Domain / PDM / CC BY / CC BY-SA only; no NC, ND or non-free images",
        "sizes": "1200x675, 800x450, 480x270 WebP (16:9 center crop)",
        "filename_versioning": "stable family-based filenames; the 'version' hash appended as ?v= busts the immutable /assets cache when a source image changes",
        "attribution_note": "source_url, creator, creator_url, license and license_url are verbatim provider metadata",
    }
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1, sort_keys=True)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated family names")
    ap.add_argument("--force", action="store_true", help="re-download/rewrite even if present")
    ap.add_argument("--no-openverse", action="store_true")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    fam_map, order = build_family_map()

    manifest = {"covers": {}, "mapping": {}}
    if os.path.exists(MANIFEST):
        try:
            existing = json.load(open(MANIFEST, encoding="utf-8"))
            for fam, e in existing.get("covers", {}).items():
                paths_ok = all(
                    os.path.exists(os.path.join(OUT_DIR, f)) for f in
                    (e.get("files_1200", ""), e.get("files_800", ""), e.get("files_480", "")))
                if not args.force or paths_ok:
                    manifest["covers"][fam] = e
            manifest["mapping"] = dict(existing.get("mapping") or {})
        except Exception:  # noqa: BLE001
            pass
    todo = order if not args.only else [f.strip() for f in args.only.split(",")]
    missing = []
    log = []

    for fam in todo:
        if args.only is None and fam in manifest["covers"]:
            continue
        spec = COVER_SPECS.get(fam)
        if spec is None:
            log.append("SKIP no-spec %s" % fam)
            missing.append(fam)
            continue
        entry = None
        tried = []
        provider = spec.get("provider", "auto")  # auto | commons | openverse
        pref_url = spec.get("pref_url")
        if spec.get("pref") and provider != "openverse":
            try:
                url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
                       "&titles=%s&prop=imageinfo&iiprop=url%%7Csize%%7Cmime%%7Cextmetadata&iiurlwidth=%d"
                       % (urllib.parse.quote(spec["pref"]), THUMB_WIDTH))
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
                    d = json.load(r)
                page = next(iter((d.get("query", {}).get("pages") or {}).values()))
                ii = (page.get("imageinfo") or [{}])[0]
                em = ii.get("extmetadata", {})
                cand = {
                    "title": spec["pref"], "url": ii.get("url", ""),
                    "thumburl": ii.get("thumburl") or ii.get("url", ""),
                    "width": ii.get("width", 0), "height": ii.get("height", 0),
                    "mime": ii.get("mime", ""),
                    "license": strip_html((em.get("LicenseShortName") or {}).get("value", "")),
                    "license_url": strip_html((em.get("LicenseUrl") or {}).get("value", "")),
                    "creator": strip_html((em.get("Artist") or {}).get("value", "")) or "Unknown creator",
                    "creator_url": "",
                    "desc_url": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(spec["pref"].replace(" ", "_")),
                    "provider": "Wikimedia Commons",
                    "src_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(spec["pref"].replace(" ", "_")),
                }
                if cand["thumburl"] and passes(cand, ["logo"] if spec.get("allow_logo") else None):
                    entry = cand
            except Exception as e:  # noqa: BLE001
                log.append("pref-failed %s: %s" % (fam, e))
        if entry is None and provider in ("auto", "commons"):
            for q in spec["q"][:2]:
                try:
                    res = commons_search(q)
                    tried.append(q)
                except Exception as e:  # noqa: BLE001
                    log.append("commons-error %s (%s): %s" % (fam, q, e))
                    time.sleep(3)
                    res = []
                entry = choose(res, ["logo"] if spec.get("allow_logo") else None, pref_url=pref_url)
                if entry is None and q != spec["q"][-1]:
                    time.sleep(0.4)
                    continue
                if entry is not None:
                    break
                time.sleep(0.4)
        if entry is None and not args.no_openverse and provider in ("auto", "openverse"):
            for q in spec["q"][:2]:
                try:
                    res = openverse_search(q)
                except Exception as e:  # noqa: BLE001
                    log.append("openverse-error %s (%s): %s" % (fam, q, e))
                    res = []
                entry = choose(res, pref_url=pref_url)
                if entry is not None:
                    break
                time.sleep(4)
        if entry is None:
            missing.append(fam)
            log.append("MISSING %s (tried: %s)" % (fam, "; ".join(tried)))
            continue
        try:
            _, status = process(fam, entry, force=args.force)
        except Exception as e:  # noqa: BLE001
            log.append("process-error %s: %s" % (fam, e))
            missing.append(fam)
            continue
        alt = clean_title_alt(entry, spec["alt"])
        stem = cover_stem(fam, entry)
        import hashlib
        version = hashlib.md5(((entry.get("url") or entry.get("image_url") or entry["title"])).encode("utf-8")).hexdigest()[:8]
        manifest["covers"][fam] = {
            "file": stem + ".webp",
            "files_1200": stem + ".webp",
            "files_800": stem + "-800.webp",
            "files_480": stem + "-480.webp",
            "version": version,
            "alt": alt,
            "title": entry["title"],
            "provider": entry["provider"],
            "source_url": entry["src_page"],
            "image_url": entry["url"],
            "creator": entry["creator"],
            "creator_url": entry["creator_url"],
            "license": entry["license"],
            "license_url": entry["license_url"],
            "status": status,
        }
        log.append("OK %-42s %s | %s | %s | %dx%d" % (
            fam, entry["provider"], entry["license"], entry["creator"], entry["width"], entry["height"]))
        _write_manifest(manifest, fam_map, todo_all=order)
        time.sleep(0.35)

    _write_manifest(manifest, fam_map, todo_all=order)
    print("\n".join(log))
    print("\ncovered: %d / %d families" % (len(manifest["covers"]), len(order)))
    if missing:
        print("MISSING families (%d): %s" % (len(missing), ", ".join(missing)))


if __name__ == "__main__":
    main()
