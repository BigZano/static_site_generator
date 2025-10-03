from split_images_and_links import *
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter



def text_to_textnodes(text):
    # Start with a single plain text node
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    
    # Apply all splitting functions in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
    



