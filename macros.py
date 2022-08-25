from bs4 import BeautifulSoup

# MACROS

# check file for macro
# replace the macro with html code block

# TOC MACRO
# macro: "[[TOC]]"
# replace with:
# - title
#   - head 1
#       - subhead
#       - subhead
#   - head 2
#       - subhead
#       - subhead

string = "<html><body>[[TOC]]<h1>this is a test</h1><a>this is a sub par</a><h2>sub</h2><h2>sub</h2><h1>test</h1>"

replace = "titel, test 123"

class Macro:
    mdMacro = ""
    file = ""
    def __init__(self, mdMacro, file):
        self.mdMacro = mdMacro
        self.file = file

class TableOfContents(Macro):
    def process(self):
        soup = BeautifulSoup(self.file,"html.parser")
        h1s = soup.findAll("h1")
        toc = ""
        for i in h1s:
            toc += i.string
        soup.find(text="[["+ self.mdMacro +"]]").replace_with(toc)
        print(soup)


TOC = TableOfContents("TOC", string)
TOC.process()
