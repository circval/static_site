import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from textnodesplitter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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
  
    def test_text_to_html1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_to_html2(self):
        node = TextNode("{code goes here}", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "{code goes here}")
    def test_text_to_html3(self):
        node = TextNode("google.com", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "", "src" "alt")
    def test_text_to_html4(self):
        node = TextNode("google.com", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertNotEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "", "src" "alt")
        
    def test_node_split1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])
    def test_node_split2(self):
        node = TextNode("This is text with a bold **word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a bold ", TextType.TEXT), TextNode("word", TextType.BOLD),])
    def test_node_split3(self):
        node = TextNode("This is text with a bold **word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertNotEqual(new_nodes, [TextNode("This is text with a bold ", TextType.TEXT), TextNode("word", TextType.BOLD),])
    def test_node_split4(self):
        node = TextNode("_This_ is text with an italic word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This", TextType.ITALIC), TextNode(" is text with an italic word", TextType.TEXT),])
        
    def test_extract_markdown_images1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with an ![image has spaces](**invalid link**)"
        )
        self.assertListEqual([("image has spaces", "**invalid link**")], matches)
    def test_extract_markdown_images_invalid(self):
        matches = extract_markdown_images(
            "This is text with an [image has spaces](invalid link)"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links1(self):
        matches = extract_markdown_links(
            "This is text with an [google](google.com)"
        )
        self.assertListEqual([("google", "google.com")], matches)
    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with an [imgur link](imgur.com)"
        )
        self.assertListEqual([("imgur link", "imgur.com")], matches)
        
if __name__ == "__main__":
        unittest.main()
