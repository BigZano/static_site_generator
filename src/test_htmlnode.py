import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from split_images_and_links import split_nodes_image
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter
from extract_markdown import extract_markdown_images, extract_markdown_links
from split_images_and_links import split_nodes_link, split_nodes_image

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello", [HTMLNode("span", "World")], {"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html(self):
        node = HTMLNode("div", props={"class": "my-class", "id": "my-id"})
        props_html = node.props_to_html()
        self.assertIn('class="my-class"', props_html)
        self.assertIn('id="my-id"', props_html)
        self.assertTrue(props_html.startswith(" "))
        self.assertTrue(props_html.endswith(" "))

    def test_neq_props_to_html(self):
        node = HTMLNode("div")
        props_html = node.props_to_html()
        self.assertEqual(props_html, "")

    def test_repr(self):
        node = HTMLNode("div", "Hello", [HTMLNode("span", "World")], {"class": "my-class"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Hello, children=[HTMLNode(tag=span, value=World, children=[], props={})], props={'class': 'my-class'})")

    def test_leaf_node_to_html(self):
        leaf = LeafNode("p", "This is a paragraph", props={"class": "text"})
        html = leaf.to_html()
        self.assertEqual(html, '<p class="text">This is a paragraph</p>')
    
    def test_leaf_node_no_tag(self):
        leaf = LeafNode(None, "Just text")
        html = leaf.to_html()
        self.assertEqual(html, "Just text")

    def test_leaf_node_no_value(self):
        leaf = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf.to_html()
    
    def test_parent_node_to_html(self):
        child1 = LeafNode("span", "Child 1")
        child2 = LeafNode("span", "Child 2", props={"class": "highlight"})
        parent = ParentNode("div", children=[child1, child2], props={"id": "container"})
        html = parent.to_html()
        self.assertEqual(html, '<div id="container"><span>Child 1</span><span class="highlight">Child 2</span></div>')

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold Text", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "strong")
        self.assertEqual(html_node.value, "Bold Text")

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic Text", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "em")
        self.assertEqual(html_node.value, "Italic Text")
    
    def test_text_node_to_html_node_plain(self):
        text_node = TextNode("Plain Text", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Plain Text")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code Text", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code Text")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Link Text", TextType.LINKS, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link Text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_link_no_url(self):
        text_node = TextNode("Link Text", TextType.LINKS)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)
    
    def test_split_code_simple(self):
        nodes = [TextNode("A `B` C", TextType.PLAIN_TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("A ", TextType.PLAIN_TEXT), ("B", TextType.CODE_TEXT), (" C", TextType.PLAIN_TEXT)]
        )

    def test_split_bold_simple(self):
        nodes = [TextNode("Hi **there** friend", TextType.PLAIN_TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("Hi ", TextType.PLAIN_TEXT), ("there", TextType.BOLD_TEXT), (" friend", TextType.PLAIN_TEXT)],
        )

    def test_non_plain_passthrough(self):
        nodes = [TextNode("x", TextType.BOLD_TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(out[0].text, "x")
        self.assertEqual(out[0].text_type, TextType.BOLD_TEXT)


    def test_unbalanced_raises(self):
        nodes = [TextNode("A `B C", TextType.PLAIN_TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)

    
    def test_skips_empty_parts(self):
        nodes = [TextNode("**bold**", TextType.PLAIN_TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("bold", TextType.BOLD_TEXT)],
        )


    def test_split_italic_simple(self):
        nodes = [TextNode("This is *italic* text", TextType.PLAIN_TEXT)]
        out = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("This is ", TextType.PLAIN_TEXT), ("italic", TextType.ITALIC_TEXT), (" text", TextType.PLAIN_TEXT)],
        )

    def test_split_multiple_delimiters(self):
        nodes = [TextNode("A `B` C `D` E", TextType.PLAIN_TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("A ", TextType.PLAIN_TEXT), ("B", TextType.CODE_TEXT), (" C ", TextType.PLAIN_TEXT), ("D", TextType.CODE_TEXT), (" E", TextType.PLAIN_TEXT)],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/image.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINKS, "https://example.com"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second link", TextType.LINKS, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with no links", TextType.PLAIN_TEXT)],
            new_nodes,
        )
    
    def test_split_images_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no images", TextType.PLAIN_TEXT)],
            new_nodes,
        )

    
    
if __name__ == "__main__":
    unittest.main()
    



