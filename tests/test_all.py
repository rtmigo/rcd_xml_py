import unittest

from rcd_xml import remove_xmldecl
from rcd_xml import remove_xmlns


class Test519(unittest.TestCase):
    def test_removeXmlDecl(self):
        assert remove_xmldecl(
            '<?xml version="1.0"?><root>ha</root>') == '<root>ha</root>'
        assert remove_xmldecl(
            ' < ? xml version="1.0" encoding="UTF-8" ? ><root>ha</root>') == '<root>ha</root>'


class TestRemove(unittest.TestCase):
    def test(self):
        self.assertEqual(
            remove_xmlns(
                "<sparql xmlns='http://www.w3.org/2005/sparql-results#'>"),
            "<sparql>", )
