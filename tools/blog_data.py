# Central dataset for the 1,000-page Nepal blog library.
# 20 "money" posts are written in full (indexed). The remaining 980 are
# noindex outline pages generated from 98 base topics x 10 angles.

SITE = "https://abhishek-thakur.com.np"
AUTHOR = "Abhishek Thakur"
PUBLISH_DATE = "2026-10-27"

CLUSTERS = {
    "payments": "Digital Payments & Finance",
    "freelancing": "Freelancing & Remote Work",
    "web": "Web Development & Tech",
    "marketing": "Digital Marketing & SEO",
    "business": "Business & E-commerce",
    "career": "Career & Education",
    "travel": "Travel & Lifestyle",
    "ai": "AI & Emerging Tech",
}

# The 20 fully-written, indexed money posts. Each key matches a Markdown
# file under content/blog/<slug>.md
MONEY_POSTS = [
    {"slug": "how-to-get-dollar-card-nepal", "cat": "payments", "kw": "how to get dollar card in nepal"},
    {"slug": "dollar-card-charges-nepal", "cat": "payments", "kw": "dollar card charges in nepal"},
    {"slug": "best-bank-dollar-card-nepal", "cat": "payments", "kw": "best bank for dollar card in nepal"},
    {"slug": "nrb-dollar-card-rules-nepal", "cat": "payments", "kw": "nrb dollar card limit"},
    {"slug": "pay-foreign-hosting-from-nepal", "cat": "payments", "kw": "how to pay for foreign hosting from nepal"},
    {"slug": "paypal-alternatives-nepal", "cat": "payments", "kw": "paypal alternative in nepal"},
    {"slug": "how-to-start-freelancing-nepal", "cat": "freelancing", "kw": "how to start freelancing in nepal"},
    {"slug": "best-freelance-jobs-nepal-students", "cat": "freelancing", "kw": "best freelance jobs in nepal for students"},
    {"slug": "how-freelancers-nepal-get-paid", "cat": "freelancing", "kw": "how freelancers in nepal get paid"},
    {"slug": "top-freelance-platforms-nepal", "cat": "freelancing", "kw": "top freelance platforms working in nepal"},
    {"slug": "upwork-to-nepali-bank-account", "cat": "freelancing", "kw": "transfer money from upwork to nepali bank account"},
    {"slug": "website-development-company-nepal", "cat": "web", "kw": "website development company in nepal"},
    {"slug": "ecommerce-website-development-nepal", "cat": "web", "kw": "e-commerce website development nepal"},
    {"slug": "custom-web-application-development-nepal", "cat": "web", "kw": "custom web application development nepal"},
    {"slug": "hire-freelance-web-developer-nepal", "cat": "web", "kw": "how to hire a freelance web developer in nepal"},
    {"slug": "digital-marketing-agency-nepal", "cat": "marketing", "kw": "digital marketing agency nepal"},
    {"slug": "best-digital-marketing-company-nepal", "cat": "marketing", "kw": "best digital marketing company in nepal"},
    {"slug": "digital-marketing-services-price-nepal", "cat": "marketing", "kw": "digital marketing services price in nepal"},
    {"slug": "social-media-marketing-agency-kathmandu", "cat": "marketing", "kw": "social media marketing agency kathmandu"},
    {"slug": "local-seo-kathmandu-businesses", "cat": "marketing", "kw": "local seo kathmandu"},
]

# 98 base topics expanded x10 angles = 980 noindex outline pages.
# Each entry: (slug, title, keyword, cluster)
BASE_TOPICS = [
    # ---- payments (14) ----
    ("esewa-vs-khalti", "eSewa vs Khalti: Which Nepali Wallet Should You Use?", "esewa vs khalti", "payments"),
    ("ime-pay-guide", "IME Pay and eSewa IME: A Guide to Nepali Wallets", "ime pay nepal", "payments"),
    ("prabhu-pay-guide", "PrabhuPay for Business: Setup and Everyday Use", "prabhu pay business", "payments"),
    ("mero-share-account", "MeroShare Account and Demat Registration in Nepal", "mero share account nepal", "payments"),
    ("nepse-investing-basics", "NEPSE Investing Basics for Beginners", "nepse investing basics", "payments"),
    ("personal-income-tax-nepal", "Personal Income Tax in Nepal: Brackets and Filing", "income tax nepal", "payments"),
    ("freelance-income-tax-nepal", "Freelance Income Tax in Nepal: What Freelancers Owe", "freelance tax nepal", "payments"),
    ("receiving-remittance-nepal", "Receiving Remittance in Nepal: Methods and Fees", "remittance to nepal", "payments"),
    ("sending-money-abroad-from-nepal", "Sending Money Abroad from Nepal", "send money abroad from nepal", "payments"),
    ("cross-border-payments-nepal", "Cross-Border Payments from Nepal to the US and EU", "cross border payments nepal", "payments"),
    ("bank-account-for-freelancers", "Opening a Bank Account for Freelance Income in Nepal", "bank account for freelancers nepal", "payments"),
    ("debit-vs-credit-card-nepal", "Debit vs Credit Cards in Nepal: Which You Need", "debit vs credit card nepal", "payments"),
    ("nrb-foreign-currency-rules", "NRB Foreign Currency Rules for Residents and Business", "nrb foreign currency rules", "payments"),
    ("digital-payment-gateways-nepal", "eSewa, Khalti and IME Pay Gateway APIs for Developers", "payment gateway api nepal", "payments"),
    # ---- freelancing (14) ----
    ("freelancing-portfolio", "How to Build a Freelancing Portfolio That Wins Clients", "freelancing portfolio nepal", "freelancing"),
    ("freelancing-proposals", "Writing Freelance Proposals That Get You Hired", "freelance proposal writing", "freelancing"),
    ("freelance-contracts-nepal", "Freelance Contracts and Payment Terms for Nepali Freelancers", "freelance contract nepal", "freelancing"),
    ("freelancing-pricing", "How to Price Your Freelance Work in Nepal and Abroad", "freelance pricing nepal", "freelancing"),
    ("upwork-profile-optimization", "Upwork Profile Optimization for New Nepali Freelancers", "upwork profile optimization", "freelancing"),
    ("selling-on-fiverr-nepal", "Selling on Fiverr from Nepal: Gigs, Levels and Fees", "fiverr nepal", "freelancing"),
    ("top-specialist-platforms", "Top Specialist Platforms for Nepali Developers", "top freelance platforms nepal", "freelancing"),
    ("remote-jobs-for-nepalese", "Finding Remote Jobs from Nepal: Ten Real Sources", "remote jobs nepal", "freelancing"),
    ("high-demand-freelance-niches", "High-Demand Freelance Niches for Nepali Developers", "freelance niches nepal", "freelancing"),
    ("avoid-freelance-scams", "How to Spot and Avoid Freelance Client Scams", "freelance scams nepal", "freelancing"),
    ("freelance-time-management", "Managing Time and Deadlines as a Nepali Freelancer", "freelance time management", "freelancing"),
    ("client-communication-habits", "Client Communication Habits That Build Repeat Business", "client communication freelancing", "freelancing"),
    ("consistent-online-income-nepal", "Building a Consistent Online Income in Nepal", "online income nepal", "freelancing"),
    ("leading-remote-teams-nepal", "Leading Remote Teams from Nepal", "remote team management nepal", "freelancing"),
    # ---- web (12) ----
    ("web-hosting-in-nepal", "Web Hosting in Nepal: Local vs International Providers", "web hosting nepal", "web"),
    ("registering-com-np-domain", "Registering a .com.np Domain with Mercantile", "com np domain nepal", "web"),
    ("wordpress-vs-custom", "WordPress vs Custom Development for Nepali Businesses", "wordpress vs custom nepal", "web"),
    ("fast-website-nepal-network", "Making Your Website Fast on Nepal's Network", "fast website nepal", "web"),
    ("website-security-checklist", "Website Security Checklist for Nepali Businesses", "website security nepal", "web"),
    ("accessible-website-checklist", "Building an Accessible Website: A Practical Checklist", "accessible website", "web"),
    ("website-maintenance-nepal", "Website Maintenance and Retainers in Nepal", "website maintenance nepal", "web"),
    ("when-to-redesign-website", "When to Redesign Your Business Website", "website redesign", "web"),
    ("landing-pages-that-convert", "Landing Pages That Convert Nepali Visitors", "landing page conversion", "web"),
    ("mobile-first-low-bandwidth", "Mobile-First Design for Low-Bandwidth Nepal", "mobile first design nepal", "web"),
    ("static-site-vs-cms", "Static Site vs CMS: Choosing the Right Stack", "static site vs cms", "web"),
    ("choosing-web-tech-stack", "Choosing the Right Tech Stack for a Nepali Web Project", "web tech stack nepal", "web"),
    # ---- marketing (12) ----
    ("basic-seo-audit-nepal", "How to Run a Basic SEO Audit for a Nepali Site", "seo audit nepal", "marketing"),
    ("on-page-seo-nepal", "On-Page SEO for Nepali Websites", "on page seo nepal", "marketing"),
    ("earning-backlinks-nepal", "Earning Backlinks for Nepali Businesses", "backlinks nepal", "marketing"),
    ("content-marketing-strategy", "Content Marketing Strategy for Nepali Businesses", "content marketing nepal", "marketing"),
    ("email-marketing-nepal", "Email Marketing That Works in Nepal", "email marketing nepal", "marketing"),
    ("youtube-marketing-nepal", "YouTube Marketing for Nepali Brands", "youtube marketing nepal", "marketing"),
    ("google-ads-nepal", "Running Google Ads in Nepal Within NRB Limits", "google ads nepal", "marketing"),
    ("facebook-ads-nepal", "Facebook and Instagram Ads for Nepali Businesses", "facebook ads nepal", "marketing"),
    ("ga4-measurement-nepal", "Measuring Marketing Results with GA4 in Nepal", "ga4 analytics nepal", "marketing"),
    ("local-seo-patan-kathmandu", "Local SEO for Patan and Kathmandu Businesses", "local seo kathmandu", "marketing"),
    ("local-seo-chitwan-terai", "Local SEO for Businesses in Chitwan and the Terai", "local seo terai", "marketing"),
    ("brand-voice-nepal", "Building a Consistent Brand Voice in Nepali Marketing", "brand voice nepal", "marketing"),
    # ---- business (10) ----
    ("pan-registration-nepal", "PAN Registration in Nepal: Step by Step", "pan registration nepal", "business"),
    ("private-limited-company-nepal", "Registering a Private Limited Company in Nepal", "company registration nepal", "business"),
    ("sole-proprietorship-nepal", "Sole Proprietorship Registration in Nepal", "sole proprietorship nepal", "business"),
    ("vat-registration-nepal", "VAT Registration for Nepali Businesses", "vat registration nepal", "business"),
    ("e-invoicing-nepal", "e-Invoicing and Digital Billing in Nepal", "e-invoicing nepal", "business"),
    ("payment-gateway-setup", "Setting Up eSewa and Khalti Payment Gateway APIs", "payment gateway setup nepal", "business"),
    ("online-store-cost-nepal", "How Much Does an Online Store Cost in Nepal?", "online store cost nepal", "business"),
    ("ecommerce-logistics-nepal", "Last-Mile Delivery and Logistics for Nepali E-commerce", "ecommerce logistics nepal", "business"),
    ("business-website-essentials", "What Every Nepali Business Website Needs", "business website nepal", "business"),
    ("professional-invoices-nepal", "Professional Invoices for Nepali Businesses", "invoice template nepal", "business"),
    # ---- career (12) ----
    ("it-colleges-nepal", "Comparing IT Engineering Colleges in Nepal", "it colleges nepal", "career"),
    ("tribhuvan-kathmandu-pokhara-university", "Tribhuvan vs Kathmandu vs Pokhara University for CS", "engineering colleges nepal", "career"),
    ("lok-sewa-computer-officer", "Lok Sewa Computer Officer: Prep and Syllabus", "lok sewa computer officer", "career"),
    ("study-in-australia-from-nepal", "Studying in Australia from Nepal: Visa and Steps", "study in australia from nepal", "career"),
    ("study-in-japan-from-nepal", "Studying in Japan from Nepal: Costs and Path", "study in japan from nepal", "career"),
    ("us-study-visa-from-nepal", "US Study Visa from Nepal: PTE/IELTS and Docs", "study in usa from nepal", "career"),
    ("study-in-europe-from-nepal", "Europe Study Options for Nepali Students", "study in europe from nepal", "career"),
    ("pte-ielts-score-guide", "PTE and IELTS Score Guidelines for Nepali Applicants", "pte ielts nepal", "career"),
    ("cs-internships-nepal", "Finding CS Internships in Nepal", "cs internships nepal", "career"),
    ("first-junior-dev-job-nepal", "Getting Your First Junior Developer Job in Nepal", "junior developer job nepal", "career"),
    ("technical-interview-prep", "Technical Interview Prep for Nepali Developers", "developer interview prep", "career"),
    ("cs-skill-roadmap", "A CS Student's Skill Roadmap for 2026", "cs skills roadmap", "career"),
    # ---- travel (12) ----
    ("annapurna-base-camp-trek", "Annapurna Base Camp: Permits, Cost and Route", "annapurna base camp trek", "travel"),
    ("everest-base-camp-trek", "Everest Base Camp Trekking: Permits and Costs", "everest base camp trek", "travel"),
    ("mardi-himal-trek", "Mardi Himal Trek: Budget and Itinerary", "mardi himal trek", "travel"),
    ("langtang-valley-trek", "Langtang Valley Trek: A Budget Guide", "langtang valley trek", "travel"),
    ("pokhara-weekend-trip", "Weekend Getaways to Pokhara on a Budget", "pokhara weekend trip", "travel"),
    ("chitwan-wildlife-tour", "Chitwan Wildlife Tour from Kathmandu", "chitwan tour", "travel"),
    ("nagarkot-weekend-trip", "Nagarkot Weekend Trip: Costs and Tips", "nagarkot trip", "travel"),
    ("upper-mustang-permit", "Upper Mustang: Permits and Costs", "upper mustang trek", "travel"),
    ("dashain-traveler-guide", "Understanding Dashain: A Traveler's Guide", "dashain festival", "travel"),
    ("tihar-deepavali-guide", "Tihar (Deepavali) in Nepal: A Visitor's Guide", "tihar festival", "travel"),
    ("chhath-puja-traditions", "Chhath Puja: Traditions and Where to See It", "chhath puja", "travel"),
    ("nepali-homestay-stays", "Staying in Nepali Homestays: What to Expect", "homestay nepal", "travel"),
    # ---- ai (12) ----
    ("ai-tools-for-digital-marketing-nepal", "AI Tools for Digital Marketing in Nepal", "ai tools for digital marketing nepal", "ai"),
    ("ai-tools-for-freelancers-nepal", "Best AI Tools for Nepali Freelancers", "ai tools for freelancers", "ai"),
    ("seo-trends-in-nepal", "SEO Trends in Nepal for 2026", "seo trends nepal", "ai"),
    ("chatgpt-for-small-business", "Using ChatGPT for Small Business in Nepal", "chatgpt for business nepal", "ai"),
    ("simple-business-automation", "Simple Automation for Nepali Businesses", "business automation nepal", "ai"),
    ("human-ai-content-workflow", "An AI Content Workflow That Still Reads Human", "ai content workflow", "ai"),
    ("ai-website-builders-nepal", "AI Website Builders for Nepali Businesses", "ai website builder nepal", "ai"),
    ("llms-for-nepali-text", "Using LLMs for Nepali and Devanagari Text", "llm nepali language", "ai"),
    ("customer-chatbots-nepal", "Customer Chatbots for Nepali Businesses", "chatbot for business nepal", "ai"),
    ("ai-content-and-seo", "How AI Content Affects SEO in Nepal", "ai seo nepal", "ai"),
    ("digital-transformation-smb", "Digital Transformation for Small Nepali Businesses", "business digital transformation nepal", "ai"),
    ("tech-trends-nepal-2026", "Tech Trends Shaping Nepal in 2026", "tech trends nepal", "ai"),
]

# 10 angle modifiers applied to every base topic (produces x10 sub-pages).
ANGLES = [
    ("", ""),
    ("for-beginners", " for Beginners"),
    ("cost-and-pricing", " Cost and Pricing"),
    ("in-kathmandu", " in Kathmandu"),
    ("step-by-step", ": Step by Step"),
    ("pros-and-cons", " Pros, Cons and Alternatives"),
    ("common-mistakes", " Common Mistakes to Avoid"),
    ("tools-and-resources", " Tools and Resources"),
    ("faq", " FAQ"),
    ("2026-guide", " 2026 Guide"),
]

# ---------------------------------------------------------------------------
# Context used to make every upgraded outline page unique and useful.
# ---------------------------------------------------------------------------
CLUSTER_CONTEXT = {
    "payments": {
        "intro": "How money moves across borders from Nepal is shaped by the National Bank of Nepal, a handful of commercial banks, and local wallets. Foreign-currency options carry real ceilings, and the single most important habit is keeping a clean, documented trail of how any foreign money reached your account.",
        "items": [
            "Confirm the current NRB foreign-currency ceiling with your bank before any large spend",
            "Document how the foreign money entered Nepal (payout, remittance or approved inflow)",
            "Match the method to the job: a card for paying, a receiving platform for collecting",
        ],
        "verify": "Foreign-currency ceilings, card terms and bank fees are set by the NRB and each bank and change; confirm the current limit and fee with your bank before you rely on a number. General information, not financial advice.",
    },
    "freelancing": {
        "intro": "Nepali freelancers earn in a foreign currency but live in a local one, so the path from a paid project to usable money has a local layer. The work is standard; the getting-paid and staying-reliable parts are where most local freelancers get stuck.",
        "items": [
            "Choose one clear offer and prove it with two real, linked examples",
            "Set up a receiving method and a Nepali bank account with a documented source",
            "Protect the schedule with a weekly hour cap and honest, stated deadlines",
        ],
        "verify": "Platform policies, payout routes and NRB rules for moving money home change; confirm the current receiving method and fee with the platform and your bank. General guidance, not financial advice.",
    },
    "web": {
        "intro": "Building for the Nepali web means a local reality: patchy connections, low-bandwidth users, local payment gateways and a small-but-loyal market. The technical choices are international, but the constraints and the costs to fix mistakes are local.",
        "items": [
            "Design for the connection your real users have, not a lab",
            "Plan ownership of the domain, hosting and code up front, not after launch",
            "Separate the one-time build cost from the ongoing maintenance and delivery costs",
        ],
        "verify": "Provider prices, hosting options and platform features change; check the current cost and ownership terms with the provider before you commit. General guidance, not a quote.",
    },
    "marketing": {
        "intro": "Digital marketing in Nepal runs on a short list of channels, and the difference between a plan and a spend is measurement. Local campaigns that track a customer, not a click, outlast every impulse that only reports impressions.",
        "items": [
            "Set a customer-level goal before choosing a channel",
            "Run a named owner and a written scope, not a rotating handoff",
            "Compare two quotes on cost per customer, not on the sticker price",
        ],
        "verify": "Platform terms, ad rules and NRB limits on foreign spend change; confirm the current cost and limits before you spend. General guidance, not a recommendation of any firm.",
    },
    "business": {
        "intro": "Setting up a real digital business in Nepal touches three layers at once: the legal (PAN, company or sole-proprietorship), the commercial (payments, delivery) and the online (the site itself). Most failures come from doing the online part before the other two are understood.",
        "items": [
            "Pick the correct legal form for your scale before you register",
            "Build the payment and delivery flow around how your customers actually buy",
            "Keep your records clean, because the tax and banking layers rely on them",
        ],
        "verify": "Registration, tax and VAT rules are set by the government and the tax authority and change; confirm the current requirement and fee with the relevant office before you act. General information, not legal or tax advice.",
    },
    "career": {
        "intro": "The Nepali career and study market is a mix of local institutions, national exams and overseas routes, each with its own rules, costs and timelines. The common thread is the documentation: a clean, verifiable paper trail decides more than the pitch.",
        "items": [
            "Match the route to the goal, not to the brochure",
            "Budget the fees and the time, and confirm both before you commit",
            "Keep every document dated and sourced, because that is what reviewers check",
        ],
        "verify": "Admission, visa and exam rules are set by the institutions and governments and change; confirm the current requirement, cost and deadline with the official source before you commit. General information, not advice.",
    },
    "travel": {
        "intro": "Getting around Nepal is inexpensive by international standards, but the permits, the season and the ground transport decide the real cost. Planning the paperwork and the transport first means the trip stays a trip, not a scramble.",
        "items": [
            "Confirm the current permits and fees for the specific route you are walking",
            "Book the ground transport and the first night before you leave",
            "Carry the documents you will be asked for at check-in, not just at the gate",
        ],
        "verify": "Permit fees, routes and season windows change; confirm the current cost and paperwork for the specific route before you book. General information, not a booking.",
    },
    "ai": {
        "intro": "AI tools in Nepal are used the way they are everywhere: to do more with less. The local twist is the language, the cost in a foreign currency and the fact that the output still has to be checked by a human who knows the market.",
        "items": [
            "Start with the one task that eats the most hours, not the flashiest tool",
            "Keep a human in the loop for anything that reaches a customer or a bank",
            "Measure the time saved against the money the tool costs, per month",
        ],
        "verify": "AI tools, their features and their cost change fast; confirm the current price and what each tool actually supports before you build a workflow on it. General guidance, not a recommendation.",
    },
}

ANGLE_CONTEXT = {
    "": {
        "intro": "This guide explains the core idea in plain language and shows the exact local steps, the documents and the numbers that matter.",
        "learn": [
            "What this means for you, and who it helps in Nepal",
            "The exact requirements, documents or setup you need",
            "The realistic process with costs in NPR",
            "The mistakes that cost the most, and how to avoid them",
            "The tools and resources that actually work locally",
        ],
    },
    "for-beginners": {
        "intro": "If you are new to this, the goal is not to master it; it is to do the first thing right and avoid the three mistakes beginners make every time.",
        "learn": [
            "The one place to start, and why it comes first",
            "What to learn before you spend money on anything",
            "The first mistake beginners make, and how to skip it",
            "A simple first project you can finish in a week",
            "What good looks like once you have finished the first one",
        ],
    },
    "cost-and-pricing": {
        "intro": "This page is about the real number, not the sticker: what you pay, what moves it up or down, and the costs that are hidden in the quote.",
        "learn": [
            "The three cost layers that make up the real total",
            "What pushes the price up, and what keeps it down",
            "The hidden costs that are not in the quote",
            "A realistic budget band for your situation",
            "How to check that a quote is fair before you sign",
        ],
    },
    "in-kathmandu": {
        "intro": "Kathmandu has the deepest market for this in the country, and that changes the options, the prices and the timeframes you can expect.",
        "learn": [
            "What is available locally, and what has to come from abroad",
            "The local timeframes, and where the delays come from",
            "How to compare a local provider with the international option",
            "What the local market charges, in a realistic band",
            "The specific Kathmandu detail that makes or breaks it",
        ],
    },
    "step-by-step": {
        "intro": "This is the exact order to do it, so you do not waste money on the step that has to come later.",
        "learn": [
            "Step one, and why it has to be first",
            "What you need before each step",
            "How long each step takes, realistically",
            "What goes wrong at each step, and the quick fix",
            "How you know the whole thing is done",
        ],
    },
    "pros-and-cons": {
        "intro": "The honest answer is a trade, not a verdict: what you gain, what you give up, and the situation where the alternative is better.",
        "learn": [
            "The real advantage, not the marketing one",
            "The real cost, including the one nobody lists",
            "The two or three alternatives, and when each wins",
            "The decision test that picks the right one for you",
            "What to do if the trade is not worth it",
        ],
    },
    "common-mistakes": {
        "intro": "This page lists the mistakes that cost Nepali users the most money, and the one-line fix for each, so you can check yourself before you commit.",
        "learn": [
            "The most expensive mistake, and why it is so common",
            "The one that is hardest to undo after it happens",
            "The one that comes from not reading the fine print",
            "The one that looks fine until the deadline",
            "How to recover if you have already made it",
        ],
    },
    "tools-and-resources": {
        "intro": "This is the shortlist of what to use, in the order to add them, so you start with the one that pays for itself.",
        "learn": [
            "The one tool that solves the main problem",
            "The free option, and where it stops being enough",
            "The paid option, and the threshold where it is worth it",
            "Where to find help locally, and where to find it abroad",
            "A simple starter stack you can use this week",
        ],
    },
    "faq": {
        "intro": "These are the questions people in Nepal actually ask about this, answered plainly, with the detail that changes the answer.",
        "learn": [
            "The most-asked question, and the detail that decides it",
            "The one that surprises most people",
            "The one that costs money to get wrong",
            "The one that has a different answer in Nepal than abroad",
            "The one you should check before you start",
        ],
    },
    "2026-guide": {
        "intro": "Rules, prices and the platforms that work change, so this page is a checklist of what to verify for 2026, not a number to memorise.",
        "learn": [
            "What has changed in the last year that most guides miss",
            "The current ceiling or limit you must confirm, and where",
            "The platforms and banks to check this year, and why",
            "The detail that will quietly change next year",
            "How to keep this page honest as the rules move",
        ],
    },
}

_ANGLE_SUGGESTED = {
    "": "What it is, who it helps, the requirements, the process with NPR costs, the mistakes to avoid, and the local tools and resources.",
    "for-beginners": "where to start, what to learn before spending, the first mistake to skip, a one-week starter project, and what good looks like.",
    "cost-and-pricing": "the three cost layers, what moves the price, the hidden costs, a realistic budget band, and how to check a quote is fair.",
    "in-kathmandu": "what is available locally versus abroad, local timeframes, how to compare a local provider, the local price band, and the local detail that decides it.",
    "step-by-step": "the exact order, what each step needs, realistic timeframes, what goes wrong at each step, and how you know it is done.",
    "pros-and-cons": "the real advantage, the real cost, the alternatives and when each wins, the decision test, and what to do if the trade is not worth it.",
    "common-mistakes": "the most expensive mistake, the hardest to undo, the fine-print one, the deadline one, and how to recover.",
    "tools-and-resources": "the one tool that solves the main problem, the free option and its limit, the paid threshold, where to find local and abroad help, and a starter stack.",
    "faq": "the most-asked question, the surprising one, the costly one, the Nepal-versus-abroad one, and the check-before-you-start one.",
    "2026-guide": "what changed in the last year, the current limit to confirm, the platforms and banks to check, the detail that will change next year, and how to keep the page honest.",
}


def priority80():
    """The 80 high-value base topics to hand-author, in cluster-priority order."""
    prio = ["payments", "freelancing", "web", "marketing", "business", "career", "ai", "travel"]
    bases = [b for b in BASE_TOPICS]
    return sorted(bases, key=lambda b: prio.index(b[3]))[:80]


def priority80_slugs():
    return [b[0] for b in priority80()]


def _money_entry(m):
    return {
        "slug": m["slug"],
        "title": "",  # filled from Markdown front matter
        "keyword": m["kw"],
        "cluster": m["cat"],
        "kind": "full",
        "full": True,
    }


def build_all():
    """Return a list of 1000 topic dicts, in stable order."""
    topics = []
    seen = set()
    for m in MONEY_POSTS:
        e = _money_entry(m)
        topics.append(e)
        seen.add(e["slug"])
    for slug, title, kw, cat in BASE_TOPICS:
        for suffix, angle in ANGLES:
            full_slug = slug if not suffix else "{}-{}".format(slug, suffix)
            # avoid duplicating an angle phrase the base title already has
            core = angle.strip().lower()
            if core and core in title.lower():
                full_title = title
            else:
                full_title = title if not angle else title + angle
            if full_slug in seen:
                continue
            seen.add(full_slug)
            topics.append(
                {
                    "slug": full_slug,
                    "title": full_title,
                    "keyword": kw,
                    "cluster": cat,
                    "kind": "outline",
                    "full": False,
                    "angle": suffix,
                }
            )
    return topics


def keywords_csv_rows():
    """1,000-row keyword map (keyword, language, script, cluster, target slug)."""
    import csv
    import io

    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["keyword", "language", "script", "cluster", "intent", "target_slug", "role", "priority", "volume_source", "volume"])
    for t in build_all():
        role = "primary" if t["full"] else "outline"
        priority = "P1" if t["full"] else "P3"
        w.writerow([
            t["keyword"] if t["full"] else "{} {}".format(t["keyword"], t["title"].split(":")[-1].strip() if t["title"] else ""),
            "English",
            "Latin",
            t["cluster"],
            "commercial" if t["full"] else "informational",
            "blog/" + t["slug"] + "/",
            role,
            priority,
            "free-sources",
            "unverified",
        ])
    return out.getvalue()
