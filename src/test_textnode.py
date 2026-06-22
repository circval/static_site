import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from textnodesplitter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
    
    
    def test_split_images1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images2(self):
        node = TextNode(
            "![This is text with an image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images3(self):
        node = TextNode(
            "This is text with ![an image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_links1(self):
        node = TextNode(
            "This is text with a [link](google.com) and another [second link](wikipedia.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "wikipedia.com"),
            ],
            new_nodes,
        )
    def test_split_links2(self):
        node = TextNode(
            "[First link, ](google.com)[second link, ](PBS.com)[third link.](wikipedia.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First link, ", TextType.LINK, "google.com"),
                TextNode("second link, ", TextType.LINK, "PBS.com"),
                TextNode("third link.", TextType.LINK, "wikipedia.com"),
            ],
            new_nodes,
        )
        
    def test_text_to_textnode_1(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
                [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")],
                new_nodes)       
    def test_text_to_textnode_2(self):
        node = "This is **text** with an _italic_ word and a `code block` and a **bold broken obi wan image**](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
                [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("bold broken obi wan image", TextType.BOLD, None),
                TextNode("](https://i.imgur.com/fJRm4Vk.jpeg) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")],
                new_nodes)     
    def test_text_to_textnode_3(self):
        node = "This is **text** with _italic words_ and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
                [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("italic words", TextType.ITALIC),
                TextNode(" and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")],
                new_nodes)
        
if __name__ == "__main__":
        unittest.main()
