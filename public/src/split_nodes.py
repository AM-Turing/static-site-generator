import re
from textnode import TextType, TextNode
from extract_links import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown Syntax")
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
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown):
    parts = re.split(r"\n{2,}", markdown)
    new_parts = []
    for part in parts:
        part = part.strip()
        if part != "":
            new_parts.append(part)
    return new_parts
