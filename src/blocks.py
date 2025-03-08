from enum import Enum
from htmlnode import *
from textnode import *
from inline import *

def markdown_to_blocks(markdown):
    blocks = []
    current_block = []
    in_code_block = False

    for line in markdown.splitlines():
        if line.startswith("```"):
            in_code_block = not in_code_block
            current_block.append(line)
            if not in_code_block:
                blocks.append("\n".join(current_block))
                current_block = []
        elif in_code_block:
            current_block.append(line)
        elif line.strip() == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    lines = block.splitlines()
    if block[0] == "#":
        return BlockType.HEADING
    
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    
    first_chars = ""
    for line in lines:
        first_chars = first_chars + line[0]
    if first_chars == ">" * len(first_chars):
        return BlockType.QUOTE
    
    second_chars = ""
    # Check for unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    

def is_ordered_list(markup_block):
    lines = markup_block.strip().splitlines()
    expected_number = 1

    for line in lines:
        # Split the line into the number part and the rest
        parts = line.strip().split('.', 1)
        
        # Check if the line starts with a number followed by '.' and a space
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].startswith(' '):
            return False
        
        # Check if the number is the expected one
        if int(parts[0]) != expected_number:
            return False
        
        # Increment the expected number for the next line
        expected_number += 1

    return True

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.text_node_to_html_node()
        children.append(html_node)
    return children

def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        block = block.replace("\n", " ")
        children = text_to_children(block)
        return ParentNode("p", children)
    elif block_type == BlockType.HEADING:
        level = block.count("#")
        text = block.lstrip("#").lstrip()
        children = text_to_children(text)
        return ParentNode(f"h{level}", children)
    elif block_type == BlockType.CODE:
        # Remove the triple backticks and preserve newlines
        code_content = block[3:-3]  # Remove the first and last 3 characters (backticks)
        # Ensure the content starts and ends cleanly
        if code_content == "\n":
            code_content = "\n"  # Preserve the single newline
        else:
            code_content = code_content.lstrip("\n")  # Remove leading newline
        return ParentNode("pre", [LeafNode("code", code_content)])
    elif block_type == BlockType.QUOTE:
        lines = block.splitlines()
        stripped_lines = [line.lstrip(">").lstrip() for line in lines]
        quote_text = "\n".join(stripped_lines)
        children = text_to_children(quote_text)
        return ParentNode("blockquote", children)
    elif block_type == BlockType.UNORDERED_LIST:
        items = block.splitlines()
        list_items = []
        for item in items:
            item_text = item.lstrip("-").lstrip()
            children = text_to_children(item_text)
            list_items.append(ParentNode("li", children))
        return ParentNode("ul", list_items)
    elif block_type == BlockType.ORDERED_LIST:
        items = block.splitlines()
        list_items = []
        for item in items:
            item_text = item.split(".", 1)[1].lstrip()
            children = text_to_children(item_text)
            list_items.append(ParentNode("li", children))
        return ParentNode("ol", list_items)
    else:
        raise ValueError(f"Invalid block type: {block_type}")
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)
    return ParentNode("div", children)

def extract_title(markdown: str) -> str:
    """
    Extracts the title from the markdown content.
    The title is the first line that starts with a single # (H1 header).
    If no H1 header is found, raises an exception.
    """
    for line in markdown.splitlines():
        if line.startswith("# "):
            # Extract the title text after the #
            title = line.lstrip("#").strip()
            return title

    # If no H1 header is found, raise an exception
    raise ValueError("No H1 header found in the markdown content.")