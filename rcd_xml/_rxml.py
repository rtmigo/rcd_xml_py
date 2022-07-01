import re
import urllib.parse
from pathlib import Path
from typing import *

import cssselect
from lxml import etree
from lxml.etree import _Element, _ElementTree, _ElementUnicodeResult

from rcd_xml._remove_xmlns import remove_xmlns


class NotFoundError(Exception):
    pass


def inner_text(node: _Element) -> str:
    return etree.tostring(node,
                          method="text",
                          encoding="utf-8").decode()


def add_text(parent: _Element, text: str):
    # добавляет текст в конец элемента

    def append_str(lhs: str, rhs: str) -> str:
        return lhs + rhs if lhs else rhs

    # To insert text before any children of a node, use the node's text
    # attribute. To insert text after the child of a node, use that child's
    # tail attribute.
    children = parent.getchildren()
    if not children:
        parent.text = append_str(parent.text, text)
    else:
        children[-1].tail = append_str(children[-1].tail, text)


def list_child_nodes(parent: _Element) -> List:
    # возвращает непосредственно дочерние узлы. Которые могут быть
    # элементами, текстом, комментариями
    return parent.xpath("child::node()")


def is_element(node: Any) -> bool:
    return isinstance(node, _Element) and node.tag is not etree.Comment


def is_text(node: Any) -> bool:
    return isinstance(node, _ElementUnicodeResult)


def is_comment(node: Any) -> bool:
    return isinstance(node, _Element) and node.tag is etree.Comment


def find_xpath(node: _Element, xpath: str) -> List[_Element]:
    return etree.XPath(xpath)(node)


def find_css(node: _Element, css: str) -> List[_Element]:
    return etree.XPath(cssselect.GenericTranslator().css_to_xpath(css))(node)


def find_xpath_one(node: _Element, xpath: str) -> Optional[_Element]:
    lst = find_xpath(node, xpath)
    if len(lst) == 1:
        result = lst[0]
        assert result is not None
        return result
    if len(lst) == 0:
        return None
    raise NotFoundError("1 node expected, %d found." % len(lst))


def remove_xmldecl(xml_text: str) -> str:
    # Удаляет XML Declaration из начала строки.
    # Это хак, помогающий в простейших случаях избежать ошибки "Failed to
    # loadMultiple external entity "<?xml version="1.0"?>".
    xml_text = re.sub(r'^\s*<\s*\?[^>]*\?\s*>', "", xml_text, 1,
                      flags=re.MULTILINE)
    return xml_text


def remove_trailing_space(xml_text: str) -> str:
    return re.sub(r">\s+$", ">", xml_text, count=1, flags=re.MULTILINE)


def str_to_tree(xml_code: str) -> _ElementTree:
    # загружает из строки XML-данные. Рассчитан на простейший случай,
    # когда в данных нет отсылок к другим документам и entities.

    xml_code = remove_xmldecl(xml_code)
    xml_code = remove_xmlns(xml_code)
    return etree.fromstring(xml_code)


def xml_file_to_tree(filename: Union[Path, str], recover=False) -> _ElementTree:
    # на самом деле etree._ElementTree:

    parser = etree.XMLParser(recover=recover)
    tree = etree.parse(str(filename), parser)
    return tree


def stripped_xml_file_to_tree(filename: str) -> _ElementTree:
    with open(filename, "rt") as f:
        xmlText = f.read()

    xmlText = remove_xmldecl(xmlText)
    xmlText = remove_xmlns(xmlText)
    if not xmlText.endswith(">"):
        xmlText = remove_trailing_space(xmlText)

    return etree.fromstring(xmlText)


def html_file_to_tree(filename: Union[Path, str], recover=True) \
        -> etree.ElementTree:
    # на самом деле возвращается etree._ElementTree:
    parser = etree.HTMLParser(recover=recover)
    tree = etree.parse(str(filename), parser)
    return tree


def tree_to_file(node, filename):
    node.write(filename, pretty_print=True)


def tree_to_str(node: Union[_Element, _ElementTree]) -> str:
    return etree.tostring(node, pretty_print=True).decode()


def html_bytes_to_etree(outer_html: bytes) -> _ElementTree:
    from io import BytesIO
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(outer_html), parser)
    return tree


def html_code_to_etree(outer_html: str) -> _ElementTree:
    from io import BytesIO
    outerHtmlBytes = outer_html.encode("utf-8")
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(outerHtmlBytes), parser)
    return tree


def html_anchor_to_link(elem, base_url):
    try:
        href = elem.attrib["href"]
    except KeyError:
        return None
    return urllib.parse.urljoin(base_url, href)
