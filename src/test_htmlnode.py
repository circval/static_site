import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from html_conversion import markdown_to_html_node

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
  
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_greatgrandchildren(self):
        greatgrandchild_node = LeafNode("c", "greatgrandchild")
        grandchild_node = ParentNode("table", [greatgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><table><c>greatgrandchild</c></table></span></div>",
        )
    def test_to_html_with_2children(self):
        child_node1 = LeafNode("par", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><par>child1</par><span>child2</span></div>",
        )
    def test_to_html_with_2children_not_equal(self):
        child_node1 = LeafNode("par", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertNotEqual(
            parent_node.to_html(),
            "<div><span><par>child1child2</par></span></div>",
        )
        
def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

if __name__ == "__main__":
        unittest.main()
