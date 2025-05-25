import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown):
    markdown_split = markdown.split("\n")
    if (
        markdown_split[0].startswith("```")
        and markdown_split[-1].strip().startswith("```")
        and len(markdown_split) >= 2
    ):
        return BlockType.CODE
    if len(markdown_split) == 1 and re.match(r"^(#{1,6})\s+.+$", markdown_split[0]):
        return BlockType.HEADING
    if all(line.startswith(">") for line in markdown_split):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in markdown_split):
        return BlockType.UNORDERED_LIST
    for i, line in enumerate(markdown_split, 1):
        if not re.match(rf"^{i}\. .+", line):
            break
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
