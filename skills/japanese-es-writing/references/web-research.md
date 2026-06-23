# Web Research

Use this reference when the user wants to fetch company pages, recruiting pages, or account-protected content for ES tailoring.

## Boundary

Only fetch content the user is allowed to access. Do not bypass CAPTCHA, paywalls, IP blocks, login protections, robots restrictions, or website terms. If the site blocks automated access, ask the user to paste the relevant text or provide an exported page.

## Helper Script

Use:

```bash
python scripts/auth_fetch.py --config config.example.json --site example --url https://example.com/page --out fetched/example
```

The script supports:

- Domain allowlist per site.
- GET requests with optional login.
- Credentials from environment variables.
- Session cookie from an environment variable.
- Optional CSRF token extraction from the login page.
- Rate limiting per request.
- HTML and extracted text output.

## OneCareer ES Research Module

Use the independent `es-research/onecareer/` module when the user wants to collect ES, interview, experience, company, career-plan, career-path, values, or 求める人物像 pages with their own account/browser access. OneCareer collection is intentionally outside this skill package.

This workflow is semi-automatic:

1. Prepare a company list, one company per line.
2. Run the browser script.
3. Log in to OneCareer in the opened browser.
4. For each company, use the browser to open the exact ES, experience, company, career, values, or recruiting page.
5. Press Enter in the terminal to save the current page as `.html`, `.txt`, and `.json`.

Example company list:

```text
Sony Group
KDDI
Hitachi Systems,https://www.onecareer.jp/companies
```

Run:

```bash
python es-research/onecareer/onecareer_browser_fetch.py --companies es-research/onecareer/onecareer_companies.example.txt --out fetched/onecareer --allow-any-domain
```

Default targets are `es,company,career,values`. To narrow collection:

```bash
python es-research/onecareer/onecareer_browser_fetch.py --companies es-research/onecareer/onecareer_companies.example.txt --out fetched/onecareer --targets es,career,values --allow-any-domain
```

Browser mechanics are isolated in `es-research/onecareer/browser_control.py`. Edit that file when changing Playwright launch behavior, profile handling, viewport size, timeout behavior, or text extraction. Keep OneCareer-specific search and saving logic in `es-research/onecareer/onecareer_browser_fetch.py`.

After collecting pages, create a writing-research digest:

```bash
python es-research/onecareer/onecareer_es_digest.py --input fetched/onecareer --out fetched/onecareer_digest.md
```

Use the digest to identify common ES prompts, selection-stage keywords, career-plan language, value/culture keywords, 求める人物像, and recurring writing patterns. Do not copy candidate ES answers into user drafts or reference files verbatim.

An agent-facing copy of the workflow is available at `.agents/onecareer-es-research.md`.

Install dependencies if needed:

```bash
python -m pip install playwright
python -m playwright install chromium
```

The script stores the browser login profile under `.browser-profiles/onecareer` by default. Do not commit that directory.

Use only content the user is allowed to access. If OneCareer blocks automation, shows CAPTCHA, or the site's terms prohibit automated collection, stop and ask the user to paste or export the relevant page text instead.

## Credential Handling

Tell the user to set environment variables locally:

Windows PowerShell:

```powershell
$env:EXAMPLE_USERNAME="your-email@example.com"
$env:EXAMPLE_PASSWORD="your-password"
```

macOS or Linux:

```bash
export EXAMPLE_USERNAME="your-email@example.com"
export EXAMPLE_PASSWORD="your-password"
```

For sites where cookie-based access is safer:

```bash
export EXAMPLE_SESSION_COOKIE="name=value; other=value"
```

Never ask the user to commit credentials into `config.json`.

## Using Results In ES

After fetching a page:

1. Read the extracted `.txt` output.
2. Identify company-specific facts: business area, role expectations, values, products, customer impact, and recruiting keywords.
3. Connect facts to the applicant's concrete experience.
4. Avoid copying website language directly into the ES.
