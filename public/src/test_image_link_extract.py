import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from extract_links import extract_markdown_images, extract_markdown_links
from split_nodes import (
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)


class TestImageUrlExtract(unittest.TestCase):
    def test_image_extract(self):
        text = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        )
        result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(text, result)

    def test_link_extract(self):
        text = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        result = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(text, result)

    def test_multiple_image_extract(self):
        text = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(text, result)

    def test_multiple_link_extract(self):
        text = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        result = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(text, result)

    def test_alt_text_missing_image(self):
        text = extract_markdown_images(
            "This is text without alt text (https://www.google.com)"
        )
        result = []
        self.assertEqual(text, result)

    def test_missing_image_link(self):
        text = "This is text without a ![link]"
        with self.assertRaises(ValueError):
            extract_markdown_images(text)

    def test_alt_text_missing_link(self):
        text = extract_markdown_links(
            "This is text without alt text (https://www.google.com)"
        )
        result = []
        self.assertEqual(text, result)

    def test_missing_url_link(self):
        text = "This is text without a [link]"
        with self.assertRaises(ValueError):
            extract_markdown_links(text)

    def test_alt_text_missing_content_image(self):
        text = "This is text without content in ![](https://www.google.com)"
        with self.assertRaises(ValueError):
            extract_markdown_images(text)

    def test_missing_content_in_link_image(self):
        text = "This is text without content in the ![link]()"
        with self.assertRaises(ValueError):
            extract_markdown_images(text)

    def test_alt_text_missing_content_url_link(self):
        text = "This is text without alt text content [](https://www.google.com)"
        with self.assertRaises(ValueError):
            extract_markdown_links(text)

    def test_missing_url_link(self):
        text = "This is text without content in the [link]()"
        with self.assertRaises(ValueError):
            extract_markdown_links(text)


class TestImageUrlSplit(unittest.TestCase):
    def test_split_multiple_images(self):
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_complex_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_simple_to_textnodes(self):
        text = "This is **text** with an bold word and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an bold word and a ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ],
            new_nodes,
        )

    def test_plaintext_to_textnodes(self):
        text = "This is plaintext"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is plaintext", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_simple_missing_delimiter_to_textnodes(self):
        text = "This is **text with an bold word and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_simple_missing_alttext_to_textnodes(self):
        text = "This is **text with an bold word and a ![](https://i.imgur.com/fJRm4Vk.jpeg)"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_simple_missing_half_bracket_to_textnodes(self):
        text = "This is **text with an bold word and a ![obi wan image(https://i.imgur.com/fJRm4Vk.jpeg)"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_simple_missing_half_parenthesis_to_textnodes(self):
        text = "This is **text with an bold word and a ![obi wan image]https://i.imgur.com/fJRm4Vk.jpeg)"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_returns(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
