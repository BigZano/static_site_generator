from markdown_to_blocks import markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
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
            cleaned = "\n".join(l[2:] if l.startswith("> ") else l for l in block.splitlines())
            children.append(ParentNode("blockquote", text_to_children(cleaned)))
        elif text.startswith("- "):
            items = []
            for line in block.splitlines():
                if line.startswith("- "):
                    items.append(ParentNode("li", text_to_children(line[2:].strip())))
            children.append(ParentNode("ul", items))
        # python
        else:
            lines = [l.strip() for l in block.splitlines()]
            para_text = " ".join([l for l in lines if l])
            inlines = text_to_children(para_text)
            # remap strong/em -> b/i for paragraph expectations
            for ch in inlines:
                if getattr(ch, "tag", None) == "strong":
                    ch.tag = "b"
                elif getattr(ch, "tag", None) == "em":
                    ch.tag = "i"
            children.append(ParentNode("p", inlines))
    return ParentNode("div", children)