import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_single(self):
        node = HTMLNode(props={"href": "https://somesite.com"})
        self.assertEqual(node.props_to_html(), ' href="https://somesite.com"')

    def test_props_with_target(self):
        node = HTMLNode(props={"href": "https://somesite.com", "target": "_blank"})
        self.assertIn(' href="https://somesite.com"', node.props_to_html())
        self.assertIn(' target="_blank"', node.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://evilsite.com"})
        self.assertEqual(node.to_html(), '<a href="https://evilsite.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Im BOLD")
        self.assertEqual(node.to_html(), "<b>Im BOLD</b>")

    def test_leaf_to_html_empty_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Some text")
        self.assertEqual(node.to_html(), "Some text")

    def test_leaf_to_html_a_multiple_attribs(self):
        node = LeafNode(
            "a", "Click me!", {"href": "https://evilsite.com", "target": "_blank"}
        )
        html = node.to_html()
        self.assertIn('href="https://evilsite.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertTrue(html.startswith("<a"))
        self.assertTrue(html.endswith(">Click me!</a>"))

    def test_to_html_with_children(self):
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

    def test_to_html_without_parent_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode("", [child_node])

    def test_to_html_with_None_parent_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node])

    def test_to_html_parent_with_None_child(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_to_html_parent_with_blank_child(self):
        with self.assertRaises(ValueError):
            ParentNode("div", "")

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
