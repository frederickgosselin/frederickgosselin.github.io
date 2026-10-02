# Website project: fgosselin.com (Astro, bilingual EN/FR)

Static Astro site in `site/`, migrated from WordPress (fgosselin.meca.polymtl.ca).

## Hosting and deployment (live since 2026/10/02)

- Public address: https://www.fgosselin.com (bare `fgosselin.com` redirects to `www`). Fallback: https://frederickgosselin.github.io/
- Repository: https://github.com/frederickgosselin/frederickgosselin.github.io (public, branch `main`, git root = this folder).
- Deploy = `git push` to `main`. The workflow `.github/workflows/deploy.yml` builds `site/` and publishes it
  (GitHub Pages source must stay "GitHub Actions"). Takes about one minute. Never push without the user's go-ahead.
- Domain registered at GoDaddy; DNS: four GitHub `A` records on `@`, `CNAME www` -> `frederickgosselin.github.io`,
  and a GitHub domain-verification TXT. The old GoDaddy mail records (MX, mail CNAMEs) are unused and were left in place.
  Do not change DNS without asking.
- The user's machine on the Polytechnique VPN resolves the old records for a while after DNS changes; test with
  `curl --resolve` or a public resolver (8.8.8.8) before concluding that the site is down.
- `gh` is installed at `C:\Program Files\GitHub CLI\gh.exe` (not on this shell's PATH); it is logged out by default.
Brand: Polytechnique Montreal palette and logos (see `site/src/styles/global.css`, `logos/`).

## Publications: keep the master list and both language pages in sync (MANDATORY)

Whenever the website is updated (any change to a publication, a new paper, a corrected link, a new preprint
or repository), the English AND French publication pages must be cross-checked against `publications.md`
(`C:\Users\frede\.claude\publications.md`) so that every paper is present and up to date.

- Pages: `site/src/content/pages/en/publications.md` and `site/src/content/pages/fr/publications.md`.
- The pages are hand-curated on purpose (they also list preprints, GitHub repositories and links to the
  publisher's hosted paper). Do NOT replace them with a BibTeX-generated list.
- Edit both languages in the same change. The two lists must contain the same entries in the same order.
- Run `python site/scripts/check-publications.py` after every publication edit and before every commit/deploy.
  It must report: nothing in `publications.md` missing from a page, nothing on a page missing from
  `publications.md`, and EN and FR identical. The "authors" section is a heuristic (it only reads
  "Surname, I." names), so review it by eye rather than treating it as pass/fail.
- If `publications.md` is the one that is out of date (a paper on the site that is not in the master file),
  say so and update it, so that the two never drift.
- Translation rule for the French page: translate ONLY the section headings, "My PhD thesis (in french)" and
  "PhD and MSc theses of students I supervised/co-supervised over the years:". Never translate article titles,
  journal names or author lists.

## Bilingual content

- Every page and every news post exists in `en` and `fr`. A news post links its translation through the
  `translation:` front-matter field; pages are paired in `site/src/i18n.ts` (`PAGES`).
- Front page = landing page with the latest news (the bio lives on the About page, not on the home page).

## Safety / git

- Never commit `backup/`, the Duplicator `*.zip` archive, `migration/`, or any `wp-config.php`: they contain the
  database dump and site internals. Keep them in `.gitignore`.
- Do not publish, push or change DNS without asking first.

## Style

- No em-dashes in site prose. Dates `YYYY/MM/DD` in notes; SI units; period as decimal separator.
- Files may be UTF-8 or cp1252 when they come from WordPress exports; the site sources are UTF-8.

## Useful commands (run in `site/`)

- `npm run dev` : local preview (also available as the `astro-dev` entry in `.claude/launch.json`)
- `npm run build` : production build into `site/dist`
- `python scripts/check-publications.py` : publication cross-check described above
