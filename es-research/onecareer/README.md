# OneCareer ES Research

This directory is independent from Codex skills. Use it to collect and summarize OneCareer ES, selection-experience pages, career-plan information, and company values, then use the reviewed patterns to improve the Japanese writing skill.

## Files

- `browser_control.py`: shared Playwright browser wrapper. Adjust browser profile, viewport, timeout, navigation, and text extraction here.
- `onecareer_browser_fetch.py`: OneCareer-specific company-list workflow and page saver.
- `onecareer_companies.example.txt`: company-list template.
- `onecareer_es_digest.py`: digest builder for saved OneCareer text.

## Collect Pages

Install dependencies:

```powershell
python -m pip install playwright
python -m playwright install chromium
```

Prepare a company list:

```text
Sony Group
KDDI
Hitachi Systems,https://www.onecareer.jp/companies
```

Run:

```powershell
python .\es-research\onecareer\onecareer_browser_fetch.py --companies .\es-research\onecareer\onecareer_companies.example.txt --out fetched\onecareer --allow-any-domain
```

The script opens a browser using a persistent local profile. Log in with your own OneCareer account, then review each research target:

- `es`: OneCareer ES and selection experiences
- `company`: OneCareer company overview
- `career`: career plan, career path, growth, training, or recruiting pages
- `values`: company values, mission, culture, or desired-candidate-profile pages

For each target, open the exact page you want to save, then press Enter in the terminal. Use `--allow-any-domain` when saving official company or recruiting pages outside OneCareer.

To collect only selected targets:

```powershell
python .\es-research\onecareer\onecareer_browser_fetch.py --companies .\es-research\onecareer\onecareer_companies.example.txt --out fetched\onecareer --targets es,career,values --allow-any-domain
```

## Build Digest

```powershell
python .\es-research\onecareer\onecareer_es_digest.py --input fetched\onecareer --out fetched\onecareer_digest.md
```

Use the digest to identify common ES prompts, selection-stage keywords, career-plan language, value/culture keywords, and reusable writing patterns. Do not copy candidate answers verbatim into drafts or skill references.

## Updating The Writing Skill

After reviewing `fetched\onecareer_digest.md`, update only generalizable guidance in:

- `skills/japanese-es-writing/references/es-frameworks.md`
- `skills/japanese-es-writing/references/japanese-style.md`
- `skills/japanese-es-writing/references/company-tailoring.md`

For 志望動機 and キャリアプラン, especially extract:

- business or role keywords the applicant can connect to their experience
- career path and training language
- values, culture, and 求める人物像
- differences between generic industry motivation and company-specific motivation

Keep raw collected pages under `fetched/`, which is ignored by Git.
