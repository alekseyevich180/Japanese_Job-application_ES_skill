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

After installation, start a new Codex session and ask for tasks such as:

```text
用 japanese-es-writing 帮我把这段中文经历改成 400 字以内的日语ガクチカ。
```

```text
帮我针对索尼的软件工程岗位重写一版志望動機。
```

```text
请润色这篇日语自己PR，让它更像日本就活 ES。
```

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
