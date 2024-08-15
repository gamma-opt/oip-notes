# oip-notes in Quarto

## Instructions to build

May need to install `librsvg` for PDF builds, or figure out a way for SVG images to fallback to PNG or something.

1. Create the conda environment in `environment.yml` and activate it
2. Activate the Julia environment
3. Run `quarto render`
4. Both the HTML files and the PDF should be in `_book` directory.

## Slides

Having one source file for both slides and regular website/pdf seems infeasible due to differing content/structure.

As an example, I've added one quickly-converted-from-website presentation to `slides/part1/lecture03.qmd`.

As far as I can tell, there is no way of having the presentations be built with `quarto render` without having them being displayed on the website.
But they are individual files anyway, so one can do `quarto render slides/**/*.qmd`.

## Headaches

- Currently, there is no good way to apply LaTeX definitions for HTML files, and thus we need to add
```
{{< include _macros.tex >}}
```
at the start of every file (taking care of the relative path if needed).
    - For TeX files, including `_macrox.tex` via `include-in-header` in `_quarto.yml` works.

- Needed to downgrade Pandoc because for PDF building `\pandocbounded` function which was added in a relatively recent version was causing problems.

- Use this for algorithms? https://github.com/leovan/quarto-pseudocode