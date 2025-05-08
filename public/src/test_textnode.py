import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
