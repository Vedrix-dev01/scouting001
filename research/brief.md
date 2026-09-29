# Research brief (shared by all research agents)

You are researching US-based prospects for a service that builds custom trading bots and trading automation
(MT4/MT5 Expert Advisors, NinjaTrader/TradeStation strategies, TradingView/Pine Script automation & webhooks,
crypto exchange API bots for Binance.US/Coinbase/Kraken/Bybit etc., copy-trading software, signal auto-execution,
custom algorithmic systems). Use WebSearch for discovery and WebFetch to VERIFY on the underlying page.

## Acceptance rules (strict)
- Must be in the United States (state + city verifiable from the site, contact page, LinkedIn, business address, etc.).
- Must have a MEANINGFUL connection to trading technology / automation (builds or sells indicators, strategies, EAs,
  bots, algo systems, trading software, signal services, trading education that covers systematic/automated trading,
  a systematic CTA/quant firm, a trading platform/tool startup, or a public request for a trading bot developer).
  Plain retail traders, market-news people, generic finance influencers => REJECT.
- Must have a COMPLETE email address that is PUBLICLY DISPLAYED on a page you actually fetched (contact page,
  footer, about page, LinkedIn/GitHub public profile, forum post, public business listing). Generic business inboxes
  (info@, support@, contact@, sales@) are acceptable if displayed by the business. NEVER guess, infer a pattern,
  or construct an email. If WebFetch of the page does not show the email text, do not accept it (you may try a
  second page like /contact, /about, /privacy, /terms where emails often appear). Emails obfuscated as
  "name [at] domain [dot] com" count as displayed — write the normal form.
- Source URL must be a URL you actually fetched in this session and that supports the evidence.
- No duplicates within your own list (same person, company, domain, or email).
- Do NOT include personal/private info (no home addresses, no phone numbers needed).

## Output
Append ONE JSON object per line (JSONL) to the output file given in your task, using Bash
(e.g. python3 - <<'PY' ... json.dumps ... PY, appending with open(path,'a')). Write records as you go
(every few records), so nothing is lost. Fields (all strings):

{
 "prospect_name": "person's full name if a named individual is identifiable, else the company name",
 "company": "company/brand name (or 'Independent' for an individual with no company)",
 "first_name": "person's first name if known; else empty string",
 "email": "exact publicly displayed email",
 "state": "US state full name", "city": "city",
 "trading_niche": "e.g. Futures algo strategies / Forex EAs / Crypto trading bots / TradingView indicators / Systematic CTA / Trading education / Signal service / Copy trading / Trading software",
 "trading_platform": "e.g. NinjaTrader 8; MT4/MT5; TradingView; TradeStation; Binance/Coinbase API; Interactive Brokers API; Python; multiple",
 "trading_product": "their specific product/project/program name",
 "buying_intent": "High / Medium  (High only if they publicly request a developer/bot/EA/automation, or are actively building a product that needs automation dev; Medium for businesses already doing/selling automation or trading software)",
 "personalization_detail": "one specific verifiable fact from the source, 1-2 sentences",
 "personalization_reason": "why that fact makes them relevant to trading automation dev help; never claim they definitely need it unless they said so",
 "personalized_opening": "1-2 natural sentences that open the email with the specific reason for contacting them (see style rules)",
 "subject_line": "unique, short (3-8 words), specific to them, no hype",
 "email_body": "full email: 'Hi <First Name or team name>,' + observation + relevance + brief relevant service + simple question CTA + 'Best regards,\\n[Your Name]\\n[Your Business]'. 90-150 words. Use \\n for newlines.",
 "source_url": "URL you fetched that shows the email and/or evidence",
 "evidence": "who they are; what they do; trading connection; automation relevance; exactly where the email was found (URL/page)",
 "evidence_type": "Official Website / LinkedIn / Public Business Profile / Trading Website / Developer Profile / Public Forum / Public Social Profile / Search Result Verified / Other",
 "research_confidence": "High / Medium / Low",
 "notes": "anything reviewers should know (e.g. generic inbox, location from LinkedIn only)"
}

## Style rules for opening / subject / body
- Do NOT open with: "I hope you're doing well", "I came across your profile", "I noticed you are a trader",
  "Hope you're having a great day". Start with the specific thing about them. Vary sentence structure per prospect.
- Banned words/phrases anywhere: tailored solutions, seamless, cutting edge/cutting-edge, revolutionize, unlock,
  transform your workflow, leverage, game changing/game-changing, synergy, URGENT, ACT NOW, guaranteed, profits
  promises, get rich, free money, investment opportunity, returns.
- Never promise profits/returns or give financial advice. Only mention services relevant to them (e.g. don't pitch MT5
  to a NinjaTrader vendor unless relevant). Keep it plain, human, professional. Each email must differ.
- If using a generic inbox with no named person, greet "Hi <Company> team," and set first_name to "".

## Confidence
High = identity, US location, email, trading activity all verified on fetched pages. Medium = relevant but
something (e.g. city) less certain. Low = avoid; only include if flagged in notes.

Work efficiently: many searches, quick fetches of contact pages. Keep going until you reach your target count
or have genuinely exhausted your segment (then broaden within your segment: other states, cities, platforms).
At the end, reply with a short summary: number accepted, number rejected (roughly, with main reasons),
and the output file path. Do not paste all records in your reply.

## ROUND 2 ADDENDUM (read carefully)
- Network reality: ONLY github.com, gist.github.com, raw.githubusercontent.com, pypi.org and registry.npmjs.org can be fetched.
  Every other site is blocked (don't waste calls retrying blocked domains). WebSearch works for discovery and for
  location snippets.
- Emails must appear on a page you fetched from those hosts (GitHub org profile "Email" field, a profile README,
  a repo README/CONTACT/package.json/setup.py/pyproject, PyPI author field, npm maintainer field).
- Location: prefer city+state shown on a fetched GitHub page. If the fetched page only says "United States", you may take
  city+state from WebSearch result snippets (Crunchbase, business listings, press) — then set research_confidence
  "Medium" and say "city from search results" in notes. Never use people-search/home-address sites.
- Prefer company/business-domain emails. Personal Gmail etc. only when the prospect clearly publishes it as their
  professional contact for a real trading project; say so in notes.
- Reject: students/class projects, job-seekers' portfolios, abandoned (>3 yrs) hobby repos, non-US, giant firms.
- Do NOT add anyone listed in research/existing.txt
  (check emails AND company names), and check the other round-2 files leads/r2_*.jsonl before each add.
- Use YOUR OWN helper script with a unique filename (e.g. scratchpad/<yourfile>_add.py). Never edit shared scripts
  or other agents' files.
