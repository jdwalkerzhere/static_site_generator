from typing import Any, Dict, List

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

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Nodes must have a tag")
        if not self.children:
            raise ValueError("Parent Nodes must have children")
        if not self.tag:
            return self.value
        children = [child.to_html() for child in self.children]
        return f"<{self.tag}{self.props_to_html()}>{self.value}{''.join(children)}</{self.tag}>"


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
