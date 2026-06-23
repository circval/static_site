def markdown_to_blocks(markdown: str):
    split_text = markdown.split("\n\n")
    for i in range(len(split_text)):
        split_text[i] = split_text[i].strip()
    split_text = list(filter(None, split_text))
    return split_text