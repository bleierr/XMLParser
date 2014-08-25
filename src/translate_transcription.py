from lxml import etree
import os, re, types
from StringIO import StringIO

#do not encode in unicode when opening, e.g. with codecs module
with open("xml"+os.sep+"confessio_msparis_diplomatic_transcription.xml", "r") as f:
    try:
        xml = StringIO(f.read())
        parser = etree.XMLParser(encoding="utf-8", resolve_entities=False)
        tree = etree.parse(xml, parser=parser)
        
    except etree.XMLSyntaxError as e:
        print e

xml = StringIO("<surface><l><w n='1'>exam<ex>ABBR</ex>ple</w><w n='2'>Word2</w></l></surface>")
tree = etree.parse(xml, parser=parser)
       
def remove_ns(strg):
    #if callable(e.tag):
        #return None
    return re.findall("\w+", strg)[-1]
    

def eSpace(n):
    if '+' in n:
        n = n[0:-1]
    try:
        n = round(float(n))
    except ValueError:
        print n
    return "<span class='space'>"+str(int(n))+str("&nbsp"*int(n))+"<\span>"
    

                  
class XMLTree(object):
    def __init__(self):
        self.html = []
        
    def surface(self, e):
        self.html.append("<div class='surface'>")
        self.loop(e)
        self.html.append("</div>")
        if e.tail:
            self.html(e.tail)
            
    def ex(self, e):
        self.html.append("<div class='ex'>")
        self.loop(e)
        self.html.append("</div>")
        if e.tail:
            self.html.append(e.tail)             
                    
    def w(self, e):
        if e.get("n"):
            for k, v in e.items():
                if k == 'n' and v == '2':
                    self.html.append("<div class='w'>")
                    self.loop(e)
                    self.html.append("</div>")
                    if e.tail:
                        self.html.append(e.tail)
            
    def loop(self, e):
        if e.text:
            self.html.append(e.text)
        if e.getchildren():
            for c in e.getchildren():
                name = remove_ns(c.tag)
                if name in dir(self):
                    getattr(self, name)(c)
                else:
                    self.loop(c)

  
lst = []
root = tree.getroot()
xml = XMLTree()
head = "<html><head><title>Title</title></head><body>"
xml.html.append(head)
"""for e in root.getchildren():
    xml.sourceDoc(e)"""
xml.loop(root)
    
end = "</body></html>"    
xml.html.append(end)
with open("output.html", "w") as f:
    f.write("".join(xml.html))
        

    


