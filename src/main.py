from textnode import TextNode, TextType


def main():
    bold = TextNode('hi there', TextType.BOLD)
    link = TextNode('click here', TextType.LINK, 'https://boot.dev')
    italic = TextNode('important', TextType.ITALIC)
    italic_copy = TextNode('important', TextType.ITALIC) 
    italic_diff = TextNode('not important', TextType.ITALIC)

    print(bold)
    print(link)
    print(italic)
    print(italic == italic_copy)
    print(italic != italic_diff)


if __name__ == '__main__':
    main()
