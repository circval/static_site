import unittest
from htmlnode import HTMLNode, LeafNode

class HTMLTestNode(unittest.TestCase):
	def test_1(self):
		bold_node = HTMLNode("b", "bold text")
		node = HTMLNode(props={"href": "https://www.google.com"})
		self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
	def test_2(self):
		node = HTMLNode(tag="h1", value="Hello World")
		self.assertEqual(node.tag, "h1")
	def test_3(self):
		bold_node = HTMLNode("b", "bold text")
		node = HTMLNode("p", "google it", [bold_node], {"href": "https://www.google.com"})
		self.assertNotEqual(node.props_to_html(), ' href="https://www.gogle.com"')
  

	def test_leaf_to_html_p_1(self):
		node = LeafNode("a", "read this")
		self.assertEqual(node.to_html(), "<a>read this</a>")
	def test_leaf_to_html_p_2(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
	def test_leaf_to_html_p_3(self):
		node = LeafNode("q", "Hello, world!")
		self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")
  
if __name__ == "__main__":
		unittest.main()
