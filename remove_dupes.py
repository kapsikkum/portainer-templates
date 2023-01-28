# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2023-01-29 00:19:52
# @Last Modified by:   kapsikkum
# @Last Modified time: 2023-01-29 00:50:52
import json
from typing import Dict, Union

from bs4 import BeautifulSoup
from markdown import markdown

old_templates: Dict = json.load(open("templates.json"))
new_templates: Dict = dict(old_templates)

new_templates["templates"] = list()


def remove_markdown(string: str) -> str:
    html = markdown(string)
    return "".join(BeautifulSoup(html).findAll(text=True))


def add_to_new(template) -> Union[Dict, None]:
    # print(t["title"] for t in new_templates["templates"])
    if not template["title"].lower() in (
        t["title"].lower() for t in new_templates["templates"]
    ):
        print(template["title"])
        template["description"] = remove_markdown(template["description"])

        new_templates["templates"].append(template)

        return template
    return None


def write_to_file(data: dict, filepath: str = "./deduped.json"):
    with open(filepath, "w+") as w:
        w.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    for t in old_templates["templates"]:
        add_to_new(t)

    write_to_file(new_templates)
