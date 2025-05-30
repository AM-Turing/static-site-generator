import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid Markdown Syntax")
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        extracted_images = extract_markdown_images(old_node.text)
        if not extracted_images:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for alt_text, image_url in extracted_images:
            image_markdown = f"![{alt_text}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        extracted_links = extract_markdown_links(old_node.text)
        if not extracted_links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for alt_text, url in extracted_links:
            link_markdown = f"[{alt_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def detect_line_block_type(line):
    if line.strip().startswith("```"):
        return BlockType.CODE
    if re.match(r"^(#{1,6})\s+.+", line):
        return BlockType.HEADING
    if line.startswith(">"):
        return BlockType.QUOTE
    if re.match(r"^[-*]\s+.+", line):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\.\s+.+", line):
        return BlockType.ORDERED_LIST
    if line.strip() == "":
        return None
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block_lines = []
    current_block_type = None
    in_code_block = False

    i = 0
    while i < len(lines):
        line = lines[i]
        line_type = detect_line_block_type(line)

        if in_code_block:
            current_block_lines.append(line)
            if line.strip().startswith("```"):
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
                current_block_type = None
                in_code_block = False
            i += 1
            continue

        if line_type == BlockType.CODE:
            if current_block_lines:
                blocks.append("\n".join(current_block_lines).strip())
            current_block_lines = [line]
            current_block_type = BlockType.CODE
            in_code_block = True
            i += 1
            continue

        if line.strip() == "":
            next_line = lines[i + 1] if i + 1 < len(lines) else None
            if (
                current_block_type
                in {
                    BlockType.ORDERED_LIST,
                    BlockType.UNORDERED_LIST,
                    BlockType.QUOTE,
                }
                and next_line is not None
                and detect_line_block_type(next_line) == current_block_type
            ):
                current_block_lines.append("")
                i += 1
                continue

            if current_block_lines:
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
                current_block_type = None
            i += 1
            continue

        if current_block_type is None:
            current_block_lines = [line]
            current_block_type = line_type
        elif line_type == current_block_type:
            current_block_lines.append(line)
        else:
            blocks.append("\n".join(current_block_lines).strip())
            current_block_lines = [line]
            current_block_type = line_type

        i += 1

    if current_block_lines:
        blocks.append("\n".join(current_block_lines).strip())

    return blocks
