from os import path, listdir, mkdir, scandir
from shutil import copy, rmtree

from htmlnode import md_to_html_doc


def mv_src_to_dest(src: str, dest: str, first_call: bool = True):
    print(f'src: {src}')
    print(f'dest: {dest}')
    print(f'first_call: {first_call}')
    if first_call:
        rmtree(dest)
        mkdir(dest)

    for content in scandir(src):
        print(f'looking at {content}')
        if not path.isfile(content):  # is a directory
            print(f'{content} is a directory, making equivalent at {dest}')
            mkdir(f"{dest}/{content.name}")
            print(f'calling recursively on {src}/{content}')
            mv_src_to_dest(content.path, f'{dest}/{content.name}', False)
            continue
        # file in pwd
        print(f'{content} is a file, copying to {dest}')
        copy(content.path, dest)


def extract_title(path: str):
    with open(path, 'r') as file:
        lines = (line for line in file.readlines())

        curr_line = next(lines)

        while not curr_line.startswith('# '):
            curr_line = next(lines)

        return curr_line.lstrip('# ')


def generate_page(from_path: str, template_path: str, dest_path: str):
    html_file_title = extract_title(from_path).strip()
    print(html_file_title)
    content = None
    with open(from_path, 'r') as md_file:
        print(f'Generating page from {from_path} to {dest_path} using {template_path}')
        md_contents = md_file.read()
        content = md_to_html_doc(md_contents).strip()

    print(f'content: {content}')
    template_content = None
    with open(template_path, 'r') as template:
        template_content = template.read()

    print(template_content)
    template_content = template_content.replace('{{ Title }}', html_file_title)
    template_content = template_content.replace('{{ Content }}', content)
    print(template_content)

    with open(dest_path, 'w') as generated_html:
        generated_html.write(template_content)


def main():
    mv_src_to_dest(src="static", dest="public")
    generate_page(from_path='src/content/index.md', template_path='src/template.html', dest_path='public/index.html')


if __name__ == "__main__":
    main()
