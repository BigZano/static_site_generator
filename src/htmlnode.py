from textnode import TextNode, TextType



class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}


    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return " " + props_str + " "

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value

        attrs = "" if not self.props else self.props_to_html().rstrip()
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag=tag, value=None, children=children if children is not None else [], props=props)

    def to_html(self):
        attrs = "" if not self.props else self.props_to_html().rstrip()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{attrs}>{children_html}</{self.tag}>"
    

def text_node_to_html_node(TextNode):
    if TextNode.text_type == TextType.BOLD_TEXT:
        return LeafNode("strong", TextNode.text)
    elif TextNode.text_type == TextType.ITALIC_TEXT:
        return LeafNode("em", TextNode.text)
    elif TextNode.text_type == TextType.PLAIN_TEXT:
        return LeafNode(None, TextNode.text)
    elif TextNode.text_type == TextType.CODE_TEXT:
        return LeafNode("code", TextNode.text)
    elif TextNode.text_type == TextType.LINKS:
        if not TextNode.url:
            raise ValueError("Link text nodes must have a URL")
        return LeafNode("a", TextNode.text, props={"href": TextNode.url})
    elif TextNode.text_type == TextType.IMAGES:
        if not TextNode.url:
            raise ValueError("Image text nodes must have a URL")
        return LeafNode("img", None, props={"src": TextNode.url, "alt": TextNode.text})
    else:
        raise ValueError(f"Unknown text type: {TextNode.text_type}")
    