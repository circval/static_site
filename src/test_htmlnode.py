import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
if __name__ == "__main__":
        unittest.main()
