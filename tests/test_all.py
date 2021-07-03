import unittest

from rcd_xml import removeXmlDecl, removeXmlNamespace


class Test519(unittest.TestCase):
	def test_removeXmlDecl(self):
		assert removeXmlDecl(
			'<?xml version="1.0"?><root>ha</root>') == '<root>ha</root>'
		assert removeXmlDecl(
			' < ? xml version="1.0" encoding="UTF-8" ? ><root>ha</root>') == '<root>ha</root>'


class TestRemove(unittest.TestCase):
    def test(self):
        self.assertEqual("<sparql>", removeXmlNamespace(
            "<sparql xmlns='http://www.w3.org/2005/sparql-results#'>"))