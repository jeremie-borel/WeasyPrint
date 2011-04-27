# coding: utf8

from attest import Tests, assert_hook
from lxml import html
#from lxml.html import html5parser as html  # API is the same as lxml.html
from cssutils.helper import path2url

from ..css import find_stylesheets

from . import resource_filename


suite = Tests()

def parse_html(filename):
    """Parse an HTML file from the test resources and resolve relative URL."""
    document = html.parse(path2url(resource_filename(filename)))
    document.getroot().make_links_absolute()
    return document


#@suite.test
#def foo():
#    source = u"<P id=greetings>今日は <em>html5lib</em>!"
#    doc = html.document_fromstring(source)
#    p = doc.cssselect('p')[0]
#    p.foo = 42
#    assert doc[0][0].foo == 42
#    assert doc[0][0] is p
#    assert p.tag == 'p'
#    assert p.get('id') == 'greetings'
#    assert 2+2 == 5

@suite.test
def test_find_stylesheets():
    document = parse_html('doc1.html')
    root = document.getroot()
    style, link = root[0]
    assert style.tag == 'style'
    assert link.tag == 'link'
    p, = root[1]
    
    sheets = find_stylesheets(document)
    assert len(sheets) == 2
    assert set(s.href.rsplit('/', 1)[-1] for s in sheets) == set(
        ['doc1.html', 'sheet1.css'])

