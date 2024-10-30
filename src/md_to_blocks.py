import re

from typing import List

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = []

    curr_block = []
    for line in markdown.split('\n'):
        line = line.strip()
        if not line:
            blocks.append('\n'.join(curr_block))
            curr_block = []
            continue
        curr_block.append(line)

    return blocks

block_spec = [
    ('HEADING', r'^#{1,6} .*?'),
    ('CODE', r'^```[\s\S]*?```'),
    ('QUOTE', r'^> .*(?:\n> .*)*\n'),
    ('UNORDERED_LIST', r'^(?:[*|-] .*\n)+'),
    ('ORDERED_LIST', r'^(?:\d+\. .*\n)+')
]

def block_to_block_type(block: str) -> str | None:
    block_regex = '|'.join('(?P<%s>%s)' % pair for pair in block_spec)
    regex_match = re.match(block_regex, block, re.DOTALL)
    if not regex_match:
        return 'PARAGRAPH'
    return regex_match.lastgroup
