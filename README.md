# US Trading Bot Prospects

`US_Trading_Bot_Prospects_200.xlsx` is the prospect database for the US trading-automation outreach campaign.

- **Prospects** sheet: 169 qualified prospects in the 24 campaign columns. Lead Status is `Ready` (81) or `Needs Review` (88, reason in Notes). Every row is `Not Sent` and Date Sent is blank.
- **Excluded** sheet: 31 researched records removed after quality review, with the reason for each.
- **Summary** sheet: campaign counts.

Before sending, replace the `[Your Name]` / `[Your Business]` placeholders in each email body.

## Research method and limits
Every email was seen on a public page fetched during research: GitHub organization or profile pages, repository READMEs, or PyPI and npm package metadata. No email was guessed or inferred. The research environment blocked most company websites, LinkedIn and forums. Where a fetched page showed only "United States", the city came from search-result snippets; those rows are Medium confidence and say so in Notes.

## Rebuilding
`research/leads/*.jsonl` holds the raw research records, and `research/curation.py` holds the exclusion and review decisions. To regenerate the workbook:

```
pip install openpyxl
python3 research/build.py --write 1540   # 1540 = approximate number of candidates screened
```
