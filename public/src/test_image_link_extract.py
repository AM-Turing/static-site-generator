import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from extract_links import extract_markdown_images, extract_markdown_links


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
        text = "This is text without alt text (https://www.google.com)"
        with self.assertRaises(ValueError):
            extract_markdown_images(text)

    def test_missing_image_link(self):
        text = "This is text without a ![link]"
        with self.assertRaises(ValueError):
            extract_markdown_images(text)

    def test_alt_text_missing_link(self):
        text = "This is text without alt text (https://www.google.com)"
        with self.assertRaises(ValueError):
            extract_markdown_links(text)

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


if __name__ == "__main__":
    unittest.main()
