#!/bin/bash python
import re

from panflute import *


def combine_elements(elem, additional_elements):
    if not additional_elements:
        return elem

    return additional_elements + [elem]


def action(elem, doc):
    additional_elements = None

    if isinstance(elem, Strong):
        return Span(*elem.content)

    if isinstance(elem, BlockQuote):
        return [e for e in elem.content if not isinstance(e, Null)]

    if isinstance(elem, Para) and re.match("^\d+\.", stringify(elem)):
        if not doc.in_list:
            doc.in_list = True
            doc.list_items = [ListItem(Para(*elem.content[2:]))]
            return Null
        elif doc.in_list:
            doc.list_items.append(ListItem(Para(*elem.content[2:])))
            return Null
    elif isinstance(elem, Para) and re.match("^\([a-z]\)", stringify(elem)):
        current_list_item = doc.list_items[-1]
        current_list_item.content += [OrderedList(ListItem(Para(*elem.content[2:])))]
        return Null
    elif isinstance(elem, Para) and doc.in_list and stringify(elem).strip():
        doc.in_list = False
        additional_elements = [OrderedList(*doc.list_items)]

    if isinstance(elem, Para) and stringify(elem).lower().startswith("chapter"):
        doc.requires_chapter_heading = True
        return combine_elements(Header(*elem.content), additional_elements)
    if isinstance(elem, Para) and doc.requires_chapter_heading:
        doc.requires_chapter_heading = False
        return combine_elements(Header(*elem.content, level=2), additional_elements)

    if isinstance(elem, Para) and stringify(elem).lower().startswith("article"):
        doc.requires_article_heading = True
        return combine_elements(Header(*elem.content, level=3), additional_elements)
    if isinstance(elem, Para) and doc.requires_article_heading:
        doc.requires_article_heading = False
        return combine_elements(Header(*elem.content, level=4), additional_elements)

    return combine_elements(elem, additional_elements)

def prepare(doc):
    doc.in_list = False
    doc.requires_chapter_heading = False
    doc.requires_article_heading = False
    doc.list_items = []

def main(doc=None):
    return run_filter(action, prepare=prepare, doc=doc) 

if __name__ == '__main__':
    # with open("chapter5.json", encoding="utf-8") as f:
    #     doc = load(f)
    #     main(doc)
    main()
