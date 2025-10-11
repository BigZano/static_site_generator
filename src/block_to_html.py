import re
from markdown_to_blocks import markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for tn in nodes:
        html_node = text_node_to_html_node(tn)
        if html_node is None:
            raise ValueError(f"Unexpected None from text_node_to_html_node for {tn}")
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        text = block.strip()
        if text.startswith("```") and text.endswith("```"):
            code_text = "\n".join(block.splitlines()[1:-1]) + "\n"
            children.append(ParentNode("pre", [ParentNode("code", [LeafNode(None, code_text)])]))
            continue
        elif text.startswith("###### "):
            children.append(ParentNode("h6", text_to_children(block[7:].strip())))
        elif text.startswith("##### "):
            children.append(ParentNode("h5", text_to_children(block[6:].strip())))
        elif text.startswith("#### "):
            children.append(ParentNode("h4", text_to_children(block[5:].strip())))
        elif text.startswith("### "):
            children.append(ParentNode("h3", text_to_children(block[4:].strip())))
        elif text.startswith("## "):
            children.append(ParentNode("h2", text_to_children(block[3:].strip())))
        elif text.startswith("# "):
            children.append(ParentNode("h1", text_to_children(block[2:].strip())))
        elif text.startswith("> "):
            quote_lines = []
            for l in block.splitlines():
                if l == ">":
                    continue
                if l.startswith("> "):
                    quote_lines.append(l[2:])
                else:
                    break
            cleaned = "\n".join(quote_lines).strip()
            if not cleaned:
                continue  # skip empty blockquote
            children.append(ParentNode("blockquote", text_to_children(cleaned)))
        elif all(l.strip() == "" or re.match(r"^\d+\.\s+", l) for l in block.splitlines()):
            items = []
            for line in block.splitlines():
                m = re.match(r"^(\d+)\.\s+(.*)", line.strip())
                if m:
                    items.append(ParentNode("li", text_to_children(m.group(2))))
            children.append(ParentNode("ol", items))
        elif all(l.strip() == "" or l.startswith("- ") for l in block.splitlines()):
            items = []
            for line in block.splitlines():
                if line.strip().startswith("- "):
                    items.append(ParentNode("li", text_to_children(line.strip()[2:])))
            children.append(ParentNode("ul", items))
        else:
            lines = [l.strip() for l in block.splitlines()]
            para_text = " ".join([l for l in lines if l])
            inlines = text_to_children(para_text)
            children.append(ParentNode("p", inlines))
    return ParentNode("div", children)
