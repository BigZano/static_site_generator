from textnode import TextNode, TextType


def main():
    node = TextNode(text_type=TextType.BOLD_TEXT, text="Hello, World!", url=None)

    print(node)

if __name__ == "__main__":
    main()