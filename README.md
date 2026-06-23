# Job Application Writing Codex Skills

This project packages Codex skills for Japanese and English job-application writing.

Included skills:

- `japanese-es-writing`: Japanese Entry Sheet writing for Japanese companies and foreign/global companies in Japan.
- `nature-polishing`: English polishing, restructuring, and Chinese-to-English rewriting support.
- `nature-writing`: English structure drafting from claims, notes, and rough source material.

The main ES skill is designed for Chinese-speaking applicants who need help with:

- 志望動機
- 自己PR
- ガクチカ / 学生時代に力を入れたこと
- 研究概要
- 面接想定問答
- Chinese notes to natural Japanese ES prose
- Company-specific rewriting for Japanese companies and foreign companies
- English application writing and polishing for foreign companies
- Word-count reduction and polishing
- User-authorized web page fetching for company research

## Install

Windows PowerShell:

```powershell
.\install.ps1
```

macOS or Linux:

```bash
bash install.sh
```

Manual install:

Copy the needed directories under `skills/` into your Codex skills directory:

```text
~/.codex/skills/japanese-es-writing
~/.codex/skills/nature-polishing
~/.codex/skills/nature-writing
```

If `CODEX_HOME` is set, copy it into:

```text
$CODEX_HOME/skills/<skill-name>
```

## Use

After installation, start a new Codex session. You can either name a skill explicitly or describe the task naturally. Naming the skill is useful when you want precise routing.

## Which Skill To Use

| Task | Use this skill | Typical request |
|---|---|---|
| Japanese ES for Japanese companies | `japanese-es-writing` | `用 japanese-es-writing 帮我写三菱商事的志望動機，400字以内。` |
| Japanese ES for foreign/global companies in Japan | `japanese-es-writing` | `用 japanese-es-writing 帮我针对 Google Japan 的 software engineer 岗位改一版日语自己PR。` |
| Chinese notes to natural Japanese ES | `japanese-es-writing` | `把这段中文经历改成日语ガクチカ，300字以内，语气适合日本就活。` |
| English application draft from notes | `nature-writing` | `用 nature-writing 根据这些中文要点写一版英文 cover letter。` |
| English ES / motivation statement structure | `nature-writing` | `用 nature-writing 帮我组织外企申请的英文 Why this company answer，200 words。` |
| Polish existing English application text | `nature-polishing` | `用 nature-polishing 润色这段英文 personal statement，让它更自然、更职业。` |
| Chinese draft to polished English | `nature-polishing` | `把这段中文申请理由改成英文，不要直译，适合外企申请。` |

## Recommended Workflows

### Japanese ES

1. Use `japanese-es-writing` for the draft.
2. Provide company name, role, word or character limit, your experience, and the strength you want to show.
3. Ask for a stricter version if the first draft is too generic or too long.

Example:

```text
用 japanese-es-writing 帮我把这段中文经历改成 400 字以内的日语ガクチカ。
```

### English Application Writing

Use `nature-writing` when you only have notes or Chinese material and need a new English answer.

```text
用 nature-writing 根据下面的中文经历写一版 250 words 的英文 motivation statement，目标是外企材料研发岗位。
```

Use `nature-polishing` when you already have an English draft and need revision.

```text
用 nature-polishing 润色下面这段英文 cover letter，保持真实经历，不要夸大。
```

### Japanese And English Versions

When you need both languages, draft the content logic once, then adapt by language:

1. Use `japanese-es-writing` for the Japanese ES version.
2. Use `nature-writing` to build the English version from the same facts.
3. Use `nature-polishing` for final English tone and concision.

Example:

```text
先用 japanese-es-writing 帮我写日语自己PR，再用 nature-writing 基于同一经历写英文版，最后用 nature-polishing 压到 180 words。
```

## Information To Provide

For better results, include:

- Target company and role
- Language: Japanese or English
- Output type: 志望動機, 自己PR, ガクチカ, cover letter, motivation statement, personal statement, career goals
- Word or character limit
- Your real experience, actions, result, and reflection
- What strength you want to emphasize
- Company research notes or job description, if available

## Project Structure

```text
skills/
  japanese-es-writing/
    SKILL.md
    agents/openai.yaml
    scripts/
    references/
  nature-polishing/
    SKILL.md
    references/
  nature-writing/
    SKILL.md
    agents/
    references/
```

## Optional Web Fetching

The skill includes `skills/japanese-es-writing/scripts/auth_fetch.py` for fetching pages that the user is authorized to access. Users must configure their own account credentials through environment variables.

For OneCareer, use the browser-based helper instead of API calls:

```powershell
python .\skills\japanese-es-writing\scripts\onecareer_browser_fetch.py --companies .\skills\japanese-es-writing\scripts\onecareer_companies.example.txt --out fetched\onecareer
```

The helper opens a browser, lets you log in with your own OneCareer account, then iterates through a company list. For each company, open the exact OneCareer company, ES, or experience page in the browser and press Enter in the terminal to save the page text.

Browser control is separated into:

```text
skills/japanese-es-writing/scripts/browser_control.py
```

Adjust Playwright launch settings, profile handling, viewport, timeouts, and page text extraction there. Keep OneCareer-specific company-list and saving logic in:

```text
skills/japanese-es-writing/scripts/onecareer_browser_fetch.py
```

After saving pages, create a digest for improving the Japanese ES writing references:

```powershell
python .\skills\japanese-es-writing\scripts\onecareer_es_digest.py --input fetched\onecareer --out fetched\onecareer_digest.md
```

Use the digest to learn common ES prompts and writing patterns. Do not copy OneCareer candidate answers verbatim into drafts or skill references.

Install Playwright first if needed:

```powershell
python -m pip install playwright
python -m playwright install chromium
```

Company list format:

```text
Sony Group
KDDI
Hitachi Systems,https://www.onecareer.jp/companies
```

Copy and edit the example config:

```text
skills/japanese-es-writing/scripts/config.example.json
```

Credentials must be set locally, not committed to GitHub.

Windows PowerShell:

```powershell
$env:EXAMPLE_USERNAME="your-email@example.com"
$env:EXAMPLE_PASSWORD="your-password"
$env:EXAMPLE_SESSION_COOKIE="name=value"
```

macOS or Linux:

```bash
export EXAMPLE_USERNAME="your-email@example.com"
export EXAMPLE_PASSWORD="your-password"
export EXAMPLE_SESSION_COOKIE="name=value"
```

Run:

```bash
python skills/japanese-es-writing/scripts/auth_fetch.py --config skills/japanese-es-writing/scripts/config.example.json --site example --url https://example.com/page --out fetched/example
```

Use this only for pages the user is allowed to access. The script does not bypass CAPTCHA, paywalls, access controls, or rate limits.
