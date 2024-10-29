import unittest

from md_to_blocks import markdown_to_blocks

class TestMDtoBlocks(unittest.TestCase):
    def test_md_to_blocks(self):
        md = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        blocked_md = markdown_to_blocks(md)
        expected_output = ['# This is a heading',
                           'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                           '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(blocked_md, expected_output)
