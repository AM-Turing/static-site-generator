import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_bold(self):
        node = TextNode("This is some text", TextType.BOLD)
        node2 = TextNode("This is some different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_italic(self):
        node = TextNode("This is some text", TextType.ITALIC)
        node2 = TextNode("This is some text", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq_italic(self):
        node = TextNode("This is some text", TextType.ITALIC)
        node2 = TextNode("This is some different text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_code(self):
        node = TextNode("function speak() {\n return 'hello world'; \n}", TextType.CODE)
        node2 = TextNode(
            "function speak() {\n return 'hello world'; \n}", TextType.CODE
        )
        self.assertEqual(node, node2)

    def test_not_eq_code(self):
        node = TextNode("function speak() {\n return 'hello world'; \n}", TextType.CODE)
        node2 = TextNode("function silence() {\n return 'shh...'; \n}", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("link text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("link text", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_link(self):
        node = TextNode("link text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("link2 text", TextType.LINK, "https://booted.dev")
        self.assertNotEqual(node, node2)

    def test_link_none(self):
        node = TextNode("Link text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link text", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_eq_image(self):
        node = TextNode("Image text", TextType.IMAGE, "https://site.dev/image.jpg")
        node2 = TextNode("Image text", TextType.IMAGE, "https://site.dev/image.jpg")
        self.assertEqual(node, node2)

    def test_not_eq_image(self):
        node = TextNode("Image text", TextType.IMAGE, "https://site.dev/image.jpg")
        node2 = TextNode(
            "Image text other", TextType.IMAGE, "https://other_site.dev/image2.jpg"
        )
        self.assertNotEqual(node, node2)

    def test_different_text_types(self):
        node = TextNode("This is some text", TextType.BOLD)
        node2 = TextNode("This is some text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_exception(self):
        node = TextNode("This is a text node", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_bold(self):
        node = TextNode("This is a bolded text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bolded text node")

    def test_italic(self):
        node = TextNode("This is a italicized text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italicized text node")

    def test_code(self):
        node = TextNode('print("This is a code block node")', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, 'print("This is a code block node")')

    def test_link(self):
        node = TextNode("text about the site", TextType.LINK, "https://somesite.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "text about the site")
        self.assertEqual(html_node.props, {"href": "https://somesite.com"})

    def test_image(self):
        node = TextNode("alt text for image", TextType.IMAGE, "https://somesite.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://somesite.com", "alt": "alt text for image"},
        )

    def test_delimititer_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_delimititer_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_delimititer_code(self):
        node = TextNode(
            "This is text with a `print('hello world')` block", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "print('hello world')")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " block")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_multi_delimititer_bold(self):
        node = TextNode("This is **text** with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " with a ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " word")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_delimititer_empty(self):
        node = TextNode("This is text with a `` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, " block")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_nested_delimititer(self):
        node = TextNode(
            "This is text with **bold and _italic_ nested** words", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold and _italic_ nested")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " words")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_delimititer_beginning(self):
        node = TextNode("_This_ is an italic word at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, " is an italic word at the beginning")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_delimititer_end(self):
        node = TextNode("This is an italic word at the _end_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is an italic word at the ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "end")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_delimititer_alone(self):
        node = TextNode("_all by myself_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "all by myself")
        self.assertEqual(new_nodes[0].text_type, TextType.ITALIC)

    def test_delimititer_missing(self):
        node = TextNode("Only one _delimiter here", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
