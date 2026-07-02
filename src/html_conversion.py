from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnodesplitter import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for t in textnodes:
        children.append(text_node_to_html_node(t))
    return children

def line_strip_to_children(block, block_type):
    lines = block.split("\n")
    new_lines = []
    if block_type == BlockType.PARAGRAPH:
        content = " ".join(line.strip() for line in lines)
        children = text_to_children(content)
        return ParentNode("p", children)
    if block_type == BlockType.HEADING:
        parts = lines[0].split(" ", 1)
        hash_num = len(parts[0])
        children = text_to_children(parts[1])
        return ParentNode(f"h{hash_num}", children)
    if block_type == BlockType.CODE:
        for l in lines:
            if not l.strip().startswith("```"):
                new_lines.append(l.strip())
        children = "\n".join(new_lines) + "\n"
        raw_text_node = TextNode(children, TextType.TEXT)
        children = text_node_to_html_node(raw_text_node)
        code_node = ParentNode("code", [children])
        return ParentNode("pre", [code_node])
    if block_type == BlockType.QUOTE:
        for l in lines:
            new_lines.append(l.strip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)
    if block_type == BlockType.UNORDERED_LIST:
        for l in lines:
            new_lines.append(l[2:])
        li_nodes = []
        for n in new_lines:
            line_children = text_to_children(n)
            li_nodes.append(ParentNode("li", line_children))
        return ParentNode("ul", li_nodes)
    if block_type == BlockType.ORDERED_LIST:
        for l in lines:
            new_lines.append(l.split('. ')[1])
        li_nodes = []
        for n in new_lines:
            line_children = text_to_children(n)
            li_nodes.append(ParentNode("li", line_children))
        return ParentNode("ol", li_nodes)
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for b in blocks:
        children_nodes.append(line_strip_to_children(b, block_to_block_type(b)))
    return ParentNode("div", children_nodes)