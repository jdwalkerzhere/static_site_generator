import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_invalid_no_tag(self):
        node = ParentNode(
            value="hi there",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode("code", "python3 main.py"),
            ],
            props={"href": "https://boot.dev"},
        )
        self.assertRaises(ValueError, node.to_html)

    def test_invalid_no_children(self):
        node = ParentNode(
            tag="div", value="hi there", props={"href": "https://boot.dev"}
        )
        self.assertRaises(ValueError, node.to_html)

    def test_valid_simple_to_html(self):
        node = ParentNode(
            tag="div",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode("code", "python3 main.py"),
            ],
            props={"href": "https://boot.dev"},
        )
        html_string = node.to_html()
        correct_string = '<div href="https://boot.dev"><b>Bold text</b>Normal text<i>Italic text</i><code>python3 main.py</code></div>'
        self.assertEqual(html_string, correct_string)
