import re
import argparse
from shutil import rmtree, copy
from os import mkdir, listdir, makedirs
from os.path import exists, isfile, join, dirname
from markdown_blocks import markdown_to_html_node

__version__ = "1.0"  # Program version

parser = argparse.ArgumentParser(
    prog="Static Site Generator",
    description="Take markdown and convert to html.",
    epilog="Send it.",
)
parser.add_argument(
    "-b",
    "--basepath",
    help="Github Pages basepath, ex: github.io/REPO-NAME, REPO-NAME=basepath",
    required=True,
    type=str,
)
parser.add_argument("-V", "--version", action="version", version="%(prog)s 1.0")
args = parser.parse_args()


def main():
    dst = "docs/"
    static_src = "static/"
    markdown_src = "content/"
    rmtree(dst, ignore_errors=True)
    copy_from_src(static_src, dst)
    process_content(markdown_src, dst)


def process_content(markdown_src, dst):
    source = listdir(markdown_src)
    if not exists(dst):
        mkdir(dst)
    for item in source:
        old_dir = join(markdown_src, item)
        if item.endswith(".md"):
            html_item = item.replace(".md", ".html")
            new_path = join(dst, html_item)
            generate_page(old_dir, "template.html", new_path)
        else:
            new_dir = join(dst, item)
            if not exists(new_dir):
                mkdir(new_dir)
            process_content(old_dir, new_dir)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        header = re.findall("^#\s+(.*)$", line)
        if header:
            return header[0]
    raise ValueError("No title header detected in markdown.")


def copy_from_src(static_src, dst):
    source = listdir(static_src)
    if not exists(dst):
        mkdir(dst)
    for item in source:
        old_dir = join(static_src, item)
        if isfile(old_dir):
            copy(old_dir, dst)
        else:
            new_dir = join(dst, item)
            mkdir(new_dir)
            copy_from_src(old_dir, new_dir)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file1:
        markdown = file1.read()
    with open(template_path, "r") as file2:
        template = file2.read()
    title = extract_title(markdown)
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    basepath = args.basepath
    updated_html = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    dir_path = dirname(dest_path)
    if dir_path:
        makedirs(dir_path, exist_ok=True)
    with open(dest_path, "w") as file3:
        file3.write(updated_html)


if __name__ == "__main__":
    main()
