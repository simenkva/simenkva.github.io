# simenkva.github.io

Source for Simen Kvaal's academic website, built with [Quarto](https://quarto.org/).

## Building the site

```sh
quarto render
```

Output is written to `docs/`, which GitHub Pages serves from (Settings → Pages → branch `main`, folder `/docs`).

## Building individual PDFs

`cv.qmd` and `publications.qmd` can also be rendered as styled PDFs (Lora/Roboto
fonts, matching the site's colors), via a Quarto ["pdf" profile](https://quarto.org/docs/projects/profiles.html)
defined in `_quarto-pdf.yml`. HTML lives in its own profile too (`_quarto-html.yml`,
active by default via `profile.default: html` in `_quarto.yml`), so the `pdf`
profile defines *only* the `pdf` format — no `--to pdf` needed, since it's the
only format available once the profile is selected:

```sh
quarto render cv.qmd --profile pdf
quarto render publications.qmd --profile pdf
```

This writes `docs/cv.pdf` / `docs/publications.pdf`.

**Two gotchas:**

- **Always render a single file, never the bare project.** Running
  `quarto render --profile pdf` with no file argument renders the *whole
  project* under that profile. Since the pdf profile's `project.render` list
  only contains `cv.qmd` and `publications.qmd`, a full-project render
  reconciles all of `docs/` against just those two outputs — deleting every
  other page, `site_libs/`, `styles.css`, images, and other static PDFs in the
  process. If that happens, restore everything with a plain `quarto render`
  (default HTML profile) and re-run the two commands above.
- **Don't drop `--profile pdf`.** `quarto render cv.qmd --to pdf` "succeeds"
  even without the profile, because Quarto/Pandoc fall back to a generic
  built-in PDF format when the active profile defines none — it silently
  produces a plain, unstyled PDF (wrong engine, no fonts/colors) instead of
  failing loudly, and overwrites the properly styled one.

## Publications list workflow

The publications page (`publications.qmd`) is generated from a BibTeX file rather
than maintained by hand.

- **Source of truth:** `kvaal_published.bib` — one `@article` entry per paper.
- **Generator:** `scripts/generate_publications.py` parses the `.bib` file and
  writes a formatted, reverse-chronological Markdown list (grouped by year, with
  the author's name bolded and DOIs linked) to `_generated/publications_list.md`.
- **Trigger:** the generator is registered as a Quarto project
  [`pre-render`](https://quarto.org/docs/projects/scripts.html) hook in
  `_quarto.yml`, so it runs automatically every time `quarto render` is invoked
  — no manual step needed.
- **Inclusion:** `publications.qmd` pulls in the generated file with
  `{{< include _generated/publications_list.md >}}`.

### Adding or editing a publication

1. Add/edit the corresponding `@article{...}` entry in `kvaal_published.bib`.
2. Run `quarto render`.
3. Commit both the `.bib` change and the resulting diff in
   `_generated/publications_list.md`.

`_generated/publications_list.md` is committed to the repo (not gitignored) even
though it's a build artifact: Quarto resolves `{{< include >}}` targets while
building its project context, *before* pre-render scripts run, so the include
target must already exist on disk for a clean checkout to render successfully.
Because generation is deterministic, the file only changes when the `.bib`
content actually changes.
