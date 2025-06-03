import unittest
from main import extract_title


class TestMain(unittest.TestCase):
    def test_header(self):
        md = """
# This is the main heading

## This is a level 2 header

### This is a level 3 header
"""
        header = extract_title(md)
        result = "This is the main heading"
        self.assertEqual(header, result)

    def test_no_layer1_header(self):
        md = """
## This is a level 2 header

### This is a level 3 header
"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_bad_format_header(self):
        md = """
#This is the main heading

## This is a level 2 header

### This is a level 3 header
"""
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
