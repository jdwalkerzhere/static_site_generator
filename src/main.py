from os import path, listdir, mkdir
from shutil import copy, rmtree

from htmlnode import md_to_html_doc


def mv_src_to_dest(src: str, dest: str, first_call: bool = True):
    if first_call:
        rmtree(dest)
        mkdir(dest)

    if path.isfile(src):
        copy(src, dest)
        return

    for content in listdir(src):
        if not path.isfile(content):  # is a directory
            mkdir(f"{dest}/{content}")
            mv_src_to_dest(f"{src}/{content}", f"{dest}/{content}", False)
            continue
        # file in pwd
        copy(content, dest)


def main():
    mv_src_to_dest(src="static", dest="public")


if __name__ == "__main__":
    main()
