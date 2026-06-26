from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str):
    split_text = markdown.split("\n\n")
    for i in range(len(split_text)):
        split_text[i] = split_text[i].strip()
    split_text = list(filter(None, split_text))
    return split_text

def block_to_block_type(block: str):
    first_char = block.split(" ", 1)[0]
    if len(first_char) <= 6:
        p = first_char
        if all(char == p[0] for char in p) == True and p[0] == "#":
            return BlockType.HEADING
    if block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    if first_char == ">" or first_char == "> ":
        split_block = block.split("\n")
        for line in split_block:
            if line[0] == ">":
                pass
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if first_char == "-":
        split_block = block.split("\n")
        for line in split_block:
            if line.startswith("- "):
                pass
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block[0].isdigit():
        split_block = block.split("\n")
        i = 1
        for line in split_block:
            if line.startswith(f"{i}. "):
                i += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH