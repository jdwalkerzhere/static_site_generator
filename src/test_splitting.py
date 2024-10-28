import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes


class TestTextSplitting(unittest.TestCase):
    def test_lanes_input(self):
        text_node = TextNode(text='This is text with a **bolded phrase** in the middle', type=TextType.TEXT)
        expected_output = [TextNode("This is text with a ", TextType.TEXT),
                           TextNode("bolded phrase", TextType.BOLD),
                           TextNode(" in the middle", TextType.TEXT)]
        self.assertEqual(split_nodes([text_node], '**', TextType.BOLD), expected_output)

    def test_split_expected(self):
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

    def test_split_nested(self):
        text_node = TextNode(text='***`code`***', type=TextType.TEXT)
        split_code = split_nodes([text_node], '`', TextType.CODE)
        self.assertRaises(ValueError, split_nodes, split_code, '**', TextType.BOLD)

    def test_more_than_one_segment(self):
        text_node = TextNode(text='*hi* my *name* is `jesse` and *I* really **want** to get **good** at `programming`', type=TextType.TEXT)
        expected_output = [TextNode(text='hi', type=TextType.ITALIC),
                           TextNode(text=' my ', type=TextType.TEXT),
                           TextNode(text='name', type=TextType.ITALIC),
                           TextNode(text=' is ', type=TextType.TEXT),
                           TextNode(text='jesse', type=TextType.CODE),
                           TextNode(text=' and ', type=TextType.TEXT),
                           TextNode(text='I', type=TextType.ITALIC),
                           TextNode(text=' really ', type=TextType.TEXT),
                           TextNode(text='want', type=TextType.BOLD),
                           TextNode(text=' to get ', type=TextType.TEXT),
                           TextNode(text='good', type=TextType.BOLD),
                           TextNode(text=' at ', type=TextType.TEXT),
                           TextNode(text='programming', type=TextType.CODE)]
        split_code = split_nodes([text_node], '`', TextType.CODE)
        split_bold = split_nodes(split_code, '**', TextType.BOLD)
        split_italic = split_nodes(split_bold, '*', TextType.ITALIC)
        self.assertEqual(split_italic, expected_output)
