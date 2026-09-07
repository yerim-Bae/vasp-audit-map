"""Read source XML without losing table row/column boundaries."""
import html
import json
import re
import zipfile
from html.parser import HTMLParser
from dart_client import ROOT

class Node:
    def __init__(self, tag, attrs=None):
        self.tag, self.attrs, self.children = tag, dict(attrs or []), []
    def text(self):
        return ' '.join(''.join(c if isinstance(c, str) else c.text() + ' ' for c in self.children).split())
    def all(self, tag):
        for child in self.children:
            if isinstance(child, Node):
                if child.tag == tag:
                    yield child
                yield from child.all(tag)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in ('br','img','hr','meta','link','input','col'):
            self.stack.append(node)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def documents(receipt):
    with zipfile.ZipFile(ROOT/'downloads'/(receipt+'.zip')) as archive:
        for name in archive.namelist():
            if not name.lower().endswith('.xml'):
                continue
            raw = archive.read(name)
            encoding = re.search(br'encoding=["\']([^"\']+)', raw[:180])
            text = raw.decode(encoding[1].decode() if encoding else 'utf-8', errors='replace')
            parser = Parser()
            parser.feed(text)
            yield name, parser.root

def rows(table):
    return [[c.text() for c in row.children if isinstance(c,Node) and c.tag in ('td','th','tu','te')] for row in table.all('tr')]

if __name__ == '__main__':
    import sys
    for receipt in sys.argv[1:]:
        print('\nRECEIPT',receipt)
        for name, root in documents(receipt):
            text = root.text()
            print('MEMBER',name,'chars',len(text),'tables',len(list(root.all('table'))))
            if '독립된 감사' in text[:6000] or '감 사 보 고 서' in text[:4000]:
                print(text[:6000])
