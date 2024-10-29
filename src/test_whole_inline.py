import unittest

from textnode import TextNode, TextType
from split_nodes import split_images, split_links, split_nodes


class TestWholeInlinePipe(unittest.TestCase):
    def test_whole_inline_pipe(self):
        markdown_doc = [TextNode(text='# I am a header no special treatment', type=TextType.TEXT),
                        TextNode(text='[i am a link](i should get split) and ![i am an image](split me)', type=TextType.TEXT),
                        TextNode(text='and *i* **am** `special text` that [should](get) ![split](up)', type=TextType.TEXT)]

        images_split = split_images(markdown_doc)
        expected_images = [TextNode(text='# I am a header no special treatment', type=TextType.TEXT),
                           TextNode(text='[i am a link](i should get split) and ', type=TextType.TEXT),
                           TextNode(text='i am an image', type=TextType.IMG, url='split me'),
                           TextNode(text='and *i* **am** `special text` that [should](get) ', type=TextType.TEXT),
                           TextNode(text='split', type=TextType.IMG, url='up')]
        self.assertEqual(images_split, expected_images)

        link_split = split_links(images_split)
        expected_links = [TextNode(text='# I am a header no special treatment', type=TextType.TEXT),
                          TextNode(text='i am a link', type=TextType.LINK, url='i should get split'),
                          TextNode(text=' and ', type=TextType.TEXT),
                          TextNode(text='i am an image', type=TextType.IMG, url='split me'),
                          TextNode(text='and *i* **am** `special text` that ', type=TextType.TEXT),
                          TextNode(text='should', type=TextType.LINK, url='get'),
                          TextNode(text=' ', type=TextType.TEXT),
                          TextNode(text='split', type=TextType.IMG, url='up')]
        self.assertEqual(link_split, expected_links)

        bold_split = split_nodes(link_split, '**', TextType.BOLD)
        expected_bolds = [TextNode(text='# I am a header no special treatment', type=TextType.TEXT),
                          TextNode(text='i am a link', type=TextType.LINK, url='i should get split'),
                          TextNode(text=' and ', type=TextType.TEXT),
                          TextNode(text='i am an image', type=TextType.IMG, url='split me'),
                          TextNode(text='and *i* ', type=TextType.TEXT),
                          TextNode(text='am', type=TextType.BOLD),
                          TextNode(text=' `special text` that ', type=TextType.TEXT),
                          TextNode(text='should', type=TextType.LINK, url='get'),
                          TextNode(text=' ', type=TextType.TEXT),
                          TextNode(text='split', type=TextType.IMG, url='up')]
        self.assertEqual(bold_split, expected_bolds)

        italic_split = split_nodes(bold_split, '*', TextType.ITALIC)
        expected_italics = [TextNode(text='# I am a header no special treatment', type=TextType.TEXT),
                            TextNode(text='i am a link', type=TextType.LINK, url='i should get split'),
                            TextNode(text=' and ', type=TextType.TEXT),
                            TextNode(text='i am an image', type=TextType.IMG, url='split me'),
                            TextNode(text='and ', type=TextType.TEXT),
                            TextNode(text='i', type=TextType.ITALIC),
                            TextNode(text=' ', type=TextType.TEXT),
                            TextNode(text='am', type=TextType.BOLD),
                            TextNode(text=' `special text` that ', type=TextType.TEXT),
                            TextNode(text='should', type=TextType.LINK, url='get'),
                            TextNode(text=' ', type=TextType.TEXT),
                            TextNode(text='split', type=TextType.IMG, url='up')]
        self.assertEqual(italic_split, expected_italics)

        code_split = split_nodes(italic_split, '`', TextType.CODE)
        expected_output = [TextNode(text='# I am a header no special treatment', type=TextType.TEXT),
                           TextNode(text='i am a link', type=TextType.LINK, url='i should get split'),
                           TextNode(text=' and ', type=TextType.TEXT),
                           TextNode(text='i am an image', type=TextType.IMG, url='split me'),
                           TextNode(text='and ', type=TextType.TEXT),
                           TextNode(text='i', type=TextType.ITALIC),
                           TextNode(text=' ', type=TextType.TEXT),
                           TextNode(text='am', type=TextType.BOLD),
                           TextNode(text=' ', type=TextType.TEXT),
                           TextNode(text='special text', type=TextType.CODE),
                           TextNode(text=' that ', type=TextType.TEXT),
                           TextNode(text='should', type=TextType.LINK, url='get'),
                           TextNode(text=' ', type=TextType.TEXT),
                           TextNode(text='split', type=TextType.IMG, url='up')]
        self.assertEqual(code_split, expected_output)
