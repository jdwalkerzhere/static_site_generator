from typing import List


def markdown_to_blocks(markdown) -> List[str]:
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
