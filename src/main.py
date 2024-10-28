from textnode import TextNode, TextType

from lexer import MarkdownDocument


def main():
    with open("./content/test_md.md", "r") as md_file:
        md_file = MarkdownDocument(md_file.read())
        print(md_file.content)


if __name__ == "__main__":
    main()
