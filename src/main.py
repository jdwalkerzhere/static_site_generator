from os import path, mkdir, scandir
from shutil import copy, rmtree

from htmlnode import md_to_html_doc, ParentNode


def mv_src_to_dest(src: str, dest: str, first_call: bool = True):
    if first_call:
        rmtree(dest)
        mkdir(dest)

    for content in scandir(src):
        if not path.isfile(content):  # is a directory
            new_path = f'{dest}/{content.name}'
            mkdir(new_path)
            mv_src_to_dest(content.path, new_path, False)
            continue
        # file in pwd
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
    with open(from_path, 'r') as md_file:
        md_contents = md_file.read()
        md_contents = md_to_html_doc(md_contents).to_html()

    with open(template_path, 'r') as template:
        template_content = template.read()

    template_content = template_content.replace('{{ Title }}', html_file_title)
    template_content = template_content.replace('{{ Content }}', md_contents)

    with open(dest_path, 'w') as generated_html:
        generated_html.write(template_content)


def generate_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for content in scandir(dir_path_content):
        if not path.isfile(content):
            new_path = f'{dest_dir_path}/{content.name}'
            mkdir(new_path)
            generate_recursive(content.path, template_path, new_path)
            continue
        generate_page(content.path, template_path, f'{dest_dir_path}/index.html')


def main():
    mv_src_to_dest(src="static", dest="public")
    generate_recursive('src/content', 'src/template.html', 'public')


if __name__ == "__main__":
    main()
