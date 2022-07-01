import re


def remove_xmlns(xml_text: str) -> str:
    return re.sub(r'''\sxmlns\s*=\s*
                   (?: (?:"[^"]+") | (?:'[^']+') ) 
                   ''',
                  '', xml_text, count=1, flags=re.MULTILINE | re.VERBOSE)

# noinspection PyPep8Naming
