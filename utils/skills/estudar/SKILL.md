---
name: estudar
description: Turns web articles (one, a list, or a chain of articles that cite each other) into the project's own articles, adapted to the project and with facts that age (prices, token counts, limits, model names, versions) checked against official sources. Captures them with the mirrors skill, lets the user pick which cited articles to follow, verifies, plans, then writes. Use when the user asks to read, study, summarize or adapt articles, or to build knowledge-base articles from web sources.
argument-hint: "<url> [<url> ...] [seguir até N] | calibrar: <regra>"
---

# Estudar

The mirrors skill captures, you choose and write, an official source verifies.

Script: `python3 "${CLAUDE_SKILL_DIR}/../mirrors/fetch_mirrors.py"` (the mirrors skill next to this one; in the dev-sandbox repo, `utils/skills/mirrors/fetch_mirrors.py`). Without the mirrors skill, or if it says Defuddle is missing, give the user the install step from its message and stop.

## 0. Calibrate first
The calibration file is `estudar-calibracao.md` in the project's docs folder (in dev-sandbox, `docs/claude-code/estudar-calibracao.md`); if there is none, create it from the structure of dev-sandbox's at the end of the first study.
- Read it. Apply every rule in "Regras" during this study; say which ones changed what you did.
- Check the previous study's output: for the files listed in its row, find changes made after your commit by someone else (`git log -p <commit>.. -- <files>` on commits without the Claude Co-Authored-By trailer, plus `git diff`). Turn repeated differences into proposed rules and show them; add them only when the user agrees.
- `/estudar calibrar: <rule>`: add the rule to "Regras" with the date and "usuário", and stop.

## 1. Capture
- Name the group after the subject (`tokens`), not the site. Each url: `--add <group> <url> --web`.
- Chain: capture with depth 0, then show `--links <group>` (count, url, link text) and let the user pick, as they would open tabs. Only when they give a limit ("seguir até 10"), use `--depth 1 --max-pages <N>`. Never more than 20 new pages without asking.

## 2. Read and map
- Read the captured files (`mirrors/<group>/...`; front matter has title, published, modified, source).
- Search the project's docs for the subject first (index files, grep). Prefer updating an existing article to creating one; say which.
- Show a source map: one row per article with title, date, what it adds, and its claims that can age. Group articles that repeat each other.

## 3. Verify
- List each claim that can age: prices, token counts, limits, model names and versions, commands, flags, defaults.
- Check each against an official source: the project's researcher agent for that subject if there is one (in dev-sandbox, `claude-code-pesquisador`; send it the whole list in one request), else the official docs, a local mirror first.
- Mark each claim: confirmed, updated (old → new, with source), or unverified. An unverified number never goes in as fact: attribute it ("segundo <fonte>, <data>") or leave it out.

## 4. Plan, then write
- Show the plan: files to create or edit, what each section covers, sources used, and the verification table. Write only after the user approves.
- Write your own text in the project's language and doc rules, adapted to the project (its setup, its commands); drop what does not apply. Never translate or paste an article; quote briefly and attribute.
- End with the sources section the project's docs use (`## Base`, `## Fontes`...): each article's url and date, the official pages used to verify, and the date checked. Cite urls, not mirror paths, so `--stale` can find them.

## 5. Record
In the calibration file, add a row to "Estudos" (date, articles, files written, claims confirmed / updated / without official source, your commit) and update each source's row in "Fontes" (claims checked and how many were right or outdated). Add a rule only for a lesson that would have changed this study; mark it "agente" and give the evidence.

## 6. Report
What was written or changed, which claims were updated, what stays unverified, and how to recheck later: `--refresh <group>` then `--stale <group> <docs folder>`.
