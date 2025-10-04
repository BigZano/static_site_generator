from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADER = "header"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith("# "):
        return BlockType.HEADER
    elif block.startswith("## "):
        return BlockType.HEADER
    elif block.startswith("### "):
        return BlockType.HEADER
    elif block.startswith("#### "):
        return BlockType.HEADER
    elif block.startswith("##### "):
        return BlockType.HEADER
    elif block.startswith("###### "):
        return BlockType.HEADER
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith(". "):
        return BlockType.ORDERED_LIST
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH