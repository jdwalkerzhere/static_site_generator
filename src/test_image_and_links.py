import unittest

from split_nodes import extract_images, extract_links, split_images, split_links
from textnode import TextType, TextNode


class TestImagesAndLinks(unittest.TestCase):
    def test_image_extraction(self):
        text = "hi you should look at this ![some alt text](https://boot.dev) and then this [not an image](https://boot.dev)"
        extracted = extract_images(text)
        expected_output = [("some alt text", "https://boot.dev")]
        self.assertEqual(extracted, expected_output)

    def test_link_extraction(self):
        text = "hi you should look at this ![some alt text](https://boot.dev) and then this [not an image](https://boot.dev)"
        extracted = extract_links(text)
        expected_output = [("not an image", "https://boot.dev")]
        self.assertEqual(extracted, expected_output)

    def test_multiple_images(self):
        text = "[I am a link](fake.url) but ![I am an image!](https://boot.dev) and ![I am too!](https://boot.dev)"
        extracted = extract_images(text)
        expected_output = [
            ("I am an image!", "https://boot.dev"),
            ("I am too!", "https://boot.dev"),
        ]
        self.assertEqual(extracted, expected_output)

    def test_multiple_links(self):
        text = "[i am a link](to somewhere) but ![i am an image](look at me) and [i am another link](to elsewhere)"
        extracted = extract_links(text)
        expected_output = [
            ("i am a link", "to somewhere"),
            ("i am another link", "to elsewhere"),
        ]
        self.assertEqual(extracted, expected_output)

    def test_starting_image(self):
        text = "![just an image](https://boot.dev)"
        extracted = extract_images(text)
        expected_output = [("just an image", "https://boot.dev")]
        self.assertEqual(extracted, expected_output)

    def test_split_image_from_textnode(self):
        textnode = TextNode(
            text="hi i show an image ![of birb](https://boot.dev) and [i am link](https://boot.dev)",
            type=TextType.TEXT,
        )
        images_split = split_images([textnode])
        expected_output = [
            TextNode(text="hi i show an image ", type=TextType.TEXT),
            TextNode(text="of birb", type=TextType.IMG, url="https://boot.dev"),
            TextNode(text=" and [i am link](https://boot.dev)", type=TextType.TEXT),
        ]
        self.assertEqual(images_split, expected_output)

    def test_split_multi_image_textnode(self):
        textnode = TextNode(
            text="![i am image](hearme.roar)![me too](rawn.xd)", type=TextType.TEXT
        )
        images_split = split_images([textnode])
        expected_output = [
            TextNode(text="i am image", type=TextType.IMG, url="hearme.roar"),
            TextNode(text="me too", type=TextType.IMG, url="rawn.xd"),
        ]
        self.assertEqual(images_split, expected_output)

    def test_split_link_from_textnode(self):
        textnode = TextNode(
            text="hi i show an image ![of birb](https://boot.dev) and [i am link](https://boot.dev)",
            type=TextType.TEXT,
        )
        link_split = split_links([textnode])
        expected_output = [
            TextNode(
                text="hi i show an image ![of birb](https://boot.dev) and ",
                type=TextType.TEXT,
            ),
            TextNode(text="i am link", type=TextType.LINK, url="https://boot.dev"),
        ]
        self.assertEqual(link_split, expected_output)

    def test_split_multi_link_textnode(self):
        textnode = TextNode(
            text="[i am link](rawr) and ![i am image](grr) and [i am other link](tee hee)",
            type=TextType.TEXT,
        )
        link_split = split_links([textnode])
        expected_output = [
            TextNode(text="i am link", type=TextType.LINK, url="rawr"),
            TextNode(text=" and ![i am image](grr) and ", type=TextType.TEXT),
            TextNode(text="i am other link", type=TextType.LINK, url="tee hee"),
        ]
        self.assertEqual(link_split, expected_output)
