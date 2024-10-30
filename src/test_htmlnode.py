import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_node_creation(self):
        node = HTMLNode()
        self.assertIsNotNone(node)
        self.assertEqual(node, HTMLNode(tag=None, value=None, children=[], props=None))

    def test_normal_node_creation(self):
        node = HTMLNode(
            tag="a",
            value="I'm an <a> tag",
            children=[],
            props={"href": "https://boots.dev", "target": "_blank"},
        )
        self.assertIsNotNone(node)
        self.assertEqual(
            node.props_to_html(), ' href="https://boots.dev" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(tag="a", value="Im an <a> tag")
        text = (
            f"HTMLNode(\n\ttag=a\n\tvalue=Im an <a> tag\n\tchildren=[]\n\tprops=None)"
        )
        self.assertEqual(node.__repr__(), text)
