from typing import Any, Dict, List

from md_to_blocks import markdown_to_blocks, block_to_block_type, block_spec
from split_nodes import split_nodes, splitter
from textnode import TextType, TextNode


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: List[HTMLNode] | None = children
        self.props: Dict[str, Any] | None = props

    def __eq__(self, value: object, /) -> bool:
        return all(
            [lhs == rhs for lhs, rhs in zip(vars(self).items(), vars(value).items())]
        )

    def __repr__(self) -> str:
        return f"HTMLNode(\n\ttag={self.tag}\n\tvalue={self.value}\n\tchildren={self.children}\n\tprops={self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join([f' {k}="{v}"' for k, v in self.props.items()])


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf Nodes must contain a value")
        if self.children:
            raise ValueError("Leaf Nodes cannot have children")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        super().__init__(tag, value, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Parent Nodes must have a tag")
        if not self.children:
            raise ValueError("Parent Nodes must have children")
        children = [child.to_html() for child in self.children]
        return f"<{self.tag}{self.props_to_html()}>{''.join(children)}</{self.tag}>"


def text_node_to_html_node(textnode: TextNode) -> LeafNode:
    match textnode.text_type:
        case "text":
            return LeafNode(value=textnode.text)
        case "bold":
            return LeafNode(tag="b", value=textnode.text)
        case "italic":
            return LeafNode(tag="i", value=textnode.text)
        case "code":
            return LeafNode(tag="code", value=textnode.text)
        case "link":
            return LeafNode(tag="a", value=textnode.text, props={"href": textnode.url})
        case "img":
            return LeafNode(
                tag="img", value="", props={"src": textnode.url, "alt": textnode.text}
            )
        case _:
            raise ValueError(f"Non-implemented TextNode Type: {textnode.text_type}")


def md_to_html_doc(markdown: str) -> ParentNode:
    root_node = ParentNode(tag="div", children=[])
    blocked_md = markdown_to_blocks(markdown)

    for block in blocked_md:
        if not block:
            continue

        block_type = block_to_block_type(block)
        match block_type:
            case "HEADING":
                # Gathering number of #'s for proper <h> tag count
                h_count = block.index("# ") + 1
                textnode = TextNode(text=block.lstrip("# "), type=TextType.TEXT)
                split_text = splitter(textnode)
                child_nodes = [text_node_to_html_node(t) for t in split_text]
                header = ParentNode(tag=f"h{h_count}", children=child_nodes)
                root_node.children.append(header)

            case "CODE":
                textnode = TextNode(text=block.strip("```"), type=TextType.CODE)
                leafnode = text_node_to_html_node(textnode)
                code_block = ParentNode(tag="pre", children=[leafnode])
                root_node.children.append(code_block)

            case "QUOTE":
                text = "\n".join(l.lstrip('> ') for l in block.split('\n'))
                quote_node = LeafNode(tag='blockquote', value=text)
                root_node.children.append(quote_node)
            case "UNORDERED_LIST":
                text_nodes = [
                    TextNode(text=l[l.index(' ')+1:], type=TextType.TEXT)
                    for l in block.split("\n")
                ]
                children = []
                for node in text_nodes:
                    split_node = splitter(node)
                    joined = "".join(text_node_to_html_node(n).to_html() for n in split_node)
                    leaf = LeafNode(tag='li', value=joined)
                    children.append(leaf)

                list_parent = ParentNode(tag="ul", children=children)
                root_node.children.append(list_parent)

            case "ORDERED_LIST":
                text_nodes = [
                    TextNode(text=l[l.index(" ") + 1 :], type=TextType.TEXT)
                    for l in block.split("\n")
                ]

                children = []
                for node in text_nodes:
                    split_node = splitter(node)
                    joined = "".join(text_node_to_html_node(n).to_html() for n in split_node)
                    leaf = LeafNode(tag='li', value=joined)
                    children.append(leaf)

                list_parent = ParentNode(tag="ol", children=children)
                root_node.children.append(list_parent)

            case "PARAGRAPH":
                split_nodes = splitter(TextNode(text=block, type=TextType.TEXT))
                leaves = [text_node_to_html_node(node) for node in split_nodes]
                paragraph = ParentNode(tag="p", children=leaves)
                root_node.children.append(paragraph)

            case _:
                raise ValueError(f"Unexpected block type: {block_type}")

    return root_node
