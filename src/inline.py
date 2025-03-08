from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # If the node is not plain text, add it to the new list as is
            new_list.append(node)
            continue

        # Split the text by the delimiter
        parts = node.text.split(delimiter)

        # Check for unmatched delimiters
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: unmatched delimiter '{delimiter}'")

        # Iterate through the split parts
        for i, part in enumerate(parts):
            if part == "":
                continue  # Skip empty parts
            if i % 2 == 0:
                # Even-indexed parts are plain text
                new_list.append(TextNode(part, TextType.TEXT))
            else:
                # Odd-indexed parts are wrapped in the delimiter
                new_list.append(TextNode(part, text_type))

    return new_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        matches = extract_markdown_images(old_node.text)
        if not matches:
            result.append(old_node)
            continue
            
        remaining_text = old_node.text
        for image_alt, image_url in matches:
            # Split at the image markdown
            parts = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            
            # Add the text before the image if it's not empty
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the image node
            result.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update remaining text
            remaining_text = parts[1]
        
        # Add any remaining text after the last image
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result

def split_nodes_link(old_nodes):
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        matches = extract_markdown_links(old_node.text)
        if not matches:
            result.append(old_node)
            continue
            
        remaining_text = old_node.text
        for link_text, link in matches:
            # Split at the link markdown
            parts = remaining_text.split(f"[{link_text}]({link})", 1)
            
            # Add the text before the link
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the image node
            result.append(TextNode(link_text, TextType.LINK, link))
            
            # Update remaining text
            remaining_text = parts[1]
        
        # Add any remaining text after the last image
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result

def text_to_textnodes(text):
    new_text = [TextNode(text, TextType.TEXT)]
    new_text = split_nodes_delimiter(new_text, "**", TextType.BOLD)
    new_text = split_nodes_delimiter(new_text, "`", TextType.CODE)
    new_text = split_nodes_delimiter(new_text, "_", TextType.ITALIC)
    new_text = split_nodes_image(new_text)
    new_text = split_nodes_link(new_text)
    return new_text
