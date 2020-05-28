import re
from time import sleep

import arxiv
import click
import pyperclip
from jinja2 import Template


ARXIV_ID_REGEX = re.compile(r"https:\/\/arxiv.org/((abs)|(pdf))/(\d{3,5}\.\d{3,5})(\.pdf)?")


def get_template():
    with open("template.jinja") as file_:
        template = Template(file_.read())
    return template


def create_page_dict(arxiv_id, arxiv_url):
    if arxiv_id is None and arxiv_url is not None:
        arxiv_id = ARXIV_ID_REGEX.match(arxiv_url).groups()[3]
    response = arxiv.query(id_list=[str(arxiv_id)])
    arxiv_obj = response[0]
    page_dict = dict(
        url=f"https://arxiv.org/abs/{arxiv_id}",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        authors=arxiv_obj["authors"],
        published=arxiv_obj["published"][:7],
        abs=arxiv_obj["summary_detail"]["value"].replace("\n", " "),
        title=arxiv_obj["title"].replace("\n", " ").replace("  ", " ").replace("  ", " "),
    )
    return page_dict


def write_page(page_dict, template):
    page_output = template.render(**page_dict)
    with open(f"ignore/output/Paper: {page_dict['title']}.md", "w") as file_:
        file_.write(page_output)
    return page_output


@click.command()
@click.option("--arxiv_url", help="Arxiv url of the paper you want to create a page for")
@click.option("--arxiv_id", help="Arxiv Id of the paper you want to create a page for")
def main(arxiv_id, arxiv_url):
    """Simple Program to take an archive id and render the corresponding Roam page with data"""
    if arxiv_id is None and arxiv_url is None:
        clipboard_contents = pyperclip.paste()
        if ARXIV_ID_REGEX.match(clipboard_contents):
            arxiv_url = clipboard_contents
    page_dict = create_page_dict(arxiv_id, arxiv_url)
    template = get_template()
    page_output = write_page(page_dict, template)
    pyperclip.copy(page_output)
    sleep(0.1)
    pyperclip.copy(f"[[Paper: {page_dict['title']}]]")


if __name__ == "__main__":
    main()
