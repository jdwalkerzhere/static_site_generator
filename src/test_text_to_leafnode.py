import unittest

from textnode import TextType, TextNode
from htmlnode import LeafNode, text_node_to_html_node


class TestTextToLeafNode(unittest.TestCase):
    def test_text_node_conversion(self):
        text_node = TextNode(text="hi there", type=TextType.TEXT, url=None)
        leaf_node_from_text_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node_from_text_node, LeafNode(value="hi there"))

    def test_bold_italic_code_conversion(self):
        bold_node = TextNode(text="hi there", type=TextType.BOLD, url=None)
        bold_leaf = LeafNode(tag="b", value="hi there")
        self.assertEqual(text_node_to_html_node(bold_node), bold_leaf)

        italic_node = TextNode(text="bye there", type=TextType.ITALIC, url=None)
        italic_leaf = LeafNode(tag="i", value="bye there")
        self.assertEqual(text_node_to_html_node(italic_node), italic_leaf)

        code_node = TextNode(text="python3 main.py", type=TextType.CODE, url=None)
        code_leaf = LeafNode(tag="code", value="python3 main.py")
        self.assertEqual(text_node_to_html_node(code_node), code_leaf)

    def test_link_conversion(self):
        node = TextNode(
            text="go learn to code", type=TextType.LINK, url="https://boot.dev"
        )
        leaf = LeafNode(
            tag="a", value="go learn to code", props={"href": "https://boot.dev"}
        )
        self.assertEqual(text_node_to_html_node(node), leaf)

    def test_image_conversion(self):
        node = TextNode(text="I'm alt text!", type=TextType.IMG, url="https://boot.dev")
        leaf = LeafNode(
            tag="img",
            value="",
            props={"src": "https://boot.dev", "alt": "I'm alt text!"},
        )
        self.assertEqual(text_node_to_html_node(node), leaf)

    def test_non_equal_conversion(self):
        text_node = TextNode(text="hi there", type=TextType.TEXT, url=None)
        bold_leaf = LeafNode(tag="b", value="hi there")
        self.assertNotEqual(text_node_to_html_node(text_node), bold_leaf)
