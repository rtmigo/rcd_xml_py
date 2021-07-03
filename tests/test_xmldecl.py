import unittest

from rcd_xml import removeXmlDecl


class Test519(unittest.TestCase):
	def test_removeXmlDecl(self):
		assert removeXmlDecl(
			'<?xml version="1.0"?><root>ha</root>') == '<root>ha</root>'
		assert removeXmlDecl(
			' < ? xml version="1.0" encoding="UTF-8" ? ><root>ha</root>') == '<root>ha</root>'