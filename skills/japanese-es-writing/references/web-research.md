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
