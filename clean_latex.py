import re

START_TAG = "% HTML_ONLY_START"
END_TAG = "% HTML_ONLY_END"
FILENAME = "book.tex"
REPLACEMENT = """\\\\begin{sphinxadmonition}{tip}{Tip:}
\\\\sphinxAtStartPar
Extra material for this section can be found on the web version of these notes.
\\\\end{sphinxadmonition}"""

with open(f"course/_build/latex/{FILENAME}", "r") as f:
    contents = f.read()

new = re.sub(r"% HTML_ONLY_START.*?% HTML_ONLY_END",
           REPLACEMENT, contents, flags=re.DOTALL)
    
with open(f"course/_build/latex/{FILENAME}", "w") as f:
    f.write(new)