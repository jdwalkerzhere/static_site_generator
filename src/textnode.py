from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "img"


class TextNode:
    def __init__(self, text: str, type: TextType, url=None) -> None:
        self.text = text
        self.text_type = type.value
        self.url = url

    def __eq__(self, other: object, /) -> bool:
        # Get the attributes for comparision
        self_attrs, other_attrs = vars(self), vars(other)

        return all(
            [lhs == rhs for lhs, rhs in zip(self_attrs.items(), other_attrs.items())]
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
