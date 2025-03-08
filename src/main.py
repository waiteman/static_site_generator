from textnode import *
from blocks import *
import os
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def copy_directory(src: str, dst: str):
    """
    Recursively copies all contents from the source directory to the destination directory.
    Deletes all contents of the destination directory before copying to ensure a clean copy.
    Logs the path of each file being copied.
    """
    # Ensure the source directory exists
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")

    # Delete all contents of the destination directory if it exists
    if os.path.exists(dst):
        logging.info(f"Deleting contents of destination directory: {dst}")
        shutil.rmtree(dst)

    # Create the destination directory
    os.makedirs(dst, exist_ok=True)
    logging.info(f"Created destination directory: {dst}")

    # Recursively copy all files and subdirectories
    for root, dirs, files in os.walk(src):
        # Compute the relative path from the source directory
        relative_path = os.path.relpath(root, src)
        # Compute the corresponding destination path
        dest_path = os.path.join(dst, relative_path)

        # Create subdirectories in the destination directory
        for dir_name in dirs:
            dest_dir = os.path.join(dest_path, dir_name)
            os.makedirs(dest_dir, exist_ok=True)
            logging.info(f"Created directory: {dest_dir}")

        # Copy files to the destination directory
        for file_name in files:
            src_file = os.path.join(root, file_name)
            dest_file = os.path.join(dest_path, file_name)
            shutil.copy2(src_file, dest_file)  # copy2 preserves metadata
            logging.info(f"Copied file: {src_file} -> {dest_file}")


def generate_page(from_path: str, template_path: str, dest_path: str):
    """
    Generates an HTML page from a markdown file using a template.
    Replaces {{ Title }} and {{ Content }} placeholders in the template with the title and HTML content.
    Writes the resulting HTML to the destination path.
    """
    # Print the generation message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as md_file:
        markdown = md_file.read()

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown)

    # Replace placeholders in the template
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    # Write the HTML to the destination file
    with open(dest_path, "w", encoding="utf-8") as html_file:
        html_file.write(full_html)

    print(f"Page successfully generated at {dest_path}")


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    """
    Recursively crawls the content directory, finds all markdown files, and generates HTML files
    in the public directory using the provided template. The directory structure is preserved.
    """
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)

    # Iterate over all entries in the content directory
    for entry in os.listdir(dir_path_content):
        # Construct full paths
        content_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(content_path):
            # If the entry is a directory, recursively process it
            generate_pages_recursive(content_path, template_path, dest_path)
        elif entry.endswith(".md"):
            # If the entry is a markdown file, generate the corresponding HTML file
            html_filename = os.path.splitext(entry)[0] + ".html"
            html_dest_path = os.path.join(dest_dir_path, html_filename)
            generate_page(content_path, template_path, html_dest_path)


if __name__ == "__main__":
    source_dir = "static"
    destination_dir = "public"
    copy_directory(source_dir, destination_dir)
    generate_pages_recursive("content", "template.html", "public")


