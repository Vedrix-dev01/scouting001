# Research brief: German real estate prospects (Real Estate Social Media Automation)

Sender: Victor Nweze, Real Estate Automation Specialist. Service: turns property data (new listings, price changes,
sold/rented, open houses, videos) into ready-to-review social posts, captions, hashtags and schedules for Instagram,
Facebook, LinkedIn — via n8n/Make/Zapier/API workflows. Positioned as automation/technology, NOT a social media manager.

## Network reality (important)
- WebFetch/curl CANNOT open German websites, Instagram, Facebook, LinkedIn, Google (all blocked). Don't retry them.
- WebSearch WORKS. Its answer text quotes content from the indexed pages (Impressum, Kontakt, listing pages, social
  profiles). You verify ONLY via WebSearch results. Use German queries, e.g.
  "Immobilienmakler Regensburg Impressum E-Mail", "<Firma> Impressum", "<Firma> Instagram", "<Firma> Facebook",
  "<Firma> Immobilien Angebote", "site:<domain> Impressum", "site:instagram.com <Firma>".
- Be economical: each query should confirm several things; roughly 4-6 searches per accepted prospect, max ~180 searches.

## Acceptance rules (strict)
- A real estate business in Germany (Makler, Immobilienbüro, Hausverwaltung, Bauträger, Projektentwickler, luxury,
  Gewerbe, Ferienimmobilien, investment). NOT portals, associations, blogs, news, schools, pure mortgage brokers, private sellers,
  and NOT big franchise HQs (Engel & Völkers HQ, Von Poll HQ, Remax DE HQ) — a local independently-run franchise office with
  its own public email is OK.
- Email: must be quoted in a search result that clearly comes from the company's OWN Impressum/Kontakt/website page
  (the result URL is on the company domain), and the email domain should match the company website domain (or be a
  plainly business address shown there, e.g. firm@t-online.de shown in their Impressum). NEVER guess, infer, or build an
  email. If the search answer only paraphrases without the exact address, don't accept. Watch for obfuscation
  like "info(at)firma.de" -> write normal form. Only professional/business addresses.
- Record city and Bundesland (State).
- Social/listing evidence: record a URL for Instagram/Facebook/LinkedIn/YouTube ONLY if a search result shows that
  profile URL belonging to the company (matching name/city). Otherwise leave empty. Record listing evidence only as
  shown in results (e.g. "Website 'Angebote' page lists 14 Objekte per search snippet"). Don't invent counts; if no count
  is visible, describe what was seen ("website has Kaufen/Mieten listing pages with current Objekte").
- If a named person (Inhaber/Geschäftsführer) appears in the Impressum snippet, you may use their name and a
  "Guten Tag Herr/Frau <Nachname>," greeting; else "Guten Tag," or "Sehr geehrtes Team von <Firma>,".
  first_name = that person's first name if known, else "".
- No duplicates: before each add, check ALL files in de/leads/*.jsonl for same company, domain or email.
- Use your own helper script file (unique name) to append; never edit others' files.

## Output: JSONL, one object per line, appended as you go, fields (strings):
prospect_name (person if named, else company), company, first_name, email, state (Bundesland), city,
business_type (e.g. Immobilienmakler / Hausverwaltung / Bauträger / Projektentwickler / Luxusimmobilienmakler),
property_focus (e.g. Wohnimmobilien Kauf & Miete; Neubauprojekte; Gewerbe; Ferienimmobilien),
listings_evidence, website, instagram, facebook, linkedin, youtube (URLs or ""),
multiple_listings ("Yes"/"No"/"Unknown"),
buying_intent (High / Medium / Low per rules below),
personalization_detail (verified fact), personalization_reason, personalized_opening (German, formal Sie),
subject_line (German, specific, short, no spam), email_body (German, see below),
source_url (the company page URL from the search result showing the email), evidence (what was found, where, which
queries confirmed it), evidence_type (Website / Instagram / Facebook / LinkedIn / Google Business / Property Portal /
Company Profile / Other Public Source — primary one; add "(via search index)"),
research_confidence (High only when email + city + listings + at least one social profile all appear in results
consistently; otherwise Medium; Low = avoid), notes (include "Language: German" and anything to check).

Buying intent: High = several signals (many listings, active Instagram/Facebook, multiple offices/agents, new developments,
frequent property posts). Medium = relevant, fewer signals. Low = relevant but little marketing evidence (avoid).

## Email (German, formal, 80-130 words), structure:
Greeting; one specific verified observation; the manual-work problem (neue Objekte, Preisänderungen, verkauft/vermietet
für Instagram/Facebook/LinkedIn aufbereiten); brief automation explanation (aus vorhandenen Objektdaten automatisch
Entwürfe für Beiträge, Captions, Hashtags, Planung — z. B. per n8n/Make/Schnittstelle zum Maklersystem); one concrete
example tailored to them; soft CTA question; closing:
"Mit freundlichen Grüßen\nVictor Nweze\nReal Estate Automation Specialist"
Use \n for line breaks. Vary wording per prospect — no two emails alike. No promises of sales/leads/results, no urgency,
no hype ("revolutionär", "garantiert", "mehr Umsatz", "Leads garantiert"). Natural German, not translated-sounding.
Subject examples to vary from: "Social Media für Ihre Objekte in <Stadt>", "Neue Objekte von <Firma> automatisch als Beitrag" — make each unique.

Finish with a short summary: accepted count, rejected count + main reasons, output path. Don't paste records.
