import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_non_eq(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq_type(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This has a url", TextType.LINK, "https://boot.dev")
        self.assertIn(node.url, vars(node).values())


if __name__ == "__main__":
    unittest.main()
