# oip-notes in Quarto

Right now only part 1 lectures 3 and 4 have content.

## Instructions to build

1. Create the conda environment in `environment.yml` and activate it
2. Activate the Julia environment
3. Run `quarto render`
4. Both the HTML files and the PDF should be in `_book` directory.

## Headaches

- Currently, there is no good way to apply LaTeX definitions for HTML files, and thus we need to add
```
::: {.hidden}
$$
{{< include _macros.tex >}}
$$
:::
```
at the start of every file (taking care of the relative path if needed).
    - For TeX files, including `_macrox.tex` via `include-in-header` in `_quarto.yml` works.

- Needed to downgrade Pandoc because for PDF building `\pandocbounded` function which was added in a relatively recent version was causing problems.