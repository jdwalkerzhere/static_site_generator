from typing import List
from textnode import TextNode, TextType


def split_nodes(old_nodes: List[TextNode],
                          delimiter: str,
                          text_type: TextType) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        new_nodes.extend([TextNode(text=text, type=text_type) for text in split_nodes])

    return new_nodes
    
