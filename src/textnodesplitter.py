from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("Missing second delimiter")
        for i, s in enumerate(split_node):
            if s == "":
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(s, text_type))
            else:
                new_nodes.append(TextNode(s, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = extract_markdown_images(node.text)
        if len(split_node) == 0:
            new_nodes.append(node)
            continue
        current_text = node.text
        for alt, url in split_node:
            text_split = current_text.split(f"![{alt}]({url})", 1)
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = text_split[1]
        if current_text == "":
            continue
        else:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = extract_markdown_links(node.text)
        if len(split_node) == 0:
            new_nodes.append(node)
            continue
        current_text = node.text
        for link_text, url in split_node:
            text_split = current_text.split(f"[{link_text}]({url})", 1)
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            current_text = text_split[1]
        if current_text == "":
            continue
        else:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = []
    bold_nodes = (split_nodes_delimiter(old_nodes, "**", TextType.BOLD))
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_split = split_nodes_image(new_nodes)
    return split_nodes_link(image_split)