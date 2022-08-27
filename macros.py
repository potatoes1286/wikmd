import copy
from bs4 import BeautifulSoup

# MACROS

string = "<html><body>[[TOC]]<h1 id='head1'>this is a test</h1><a>this is a sub par</a><h2 id='head2'>sub</h2><h3>testingggg</h3><h2>sub</h2><h1>test</h1></body></html>"

class Macro:
    mdMacro = ""
    file = ""
    def __init__(self, mdMacro, file):
        self.mdMacro = mdMacro
        self.file = file


class TableOfContents(Macro):
    """
    MACRO: "TOC" or "TOC <depth>"
    By default the TOC will be 3 levels.
    you can specify the depth with a number
    """

    # first the header type, second the indent
    headers = [
        ["h1",0],
        ["h2",20],
        ["h3",40],
        ["h4",60]
    ]

    def process(self):
        args = self.mdMacro.split(" ")
        soup = BeautifulSoup(self.file,"html.parser")
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
        soup.find(text="[["+ args[0] +"]]").replace_with(newsoup)
        return(soup)


TOC = TableOfContents("TOC", string)
TOC.process()
