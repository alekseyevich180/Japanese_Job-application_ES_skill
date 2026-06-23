---
name: japanese-es-writing
description: Draft, revise, translate, and polish Japanese job-hunting Entry Sheets for Chinese-speaking applicants applying to Japanese companies or foreign/global companies in Japan. Use when the user asks for Japanese ES support, including 志望動機, 自己PR, ガクチカ, 学生時代に力を入れたこと, 研究概要, キャリアプラン, 長所短所, 面接想定問答, word-count reduction or expansion, Japanese naturalness checks, company-specific tailoring, foreign-company/global-company fit, or converting Chinese experience notes into Japanese application prose.
---

# Japanese ES Writing

## Core Workflow

First identify the target output:

- New draft from raw notes
- Revision of an existing Japanese ES
- Chinese-to-Japanese conversion
- Company-specific tailoring for Japanese companies or foreign/global companies in Japan
- Shortening, expanding, or tone adjustment
- Interview follow-up preparation

Ask only for missing information that materially affects the answer: target company, role, word or character limit, school/major, concrete experience, result, and applicant's intended strength. If enough information exists, proceed and state assumptions briefly.

## Drafting Rules

Use Japanese ES conventions:

- Prefer concrete actions, motivations, constraints, and outcomes over broad claims.
- Keep the applicant modest but not passive.
- Show company fit through business, role, values, technology, products, or customer impact rather than flattery.
- Avoid machine-translation phrasing, inflated adjectives, and unverifiable claims.
- Preserve the user's true experience. Do not invent awards, numbers, internships, leadership roles, or company research.
- When content is weak, say what evidence is missing and offer fill-in prompts.

Default to Japanese output unless the user asks for Chinese explanation. For Chinese-speaking users, include concise Chinese notes when useful: why the structure works, what changed, and what information would improve the answer.

## Reference Selection

Load only the reference needed for the task:

- Read `references/es-frameworks.md` for 志望動機, 自己PR, ガクチカ, 研究概要, and interview-answer structures.
- Read `references/japanese-style.md` for natural Japanese, ES tone, forbidden expressions, and revision checks.
- Read `references/company-tailoring.md` when tailoring to a specific company, industry, or job type.
- Read `references/output-patterns.md` when choosing response format, comparison tables, or multi-version output.
- Read `references/web-research.md` when the user wants to fetch company pages, recruiting pages, career-plan or values pages, or use OneCareer ES research collected outside the skill.

## Web Research Helper

Use `scripts/auth_fetch.py` only when the user asks to fetch web pages and provides, or agrees to configure, credentials for accounts they are authorized to use.

Use the independent `es-research/onecareer/` module when the user asks to collect OneCareer ES pages, company pages, career-plan pages, values, or 求める人物像 using their own account and browser login state. Ask for, or create, a company list file before running it.

Use `es-research/onecareer/onecareer_es_digest.py` after OneCareer pages have been saved and the goal is to improve ES writing references from collected examples. Treat the digest as pattern research only; do not copy candidate ES answers verbatim.

Before using the helper:

- Confirm the target website and page are allowed by the user's account and the website terms.
- Do not bypass CAPTCHA, paywalls, access controls, rate limits, or technical blocks.
- Prefer public company and recruiting pages when possible.
- Store credentials in environment variables, not in prompts, source files, or committed config.
- Store browser profiles locally and do not commit `.browser-profiles/`.
- Use the downloaded text only as context for ES tailoring; cite uncertainty if the page may be outdated or incomplete.

## Quality Checks

Before finalizing:

- Check the answer fits the requested limit. If exact Japanese character count is important, mention that the count is approximate unless counted with a tool.
- Confirm the main claim appears in the first sentence or first two sentences.
- Confirm each paragraph has a function: claim, evidence, company fit, future contribution.
- Remove generic statements that could apply to any company.
- Replace direct Chinese logic order with Japanese ES-friendly flow where needed.

## Output Defaults

For a draft or revision, provide:

1. 完成稿
2. 改善ポイント
3. さらに強くするために必要な情報

For a rewrite, preserve meaning and provide a stricter version if the original is too casual, too long, or too generic.
