"""Remote-only image fallbacks for blog topic families.

The main blog cover manifest contains the curated Wikimedia/Openverse URLs.
These entries cover the remaining families without creating or referencing
local image derivatives.
"""

BLOG_FALLBACKS = {
    "ai-content-and-seo": {
        "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
        "alt": "Laptop displaying a digital workspace for content and SEO analysis",
    },
    "ai-tools-for-freelancers-nepal": {
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        "alt": "Close-up of electronic hardware and circuit components",
    },
    "ai-website-builders-nepal": {
        "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
        "alt": "Laptop showing a website development workspace",
    },
    "chatgpt-for-small-business": {
        "image_url": "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1200&q=80",
        "alt": "Team collaborating around a laptop in a small business workspace",
    },
    "cs-internships-nepal": {
        "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
        "alt": "Students studying together with laptops",
    },
    "cs-skill-roadmap": {
        "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80",
        "alt": "Notebook and study materials arranged for planning",
    },
    "customer-chatbots-nepal": {
        "image_url": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=80",
        "alt": "Business team collaborating around a table",
    },
    "digital-marketing-services-price-nepal": {
        "image_url": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1200&q=80",
        "alt": "Calculator and financial paperwork on a desk",
    },
    "digital-transformation-smb": {
        "image_url": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200&q=80",
        "alt": "Business team discussing a digital transformation plan",
    },
    "e-invoicing-nepal": {
        "image_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80",
        "alt": "Paperwork and calculator used for digital invoicing",
    },
    "ecommerce-logistics-nepal": {
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=80",
        "alt": "Cardboard packages prepared for ecommerce delivery",
    },
    "ecommerce-website-development-nepal": {
        "image_url": "https://images.unsplash.com/photo-1556740749-887f6717d7e4?auto=format&fit=crop&w=1200&q=80",
        "alt": "Online shopping payment on a laptop",
    },
    "first-junior-dev-job-nepal": {
        "image_url": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1200&q=80",
        "alt": "Young professionals working together in an office",
    },
    "freelance-time-management": {
        "image_url": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&w=1200&q=80",
        "alt": "Planner and clock used to manage freelance deadlines",
    },
    "freelancing-pricing": {
        "image_url": "https://images.unsplash.com/photo-1554224154-22dec7ec8818?auto=format&fit=crop&w=1200&q=80",
        "alt": "Calculator and pen beside freelance pricing paperwork",
    },
    "human-ai-content-workflow": {
        "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
        "alt": "Writing notes beside a laptop for a human-led content workflow",
    },
    "llms-for-nepali-text": {
        "image_url": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?auto=format&fit=crop&w=1200&q=80",
        "alt": "Open book and study materials for language and text work",
    },
    "nagarkot-weekend-trip": {
        "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
        "alt": "Mountain landscape viewed during a weekend trip",
    },
    "pte-ielts-score-guide": {
        "image_url": "https://images.unsplash.com/photo-1456324504439-367cee3b3c32?auto=format&fit=crop&w=1200&q=80",
        "alt": "Notebook and pen prepared for an English language exam",
    },
    "seo-trends-in-nepal": {
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
        "alt": "Analytics dashboard showing digital performance trends",
    },
    "simple-business-automation": {
        "image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=80",
        "alt": "Modern office workspace for business automation",
    },
    "tech-trends-nepal-2026": {
        "image_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=1200&q=80",
        "alt": "City lights representing emerging technology trends",
    },
    "technical-interview-prep": {
        "image_url": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80",
        "alt": "Team discussion during a technical interview preparation session",
    },
    "vat-registration-nepal": {
        "image_url": "https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=1200&q=80",
        "alt": "Tax forms and paperwork arranged on a desk",
    },
}

# Replace the few duplicated legacy manifest sources with distinct direct
# URLs so each topic family has its own image where the subject allows it.
BLOG_OVERRIDES = {
    "basic-seo-audit-nepal": {
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
        "alt": "Analytics dashboard showing search and website performance",
    },
    "how-freelancers-nepal-get-paid": {
        "image_url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=1200&q=80",
        "alt": "Money and a calculator representing freelance payments",
    },
    "esewa-vs-khalti": {
        "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1200&q=80",
        "alt": "Contactless card payment at a terminal",
    },
    "web-hosting-in-nepal": {
        "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80",
        "alt": "Server room representing website hosting infrastructure",
    },
}

# Accessible, article-specific alt text for retained legacy covers. Provider
# filenames are useful for provenance but are not meaningful to screen-reader
# users.
BLOG_ALT_OVERRIDES = {
    "accessible-website-checklist": "Refreshable braille display representing accessible digital content",
    "avoid-freelance-scams": "Padlock representing protection against freelance client scams",
    "bank-account-for-freelancers": "Nepal Bank branch in Bhaktapur",
    "basic-seo-audit-nepal": "Analytics dashboard showing search and website performance",
    "best-freelance-jobs-nepal-students": "Students studying together with laptops",
    "choosing-web-tech-stack": "Colorful source code on a computer screen",
    "client-communication-habits": "Client and designer collaborating during a project call",
    "consistent-online-income-nepal": "Home office desk for remote freelance work",
    "content-marketing-strategy": "Business professional writing marketing notes at a desk",
    "debit-vs-credit-card-nepal": "Card payment terminal",
    "digital-marketing-services-price-nepal": "Calculator and financial paperwork on a desk",
    "ecommerce-website-development-nepal": "Online shopping payment on a laptop",
    "fast-website-nepal-network": "Network cables connected to a router",
    "freelance-contracts-nepal": "Signed legal contract and pen",
    "freelance-time-management": "Planner and clock used to manage freelance deadlines",
    "freelancing-pricing": "Calculator and pen beside freelance pricing paperwork",
    "freelancing-proposals": "Hand typing on a laptop beside a notebook",
    "hire-freelance-web-developer-nepal": "Clients planning a website project together",
    "how-to-get-dollar-card-nepal": "Person using a credit card while working on a laptop",
    "how-to-start-freelancing-nepal": "Desks in an open office for starting freelance work",
    "local-seo-kathmandu-businesses": "Shops along a Kathmandu street",
    "nrb-dollar-card-rules-nepal": "Nepal Rastra Bank branch in Pokhara",
    "nrb-foreign-currency-rules": "Nepal Rastra Bank building",
    "pay-foreign-hosting-from-nepal": "Server racks in a data center for web hosting",
    "prabhu-pay-guide": "Mobile phone used for a digital payment",
    "receiving-remittance-nepal": "Cash remittance handed to a family member",
    "remote-jobs-for-nepalese": "Remote worker using a laptop",
    "sending-money-abroad-from-nepal": "Bank counter used for a remittance transfer",
    "website-security-checklist": "Unlocked laptop representing a website security risk",
    "wordpress-vs-custom": "Laptop showing source code for a web project",
}

# Article-specific corrections made after reviewing the published article text
# and the prior cover choices.  These stay remote-only: no image is copied into
# the repository.  The small number of product-specific entries use the
# product artwork itself; the rest use stable Unsplash image URLs that match
# the article's subject rather than its keyword alone.
BLOG_REPLACEMENTS = {
    "best-bank-dollar-card-nepal": {
        "image_url": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1200&q=80",
        "alt": "Bank card beside a laptop for comparing dollar-card options",
    },
    "best-digital-marketing-company-nepal": {
        "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
        "alt": "Marketing team reviewing a business strategy around a table",
    },
    "cross-border-payments-nepal": {
        "image_url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=1200&q=80",
        "alt": "Money and a calculator representing cross-border payments",
    },
    "custom-web-application-development-nepal": {
        "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
        "alt": "Developer workspace showing a custom web application in code",
    },
    "digital-marketing-agency-nepal": {
        "image_url": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80",
        "alt": "Digital marketing team collaborating on a campaign",
    },
    "digital-payment-gateways-nepal": {
        "image_url": "https://catchspaces.sfo2.digitaloceanspaces.com/nepalbuzz/2018/11/eSewa-or-Khalti.jpg",
        "alt": "eSewa and Khalti digital wallet logos for a Nepali payment gateway comparison",
    },
    "dollar-card-charges-nepal": {
        "image_url": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=80",
        "alt": "Payment card and calculator representing card fees and limits",
    },
    "earning-backlinks-nepal": {
        "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "alt": "Analytics dashboard used to evaluate search and backlink performance",
    },
    "email-marketing-nepal": {
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80",
        "alt": "Marketing planning desk with notes and a laptop",
    },
    "esewa-vs-khalti": {
        "image_url": "https://www.arjankc.com.np/blog/assets/images/posts/esewa-vs-khalti-payment-gateway-nepal.webp",
        "alt": "eSewa and Khalti mobile wallet screens shown side by side",
    },
    "freelance-income-tax-nepal": {
        "image_url": "https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=1200&q=80",
        "alt": "Tax forms, calculator and pen for freelance income tax planning",
    },
    "freelancing-portfolio": {
        "image_url": "https://images.unsplash.com/photo-1456324504439-367cee3b3c32?auto=format&fit=crop&w=1200&q=80",
        "alt": "Laptop and notebook used to build a freelance portfolio",
    },
    "high-demand-freelance-niches": {
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        "alt": "Laptop and digital workspace for focused freelance development work",
    },
    "how-freelancers-nepal-get-paid": {
        "image_url": "https://images.unsplash.com/photo-1556740749-887f6717d7e4?auto=format&fit=crop&w=1200&q=80",
        "alt": "Online payment card and laptop representing freelance payment methods",
    },
    "ime-pay-guide": {
        "image_url": "https://www.gfmd.org/sites/g/files/tmzbdl1801/files/ppd/unnamed_1.png",
        "alt": "IME Pay digital wallet logo",
    },
    "landing-pages-that-convert": {
        "image_url": "https://images.unsplash.com/photo-1558655146-9f40138edfeb?auto=format&fit=crop&w=1200&q=80",
        "alt": "Laptop displaying a web page design for a landing-page project",
    },
    "leading-remote-teams-nepal": {
        "image_url": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1200&q=80",
        "alt": "Remote team collaborating around a laptop",
    },
    "mero-share-account": {
        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
        "alt": "Stock market chart for a demat and MeroShare investing guide",
    },
    "mobile-first-low-bandwidth": {
        "image_url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=1200&q=80",
        "alt": "Smartphone displaying a mobile-first web interface",
    },
    "nepse-investing-basics": {
        "image_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1200&q=80",
        "alt": "Financial chart used to explain beginner stock investing",
    },
    "on-page-seo-nepal": {
        "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
        "alt": "Website analytics dashboard for on-page SEO work",
    },
    "paypal-alternatives-nepal": {
        "image_url": "https://images.unsplash.com/photo-1559526324-593bc073d938?auto=format&fit=crop&w=1200&q=80",
        "alt": "Online payment card and laptop representing PayPal alternatives",
    },
    "personal-income-tax-nepal": {
        "image_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80",
        "alt": "Calculator and tax paperwork for personal income tax filing",
    },
    "registering-com-np-domain": {
        "image_url": "https://images.unsplash.com/photo-1523726491678-bf852e717f6a?auto=format&fit=crop&w=1200&q=80",
        "alt": "Web development workspace for registering and managing a domain",
    },
    "selling-on-fiverr-nepal": {
        "image_url": "https://res.cloudinary.com/jerrick/image/upload/v1680153327/64251aefe2c6d0001d622a23.png",
        "alt": "Fiverr and Upwork freelance marketplace logos",
    },
    "social-media-marketing-agency-kathmandu": {
        "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=1200&q=80",
        "alt": "Smartphone showing social media apps for a Kathmandu marketing campaign",
    },
    "static-site-vs-cms": {
        "image_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1200&q=80",
        "alt": "Website design workspace for comparing a static site and CMS",
    },
    "top-freelance-platforms-nepal": {
        "image_url": "https://miro.medium.com/1%2Atelhc6vYeQKSILP1FqmXAA.jpeg",
        "alt": "Fiverr and Upwork freelance marketplace logos",
    },
    "top-specialist-platforms": {
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
        "alt": "Developers collaborating on specialist software projects",
    },
    "upwork-profile-optimization": {
        "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
        "alt": "Freelancer profile and client work discussed on a laptop",
    },
    "upwork-to-nepali-bank-account": {
        "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1200&q=80",
        "alt": "Bank card and laptop representing a freelance payout to a bank account",
    },
    "website-development-company-nepal": {
        "image_url": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200&q=80",
        "alt": "Web project team reviewing a website development plan",
    },
    "website-maintenance-nepal": {
        "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80",
        "alt": "Server racks representing ongoing website maintenance and monitoring",
    },
    "when-to-redesign-website": {
        "image_url": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1200&q=80",
        "alt": "Web designer reviewing a business website redesign",
    },
    "youtube-marketing-nepal": {
        "image_url": "https://images.unsplash.com/photo-1586899028174-e7098604235b?auto=format&fit=crop&w=1200&q=80",
        "alt": "Video creator workspace for YouTube brand marketing",
    },
}
