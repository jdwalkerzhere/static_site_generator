from htmlnode import md_to_html_doc


def main():
    with open("./content/test_md.md", "r") as md_file:
        html_string = md_to_html_doc(md_file.read())
        print(html_string)


if __name__ == "__main__":
    main()
