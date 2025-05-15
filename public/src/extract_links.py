import re


def extract_markdown_images(text):
    check_bracket = re.findall(r"\[", text)
    if not check_bracket:
        raise ValueError("Missing Bracket in Alt Text: Invalid Markdown Format")

    check_parenthesis = re.findall(r"\(", text)
    if not check_parenthesis:
        raise ValueError("Missing Parenthesis in URL: Invalid Markdown Format")

    check_bracket_2 = re.findall(r"\]", text)
    if not check_bracket_2:
        raise ValueError("Missing Bracket in Alt Text: Invalid Markdown Format")

    check_parenthesis_2 = re.findall(r"\)", text)
    if not check_parenthesis_2:
        raise ValueError("Missing Parenthesis in URL: Invalid Markdown Format")

    pattern = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for alt, image_url in pattern:
        if not alt:
            raise ValueError(
                "Missing Alt Text in ![] (Ex: ![Alt Text]): Invalid markdown format"
            )
        if not image_url:
            raise ValueError(
                "Missing Image URL in () (Ex: www.example.com): Invalid markdown format"
            )
    return pattern


def extract_markdown_links(text):
    check_bracket = re.findall(r"\[", text)
    if not check_bracket:
        raise ValueError("Missing Bracket in Alt Text: Invalid Markdown Format")

    check_parenthesis = re.findall(r"\(", text)
    if not check_parenthesis:
        raise ValueError("Missing Parenthesis in Link URL: Invalid Markdown Format")

    check_bracket_2 = re.findall(r"\]", text)
    if not check_bracket_2:
        raise ValueError("Missing Bracket in Alt Text: Invalid Markdown Format")

    check_parenthesis_2 = re.findall(r"\)", text)
    if not check_parenthesis_2:
        raise ValueError("Missing Parenthesis in Link URL: Invalid Markdown Format")

    pattern = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    for alt, link_url in pattern:
        if not alt:
            raise ValueError(
                "Missing Alt Text in ![] (Ex: [Alt Text]): Invalid markdown format"
            )
        if not link_url:
            raise ValueError(
                "Missing Link URL in () (Ex: www.example.com): Invalid markdown format"
            )
    return pattern
