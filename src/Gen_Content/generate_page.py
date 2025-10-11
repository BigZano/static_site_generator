import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from block_to_html import markdown_to_html_node
from .extract_title_markdown import extract_title


def generate_page(from_path, template_path, to_path):
    print(f"Generating page from {from_path} to {to_path} using template {template_path}")
    md = _read_text(from_path)
    title = extract_title(md)
    html = markdown_to_html_node(md).to_html()
    tmpl = _read_text(template_path)
    page = tmpl.replace("{{ Title }}", title).replace("{{ Content }}", html)
    _write_text(to_path, page)


def _read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def _write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively crawl every entry in the content directory.
    For each markdown file found, generate a new .html file using the template.
    The generated pages are written to the public directory maintaining the same directory structure.
    """
    print(f"Scanning directory: {dir_path_content}")
    
    if os.path.isdir(dir_path_content):
        # Create corresponding directory in destination if it doesn't exist
        os.makedirs(dest_dir_path, exist_ok=True)
        
        # Process each item in the directory
        for entry in os.listdir(dir_path_content):
            entry_from = os.path.join(dir_path_content, entry)
            entry_to = os.path.join(dest_dir_path, entry)
            
            # Recursively process subdirectories and files
            generate_pages_recursive(entry_from, template_path, entry_to)
            
    elif dir_path_content.endswith(".md"):
        # Convert .md extension to .html for the output file
        html_output_path = dest_dir_path[:-3] + ".html" if dest_dir_path.endswith(".md") else dest_dir_path.replace(".md", ".html")
        generate_page(dir_path_content, template_path, html_output_path)
    else:
        print(f"Skipping non-markdown file: {dir_path_content}")