from typing import List
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
