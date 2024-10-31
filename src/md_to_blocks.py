import re

from typing import List


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = []

    curr_block = []
    code_block = False
    for line in markdown.split("\n"):
        line = line.strip()

        if code_block and line.endswith("```"):
            curr_block.append(line)
            blocks.append("\n".join(curr_block))
            curr_block = []
            code_block = False
            continue

        if not line and not code_block:
            blocks.append("\n".join(curr_block))
            curr_block = []
            continue

        if line.startswith("```"):
            code_block = True
        curr_block.append(line)

    return blocks


block_spec = [
    ("HEADING", r"^#{1,6} .*?"),
    ("CODE", r"^```[\s\S]*?```"),
    ("QUOTE", r"^> .*(?:\n> .*)*\n"),
    ("UNORDERED_LIST", r"^(?:[*|-] .*\n)+"),
    ("ORDERED_LIST", r"^(?:\d+\. .*\n)+"),
]


def block_to_block_type(block: str) -> str | None:
    block_regex = "|".join("(?P<%s>%s)" % pair for pair in block_spec)
    regex_match = re.match(block_regex, block, re.DOTALL)
    if not regex_match:
        return "PARAGRAPH"
    return regex_match.lastgroup
