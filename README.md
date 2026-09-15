# simenkva.github.io

Source for Simen Kvaal's academic website, built with [Quarto](https://quarto.org/).

## Building the site

```sh
quarto render
```

Output is written to `docs/`, which GitHub Pages serves from (Settings → Pages → branch `main`, folder `/docs`).

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
