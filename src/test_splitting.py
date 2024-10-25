import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes


class TestTextSplitting(unittest.TestCase):
    def split_expected(self):
        text_node = TextNode(text='Hello there *my* **name** `is jesse`', type=TextType.TEXT)
        expected_output = [TextNode(text='Hello there ', type=TextType.TEXT),
                           TextNode(text='my', type=TextType.ITALIC),
                           TextNode(text=' ', type=TextType.TEXT),
                           TextNode(text='name', type=TextType.BOLD),
                           TextNode(text=' ', type=TextType.TEXT),
                           TextNode(text='is jesse', type=TextType.CODE)]
        split_code = split_nodes([text_node], '`', TextType.CODE)
        split_bold = split_nodes(split_code, '**', TextType.BOLD)
        split_italic = split_nodes(split_bold, '*', TextType.ITALIC)
        self.assertEqual(split_italic, expected_output)

    def split_nested(self):
        text_node = TextNode(text='***`code`***', type=TextType.TEXT)
        expected_output = [TextNode(text='', type=TextType.BOLD),
                           TextNode(text='', type=TextType.ITALIC),
                           TextNode(text='code', type=TextType.CODE),
                           TextNode(text='', type=TextType.BOLD),
                           TextNode(text='', type=TextType.ITALIC)]
        split_code = split_nodes([text_node], '`', TextType.CODE)
        split_bold = split_nodes(split_code, '**', TextType.BOLD)
        split_italic = split_nodes(split_bold, '*', TextType.ITALIC)
        self.assertEqual(split_italic, expected_output)

