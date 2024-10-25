import unittest

from htmlnode import HTMLNode, LeafNode


class TestLeafNode(unittest.TestCase):
    def test_invalid_has_children(self):
        node = LeafNode(
            tag="a",
            value="hi there",
            children=[HTMLNode()],
            props={"href": "https://boot.dev"},
        )
        self.assertRaises(ValueError, node.to_html)

    def test_invalid_no_value(self):
        node = LeafNode(tag="a", props={"href": "https://boot.dev"})
        self.assertRaises(ValueError, node.to_html)

    def test_valid_html_render(self):
        node = LeafNode(tag="a", value="hi there", props={"href": "https://boot.dev"})
        html_string = node.to_html()
        correct_string = '<a href="https://boot.dev">hi there</a>'
        self.assertEqual(html_string, correct_string)
