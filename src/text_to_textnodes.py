from split_images_and_links import *
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    # images and links FIRST (before delimiters, to avoid processing underscores in URLs)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # bold next (both ** and __)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD_TEXT)
    # italic next (both * and _)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    # code last
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    return nodes
    



