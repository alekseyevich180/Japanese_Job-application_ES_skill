# OneCareer ES Research Agent Copy

Purpose: collect OneCareer ES, selection-experience pages, career-plan information, and company values independently from the `skills/` package, then convert reviewed patterns into improvements for the Japanese ES writing skill.

Use these project paths:

- Browser wrapper: `es-research/onecareer/browser_control.py`
- OneCareer collector: `es-research/onecareer/onecareer_browser_fetch.py`
- Company-list template: `es-research/onecareer/onecareer_companies.example.txt`
- Digest builder: `es-research/onecareer/onecareer_es_digest.py`
- Writing references to update after review: `skills/japanese-es-writing/references/`

Default collection command:

```powershell
python .\es-research\onecareer\onecareer_browser_fetch.py --companies .\es-research\onecareer\onecareer_companies.example.txt --out fetched\onecareer --allow-any-domain
```

Default digest command:

```powershell
python .\es-research\onecareer\onecareer_es_digest.py --input fetched\onecareer --out fetched\onecareer_digest.md
```

Rules:

- Use only pages the user can access with their own account.
- Do not bypass CAPTCHA, paywalls, access controls, rate limits, or website restrictions.
- Keep login profiles in `.browser-profiles/` and raw pages in `fetched/`.
- Do not copy candidate ES answers verbatim into user drafts or skill references.
- Convert collected material into abstract patterns: common prompts, evaluation points, structure, tone, phrasing cautions, career-plan language, company values, culture, and 求める人物像.
- For 志望動機 and キャリアプラン, connect values and career-plan material to concrete applicant experience rather than quoting company pages.
