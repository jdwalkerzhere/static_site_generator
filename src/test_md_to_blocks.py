import unittest

from md_to_blocks import block_to_block_type, markdown_to_blocks

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

        block_types = [block_to_block_type(block) for block in blocked_md]
        expected_output = ['HEADING', 'PARAGRAPH', 'UNORDERED_LIST']

        for block_type, actual_type in zip(block_types, expected_output):
            self.assertEqual(block_type, actual_type)

    def test_md_block_types(self):
        paragraph = 'im just # text'
        para_type = block_to_block_type(paragraph)
        self.assertEqual(para_type, 'PARAGRAPH')

        heading = '#### im a heading'
        heading_type = block_to_block_type(heading)
        self.assertEqual(heading_type, 'HEADING')

        code = '```import re\ntext="stuff *is* weird"\nre.match(r".", text)```'
        code_type = block_to_block_type(code)
        self.assertEqual(code_type, 'CODE')

        quote = '> hi there\n> im a quote'
        quote_type = block_to_block_type(quote)
        self.assertEqual(quote_type, 'QUOTE')

        unordered = '* thing\n- another thing\n* another thing'
        unordered_list_type = block_to_block_type(unordered)
        self.assertEqual(unordered_list_type, 'UNORDERED_LIST')

        ordered = '1. thing\n2. another thing\n3. another thing'
        ordered_list_type = block_to_block_type(ordered)
        self.assertEqual(ordered_list_type, 'ORDERED_LIST')
