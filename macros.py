import copy
from bs4 import BeautifulSoup
import re

# MACROS

string = '<p>[[ TOC 2 ]]</p><h1 id="simple-markdown">Simple markdown</h1><p>To see al the markdown syntax you can visit the <a href="/Markdown%20cheatsheet">markdown cheatsheet</a></p><h1 id="homepage">Homepage</h1><p>The homepage is default the “homepage.md” file, this can’t be changed. If this file doesn’t exist create it in de wiki folder.</p><h2>test</h2>'

class Macro:
    mdMacro = ""
    file = ""
    def __init__(self, file):
        self.file = file
        self.process()
    def process(self):
        try:
            return TableOfContents(self.file).process()
        except Exception:
            return self.file

class TableOfContents():
    """
    MACRO: "TOC" or "TOC <depth>"
    By default the TOC will be 3 levels.
    you can specify the depth with a number
    """

    def __init__(self, file):
        self.file = file

    # first the header type, second the indent
    headers = [
        ["h1",0],
        ["h2",20],
        ["h3",40],
        ["h4",60]
    ]

    def process(self):
        soup = BeautifulSoup(self.file,"html.parser")

        TOC = soup.find(text=re.compile("^\[\[ *(TOC *[0-9]*) *\]\]$"))
        self.mdMacro = TOC
        args = self.mdMacro.strip("[[ ]]").split(" ")
        if len(args) <= 1:
            # default depth is 3
            args.append("3")
        depthHeaders = [item [0] for item in self.headers[0:int(args[1])]]
        listWithHeaders = soup.find_all(depthHeaders)
        
        
        title = soup.new_tag("h4")
        title.string = "Table of content"

        # get all headers
        newsoup = BeautifulSoup()
        newsoup.append(title)
        for i in listWithHeaders:
            newHead = copy.copy(i)
            margin = 0
            for head, indent in self.headers:
                if head == str(i.name):
                    margin = indent
                    break
 
            newHead.name = "p"
            newHead.string.wrap(soup.new_tag("a"))
            newHead["id"] = ""
            newHead.a['style'] = "margin-left: " + str(margin) + "px; font-weight: bold; color:grey; text-decoration: none;"
            newHead.a["href"] = "#" + str(i.get('id'))
            newsoup.append(newHead)
        soup.find(text=TOC).replace_with(newsoup)
        return soup
