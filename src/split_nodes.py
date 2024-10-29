import re

from typing import List, Tuple
from textnode import TextNode, TextType


def split_nodes(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        # Since we're not allowing nested text styles
        if node.text_type != 'text':
            new_nodes.append(node)
            continue

        if not node.text:
            continue

        # Splitting up the text by the delimiter
        split_by_delim = [txt for txt in node.text.split(delimiter)]

        # If the length of the split is even it means we've encountered an odd number of delimeters: malformed markdown
        if len(split_by_delim) % 2 == 0:
            raise ValueError(f"No matching delimiter found for '{delimiter}'")

        for i in range(len(split_by_delim)):
            text = split_by_delim[i]

            # if the leading character was the delimeter, we'll get an empty text node
            if not text:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(text=text, type=TextType.TEXT))
                continue
            new_nodes.append(TextNode(text=text, type=text_type))

    return new_nodes


def extract_images(text: str) -> List[Tuple[str,str]]:
    return re.findall(pattern=r'!\[(.*?)\]\((.*?)\)', string=text)


def extract_links(text: str) -> List[Tuple[str,str]]:
    return re.findall(pattern=r'(?<!\!)\[(.*?)\]\((.*?)\)', string=text)


def split_images(nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for node in nodes:
        extracted_images = extract_images(node.text)[::-1]

        if not extracted_images:
            new_nodes.append(node)
            continue

        i, j = 0, 2

        start = 0

        while j < len(node.text):
            if node.text[i:j] == '![':
                if abs(start - i) != 0:
                    new_nodes.append(TextNode(text=node.text[start:i], type=TextType.TEXT))
                alt_text, url = extracted_images.pop()
                new_nodes.append(TextNode(text=alt_text, type=TextType.IMG, url=url))
                i += 5 + len(alt_text) + len(url)
                j = i + 2
                start = i
                continue
            i += 1
            j += 1

        if start < len(node.text):
            new_nodes.append(TextNode(text=node.text[start:], type=TextType.TEXT))

    return new_nodes


def split_links(nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for node in nodes:
        extracted_links = extract_links(node.text)[::-1]

        if not extracted_links or node.text_type != 'text':
            new_nodes.append(node)
            continue

        hyperlink, url = extracted_links.pop()

        str_link = f'[{hyperlink}]({url})'

        i = 0
        j = len(str_link)

        start = 0


        while j <= len(node.text):
            if node.text[i:j] == str_link:
                if abs(start - i) != 0:
                    new_nodes.append(TextNode(text=node.text[start:i], type=TextType.TEXT))
                new_nodes.append(TextNode(text=hyperlink, type=TextType.LINK, url=url))
                i += len(str_link) 
                start = i
                if not extracted_links:
                    break

                hyperlink, url = extracted_links.pop()
                str_link = f'[{hyperlink}]({url})'

                j = i + len(str_link)
                continue
            i += 1
            j += 1

        if start < len(node.text):
            new_nodes.append(TextNode(text=node.text[start:], type=TextType.TEXT))

    return new_nodes
