# Research brief: Invoice AI automation prospects (OpenClaw agents)

Sender: Oseni Ibrahim, AI Automation Specialist. Offer: OpenClaw-based AI agent development for invoice management,
reporting, finance operations, billing workflows and business automation (invoice intake/extraction, status tracking,
overdue follow-ups, payment reminders, AR reporting, reconciliation, CRM/ERP/accounting sync, finance alerts,
management summaries, invoice search assistant).

## Network reality (critical)
- Company websites, LinkedIn, Google are BLOCKED. Don't retry them.
- Reachable: github.com pages via WebFetch (org/profile/repo pages; github.com/topics 404s), raw.githubusercontent.com
  and registry.npmjs.org and pypi.org via curl in Bash (e.g. curl -s https://registry.npmjs.org/<pkg>,
  curl -s https://pypi.org/pypi/<pkg>/json).
- WebSearch is SHARED and SCARCE (≈200 for the whole session across 8 agents). Obey YOUR search budget in the task.
  Every search should confirm several facts at once.
- Do NOT use GitHub MCP tools (mcp__github__*) — out of scope for this session.

## Acceptance rules
- Real company with a real business (not a hobby package, not an individual freelancer, not a student).
- Relevant: invoicing / billing / accounting / AR / AP / e-invoicing / payments / ERP / finance admin is core to what they do.
- Country: US, UK, DE, NL, FR, CA, AU, CH, AT, BE, IE, SE, DK, NO, FI or other European country. Verify country (and
  city where possible) from a fetched GitHub org page, package metadata/README, or a search snippet. ccTLD alone is NOT
  enough; ccTLD + GitHub org location or README/company imprint text = OK.
- Email: only a professional email PUBLICLY shown: GitHub org "Email" field, README/CONTACT/SECURITY file, npm
  maintainer/publisher or package.json author field, PyPI author_email, or a search snippet quoting the company's own
  page. Must be on the company's domain. Never guess/construct. If the company is clearly relevant and verified but no
  email is found: keep it with email "" (it will be marked "No verified email").
- Person: only name a person if a fetched page/metadata ties them to the company (e.g. npm maintainer name + company
  domain email, GitHub org README naming founder). Job title only if stated; else "".
  Otherwise prospect_name = company name, first_name = "".
- Avoid giant enterprises (SAP, Oracle, Intuit, Stripe HQ, Microsoft) — fine to include mid-size vendors.
- No duplicates: before each add, check ALL files in inv/leads/*.jsonl (company name, website domain, email domain).
- Use your own helper script with a unique filename; never edit others' files.

## Output: JSONL one object per line in your output file, appended as you go. Fields (strings):
prospect_name, company, first_name, job_title, email, country, state (state/region or ""), city,
company_type (one of: Invoicing software / Accounting software / Accounts receivable software / E-invoicing /
Billing & subscription management / Accounting & bookkeeping firm / ERP implementation & consulting / Payment & fintech /
Business management software / Financial administration services),
industry, invoice_product (their invoice/billing/finance product or service), accounting_platform (integrations named,
e.g. Xero, QuickBooks, DATEV, Exact — only if seen), erp (only if seen), payment_platform (only if seen),
company_size (only if seen, else ""), website, linkedin (only if seen, else ""),
buying_intent (High/Medium/Low per evidence: High = active automation product, many integrations, complex B2B
workflows, hiring; Medium = relevant product, less evidence; Low = weak) — do NOT mark everything High,
automation_opportunity ("Potential opportunity: automate ..." specific to them),
personalization_detail (verified fact), personalization_reason, personalized_opening (English, 1-2 sentences),
subject_line (specific, unique), email_body, source_url (page that shows the evidence/email),
evidence (what was found where), evidence_type (Website / Product page / Documentation / Company page / Developer
registry (npm/PyPI) / GitHub organization page / Search result / Press release / Job posting),
research_confidence (High = company, website, email, personalization all verified; Medium = company+website verified,
contact limited; Low = limited), notes.

## Email (English, 70-120 words)
"Hi <First Name>," only if first_name is a verified name, else "Hello," or "Hello <Company> team,".
Specific observation -> connect their product/workflow to an automation opportunity -> "I build OpenClaw-based AI agents
that ..." (only relevant workflows) -> one simple question -> sign-off exactly:
"Best,\nOseni Ibrahim\nAI Automation Specialist". Use \n for line breaks. No placeholders. Don't claim they lack
automation. Banned words: seamless, tailored, stunning, revolutionize, game changer, cutting edge, unlock, supercharge,
transform your business, leverage. Each email and subject different.

Finish with a short summary: accepted (with/without email), rejected + main reasons, searches used, output path.
