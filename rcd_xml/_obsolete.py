import warnings
from typing import List, Any

from lxml import etree
from lxml.etree import _ElementTree, _Element

from rcd_xml import remove_xmlns
from rcd_xml._rxml import html_file_to_tree, find_xpath, find_xpath_one, \
    html_bytes_to_etree, html_code_to_etree, tree_to_str, inner_text, \
    is_element, is_text, is_comment, add_text, list_child_nodes, str_to_tree, \
    remove_xmldecl, xml_file_to_tree, stripped_xml_file_to_tree, \
    remove_trailing_space, tree_to_file, html_anchor_to_link, find_css


def htmlFileToTree(filename: str, recover=True) -> etree.ElementTree:
    warnings.warn("Use html_file_to_etree", DeprecationWarning)
    return html_file_to_tree(filename, recover)


def findCss(node: etree.Element, css: str) -> List[etree.Element]:
    warnings.warn("Use find_css", DeprecationWarning)
    return find_css(node, css)


def findXpath(node, xpath: str) -> List[etree.Element]:
    warnings.warn("Use find_xpath", DeprecationWarning)
    return find_xpath(node, xpath)


def findXpathOne(node, xpath):
    warnings.warn("Use find_xpath_one", DeprecationWarning)
    return find_xpath_one(node, xpath)


def htmlBytesToTree(outerHTML: bytes) -> _ElementTree:
    warnings.warn("Use html_bytes_to_etree", DeprecationWarning)
    return html_bytes_to_etree(outerHTML)


def htmlCodeToTree(outerHTML: str) -> etree.ElementTree:
    warnings.warn("Use html_code_to_etree", DeprecationWarning)
    return html_code_to_etree(outerHTML)


def treeToStr(node):
    warnings.warn("Use tree_to_str", DeprecationWarning)
    return tree_to_str(node)


def innerText(node: _Element) -> str:
    warnings.warn("Use inner_text", DeprecationWarning)
    return inner_text(node)


def innerText_old(node, blank=""):
    # этот метод считает текст внутри комментариев столь же ценным, как внутри
    # элементов, и порой это приводит к нежелательным результатам
    warnings.warn("Obsolete", DeprecationWarning)
    return blank.join([x for x in node.itertext()])


def isElement(node: Any) -> bool:
    warnings.warn("Use is_element", DeprecationWarning)
    return is_element(node)


def isText(node: Any) -> bool:
    warnings.warn("Use is_text", DeprecationWarning)
    return is_text(node)


def isComment(node: Any) -> bool:
    warnings.warn("Use is_comment", DeprecationWarning)
    return is_comment(node)


def addText(parent: _Element, text: str):
    warnings.warn("Use add_text", DeprecationWarning)
    add_text(parent, text)


def listChildNodes(parent: _Element) -> List:
    warnings.warn("Obsolete", DeprecationWarning)
    return list_child_nodes(parent)


def removeXmlDecl(xmlText):
    warnings.warn("Obsolete", DeprecationWarning)
    return remove_xmldecl(xmlText)


def strToTree(xml_code: str) -> _ElementTree:
    warnings.warn("Obsolete", DeprecationWarning)
    return str_to_tree(xml_code)


def xmlFileToTree(filename: str, recover=False) -> _ElementTree:
    warnings.warn("Obsolete", DeprecationWarning)
    return xml_file_to_tree(filename, recover)


def removeTrailingSpaces(xmlText: str) -> str:
    warnings.warn("Obsolete", DeprecationWarning)
    return remove_trailing_space(xmlText)


def xmlFileToTreeNoNS(filename: str) -> _ElementTree:
    warnings.warn("Obsolete", DeprecationWarning)
    return stripped_xml_file_to_tree(filename)


def htmlAnchorToLink(elementA, baseUrl):
    warnings.warn("Obsolete", DeprecationWarning)
    return html_anchor_to_link(elementA, baseUrl)


def treeToFile(node, filename):
    warnings.warn("Obsolete", DeprecationWarning)
    tree_to_file(node, filename)


def removeXmlNamespace(xmlText: str) -> str:
    warnings.warn("Use remove_xml_namespace", DeprecationWarning)
    return remove_xmlns(xmlText)
