import urllib.parse
import warnings
from typing import *

import cssselect
from lxml import etree


def innerText(node: etree.Element) -> str:
    return etree.tostring(node, method="text",
                          encoding="utf-8").decode()  # .decode()


def innerText_old(node, blank=""):
    # этот метод считает текст внутри комментариев столь же ценным, как внутри
    # элементов, и порой это приводит к нежелательным результатам
    return blank.join([x for x in node.itertext()])


def addText(parent: etree.Element, text: str):
    # добавляет текст в конец элемента

    def appendStr(lhs: str, rhs: str) -> str:
        return lhs + rhs if lhs else rhs

    # To insert text before any children of a node, use the node's text
    # attribute. To insert text after the child of a node, use that child's
    # tail attribute.
    children = parent.getchildren()
    if not children:
        parent.text = appendStr(parent.text, text)
    else:
        children[-1].tail = appendStr(children[-1].tail, text)


def listChildNodes(parent: etree.Element) -> List:
    # возвращает непосредственно дочерние узлы. Которые могут быть
    # элементами, текстом, комментариями
    return parent.xpath("child::node()")


def isElement(node: object) -> bool:
    return isinstance(node, etree._Element) and node.tag is not etree.Comment


def isText(node: object) -> bool:
    return isinstance(node, etree._ElementUnicodeResult)


def isComment(node: object) -> bool:
    return isinstance(node, etree._Element) and node.tag is etree.Comment


# return isinstance(arg, etree._ElementUnicodeResult)


def findXpath(node, xpath: str) -> List[etree.Element]:
    return etree.XPath(xpath)(node)


def find_css(node: etree.Element, css: str) -> List[etree.Element]:
    return etree.XPath(cssselect.GenericTranslator().css_to_xpath(css))(node)


def findCss(node: etree.Element, css: str) -> List[etree.Element]:
    warnings.warn("Use find_css", DeprecationWarning)
    return find_css(node, css)


class NotFoundError(Exception):
    pass


def findXpathOne(node, xpath):
    lst = findXpath(node, xpath)
    if len(lst) == 1:
        assert lst[0] is not None
        return lst[0]
    if len(lst) == 0:
        return None
    raise NotFoundError("1 node expected, %d found." % len(lst))


# WTF https://www.behance.net/rbrt/resume

def removeXmlDecl(xmlText):
    # Удаляет XML Declaration из начала строки.
    # Это хак, помогающий в простейших случаях избежать ошибки "Failed to
    # loadMultiple external entity "<?xml version="1.0"?>".
    import re
    xmlText = re.sub('''^\s*<\s*\?[^>]*\?\s*>''', "", xmlText, 1,
                     flags=re.MULTILINE)
    return xmlText


def removeXmlNamespace(xmlText: str) -> str:
    import re

    return re.sub(r'''\sxmlns\s*=\s*
                   (?: (?:"[^"]+") | (?:'[^']+') ) 
                   ''',
                  '', xmlText, count=1, flags=re.MULTILINE | re.VERBOSE)


def removeTrailingSpaces(xmlText: str) -> str:
    import re
    return re.sub(">\s+$", ">", xmlText, count=1, flags=re.MULTILINE)


# print(removeXmlNamespace("<sparql xmlns='http://www.w3.org/2005/sparql-results#'>"))
# exit()

# odnoklassniki


def strToTree(xmlcode: str) -> etree._ElementTree:
    # загружает из строки XML-данные. Рассчитан на простейший случай,
    # когда в данных нет отсылок к другим документам и entitites.

    xmlcode = removeXmlDecl(xmlcode)
    xmlcode = removeXmlNamespace(xmlcode)
    return etree.fromstring(xmlcode)


def xmlFileToTree(filename: str,
                  recover=False) -> etree.ElementTree:
    # на самом деле etree._ElementTree:

    parser = etree.XMLParser(recover=recover)
    tree = etree.parse(filename, parser)
    return tree


def xmlFileToTreeNoNS(
        filename: str) -> etree.ElementTree:  # на самом деле etree._ElementTree:

    with open(filename, "rt") as f:
        xmlText = f.read()

    # №print("1", flush=True)
    xmlText = removeXmlDecl(xmlText)
    # print("2", flush=True)
    xmlText = removeXmlNamespace(xmlText)
    if not xmlText.endswith(">"):
        xmlText = removeTrailingSpaces(xmlText)
    # if not xmlText.endswith(">"):
    # print(xmlText[-10:])
    #	raise ValueError("The XML does not end with '>'.")

    # print("3", flush=True)

    return etree.fromstring(xmlText)

    """
    from io import StringIO, FileIO
    import xml.etree.ElementTree as ET

    with FileIO(filename) as f:

    # instead of ET.fromstring(xml)
        it = ET.iterparse(f)
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        return it
    """


def htmlFileToTree(filename: str,
                   recover=True) -> etree.ElementTree:  # на самом деле etree._ElementTree:

    parser = etree.HTMLParser(recover=recover)
    tree = etree.parse(filename, parser)
    return tree


def treeToFile(node, filename):
    # str = etree.tostring(root, pretty_print=True)
    # et = etree.ElementTree(root)
    # et.write(sys.stdout, pretty_print=True)

    # with open(filename, 'w') as file:
    node.write(filename, pretty_print=True)


def treeToStr(node):
    return etree.tostring(node, pretty_print=True).decode()


def htmlBytesToTree(outerHTML: bytes) -> etree.ElementTree:
    from io import BytesIO

    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(outerHTML), parser)

    return tree


def htmlCodeToTree(outerHTML: str) -> etree.ElementTree:
    # на самом деле возвращается etree._ElementTree:

    from io import BytesIO

    outerHtmlBytes = outerHTML.encode("utf-8")

    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(outerHtmlBytes), parser)

    return tree


def htmlAnchorToLink(elementA, baseUrl):
    try:
        href = elementA.attrib["href"]
    except KeyError:
        return None
    return urllib.parse.urljoin(baseUrl, href)
