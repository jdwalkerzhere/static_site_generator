from typing import Any, Dict, List


class HTMLNode:
    def __init__(self,
                 tag = None,
                 value = None,
                 children = None,
                 props = None) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: List[HTMLNode] | None = children
        self.props: Dict[str, Any] | None = props

    def __eq__(self, value: object, /) -> bool:
        return all([lhs == rhs for lhs, rhs in zip(vars(self).items(), vars(value).items())])

    def __repr__(self) -> str:
        return f'HTMLNode(\n\ttag={self.tag}\n\tvalue={self.value}\n\tchildren={self.children}\n\tprops={self.props})'

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ''
        return ''.join([f' {k}="{v}"' for k, v in self.props.items()])
