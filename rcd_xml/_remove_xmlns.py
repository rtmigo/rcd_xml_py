import re
import warnings


def remove_xmlns(xml_text: str) -> str:

    return re.sub(r'''\sxmlns\s*=\s*
                   (?: (?:"[^"]+") | (?:'[^']+') ) 
                   ''',
                  '', xml_text, count=1, flags=re.MULTILINE | re.VERBOSE)


def removeXmlNamespace(xmlText: str) -> str:
    warnings.warn("Use remove_xml_namespace", DeprecationWarning)
    return remove_xmlns(xmlText)