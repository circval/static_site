import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
	def test_eq(self):
        	node = TextNode("This is a text node", TextType.BOLD)
        	node2 = TextNode("This is a text node", TextType.BOLD)
        	self.assertEqual(node, node2)

	def test_noneq(self):
		node = TextNode("This node isn't equal1", TextType.CODE)
		node2 = TextNode("This node isn't equal2", TextType.CODE)
		self.assertNotEqual(node, node2)

	def test_noneq2(self):
                node = TextNode("This node isn't equal1", TextType.CODE)
                node2 = TextNode("This node isn't equal2", TextType.CODE, url = None)
                self.assertNotEqual(node, node2)

	def test_noneq3(self):
                node = TextNode("This node isn't equal", TextType.CODE)
                node2 = TextNode("This node isn't equal", TextType.ITALIC)
                self.assertNotEqual(node, node2)

if __name__ == "__main__":
    	unittest.main()
