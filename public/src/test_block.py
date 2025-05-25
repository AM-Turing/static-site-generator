import unittest
from block import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    def test_code_block(self):
        markdown = "```\ndef foo():\n    return 'bar'\n```"
        self.assertEqual(block_to_block_type(markdown), BlockType.CODE)

    def test_heading_level_1(self):
        markdown = "# Heading 1"
        self.assertEqual(block_to_block_type(markdown), BlockType.HEADING)

    def test_heading_level_6(self):
        markdown = "###### Heading 6"
        self.assertEqual(block_to_block_type(markdown), BlockType.HEADING)

    def test_blockquote(self):
        markdown = "> This is a quote\n> continued on next line"
        self.assertEqual(block_to_block_type(markdown), BlockType.QUOTE)

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(markdown), BlockType.UNORDERED_LIST)

    def test_valid_ordered_list(self):
        markdown = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(markdown), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list_not_sequential(self):
        markdown = "1. First\n2. Second\n4. Not Third"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_single_paragraph(self):
        markdown = "This is just a plain paragraph with no special formatting."
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_code_block_incorrect_end(self):
        markdown = "```\ncode starts\nnot closed properly"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_mixed_blockquote_and_paragraph(self):
        markdown = "> This is a quote\nThis is not"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
