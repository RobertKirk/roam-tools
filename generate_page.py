import re
from datetime import datetime
import openreview
from time import sleep

import arxiv
import click
import pyperclip
from jinja2 import Template


ARXIV_ID_REGEX = re.compile(r"https:\/\/(ar5iv\.labs\.)?arxiv.org\/((abs)|(pdf)|(html))\/(\d{3,5}\.\d{3,5})(\.pdf)?")

OPENREVIEW_ID_REGEX = re.compile(r"https:\/\/openreview.net/((forum)|(pdf))\?id\=(\w*)")


def get_template():
    with open("template.jinja") as file_:
        template = Template(file_.read())
    return template


def arxiv_create_page_dict(arxiv_id, arxiv_url):
    if arxiv_id is None and arxiv_url is not None:
        arxiv_id = ARXIV_ID_REGEX.match(arxiv_url).groups()[5]
    response = arxiv.query(id_list=[str(arxiv_id)])
    arxiv_obj = response[0]
    page_dict = dict(
        url=f"https://arxiv.org/abs/{arxiv_id}",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        authors=arxiv_obj["authors"],
        published_year=arxiv_obj["published"][:4],
        published_month=arxiv_obj["published"][5:7],
        abs=arxiv_obj["summary_detail"]["value"].replace("\n", " "),
        title=arxiv_obj["title"].replace("\n", " ").replace("  ", " ").replace("  ", " "),
    )
    return page_dict


def openreview_create_page_dict(openreview_id, openreview_url):
    if openreview_id is None and openreview_url is not None:
        openreview_id = OPENREVIEW_ID_REGEX.match(openreview_url).groups()[3]
    cli = openreview.Client("https://api.openreview.net")
    openreview_obj = cli.get_note(openreview_id)
    created = datetime.fromtimestamp(openreview_obj.cdate / 1000)
    page_dict = dict(
        url=f"https://openreview.org/forum?id={openreview_id}",
        pdf_url=f"https://openreview.org/pdf?id={openreview_id}",
        authors=openreview_obj.content["authors"],
        published_year=created.year,
        published_month=created.strftime("%m"),
        abs=openreview_obj.content["abstract"],
        title=openreview_obj.content["title"].replace("\n", " ").replace("  ", " ").replace("  ", " "),
    )
    return page_dict


def write_page(page_dict, template):
    page_output = template.render(**page_dict)
    with open(f"ignore/output/Paper: {page_dict['title']}.md", "w") as file_:
        file_.write(page_output)
    return page_output


@click.command()
@click.option("--paper_url", help="paper url of the paper you want to create a page for")
@click.option("--paper_id", help="paper Id of the paper you want to create a page for")
def main(paper_id, paper_url):
    """Simple Program to take an archive id and render the corresponding Roam page with data"""
    if paper_id is None and paper_url is None:
        clipboard_contents = pyperclip.paste()
        if ARXIV_ID_REGEX.match(clipboard_contents):
            paper_url = clipboard_contents
            page_dict = arxiv_create_page_dict(paper_id, paper_url)
        elif OPENREVIEW_ID_REGEX.match(clipboard_contents):
            paper_url = clipboard_contents
            page_dict = openreview_create_page_dict(paper_id, paper_url)
    template = get_template()
    page_output = write_page(page_dict, template)
    pyperclip.copy(page_output)
    sleep(1.0)
    pyperclip.copy(f"[[Paper: {page_dict['title']}]]")


if __name__ == "__main__":
    main()
