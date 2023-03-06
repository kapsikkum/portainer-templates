# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2023-01-29 00:19:52
# @Last Modified by:   kapsikkum
# @Last Modified time: 2023-03-07 09:52:21
import json
from typing import Dict, Union

from bs4 import BeautifulSoup
from markdown import markdown

old_templates: Dict = json.load(open("unsorted.json"))
new_templates: Dict = dict(old_templates)

new_templates["templates"] = []


def remove_markdown(string: str) -> str:
    html = markdown(string)
    return "".join(BeautifulSoup(html, "lxml").findAll(text=True))


def sort_templates(templates):
    return sorted(templates, key=lambda template: template["title"])


def add_to_new(template) -> Union[Dict, None]:
    if template["title"].lower() not in (
        t["title"].lower() for t in new_templates["templates"]
    ):
        template["description"] = remove_markdown(template["description"])

        new_templates["templates"].append(template)

        return template
    return None


def write_to_file(data: dict, filepath: str = "./templates.json"):
    with open(filepath, "w+") as w:
        w.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    for t in old_templates["templates"]:
        add_to_new(t)

    new_templates["templates"] = sort_templates(new_templates["templates"])

    print(
        f"{len(new_templates['templates']) - len(old_templates['templates'])} new templates, {len(new_templates['templates'])} total."
    )

    write_to_file(new_templates)
