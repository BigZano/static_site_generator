import os
import re
from pathlib import Path

def _first_paragraph(markdown: str, max_len: int = 180) -> str:
    """Extract first non-heading paragraph for meta description"""
    for line in markdown.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith(("#", "!", "-", "*", ">", "[")):
            continue
        s = re.sub(r"\s+", " ", s)
        return (s[:max_len] + "…") if len(s) > max_len else s
    return "Professional resume and portfolio"

def _to_canonical(base_url: str, dest_path: str) -> str:
    """Generate canonical URL from destination path"""
    p = Path(dest_path)
    try:
        rel = p.relative_to("docs")
    except Exception:
        rel = p
    url_path = "/" if rel.as_posix() in ("", ".") else "/" + rel.as_posix()
    if url_path.endswith("/index.html"):
        url_path = url_path[: -len("index.html")]
    if not base_url.endswith("/"):
        base_url += "/"
    return (base_url.rstrip("/") + url_path).replace("//", "/")

def _render_markdown(markdown: str) -> str:
    """Convert markdown to HTML using existing pipeline"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from block_to_html import markdown_to_html_node
    
    return markdown_to_html_node(markdown).to_html()

def generate_page(from_path, template_path, dest_path):
    """Generate a single HTML page from markdown"""
    print(f"Generating page from {from_path} to {dest_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from Gen_Content.extract_title_markdown import extract_title
    title = extract_title(markdown)

    description = _first_paragraph(markdown)
    base_url = "/"
    canonical = _to_canonical(base_url, dest_path)

    content_html = _render_markdown(markdown)

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    page_html = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", content_html)
        .replace("{{ Description }}", description)
        .replace("{{ Canonical }}", canonical)
        .replace("{{ BaseUrl }}", base_url)
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_html)
    
    print(f"Page written to {dest_path}")