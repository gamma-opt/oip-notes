import re

START_TAG = "% HTML_ONLY_START"
END_TAG = "% HTML_ONLY_END"
FILENAME = "book.tex"

def repl(matchobj):
    return f"""\\begin{{sphinxadmonition}}{{tip}}{{Tip:}}
\\sphinxAtStartPar
Extra material for this section can be found on the web version of these notes \\sphinxhref{{{matchobj.group(1)}}}{{here}}.
\\end{{sphinxadmonition}}"""

with open(f"course/_build/latex/{FILENAME}", "r") as f:
    contents = f.read()

new = re.sub(f"{START_TAG} (.*?$).*?{END_TAG}",
           repl, contents, flags=re.DOTALL + re.MULTILINE)
    
with open(f"course/_build/latex/{FILENAME}", "w") as f:
    f.write(new)