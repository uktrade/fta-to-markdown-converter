#!/bin/bash python
import argparse

from panflute import *


def action(elem, doc):
    if isinstance(elem, Strong):
        return Span(*elem.content)

    if isinstance(elem, BlockQuote):
        return [e for e in elem.content if not isinstance(e, Null)]

    if isinstance(elem, Para) and stringify(elem).lower().startswith("chapter"):
        doc.requires_chapter_heading = True
        return Header(*elem.content)
    if isinstance(elem, Para) and doc.requires_chapter_heading:
        doc.requires_chapter_heading = False
        return Header(*elem.content, level=2)

    if isinstance(elem, Para) and stringify(elem).lower().startswith("article"):
        doc.requires_article_heading = True
        return Header(*elem.content, level=3)
    if isinstance(elem, Para) and doc.requires_article_heading:
        doc.requires_article_heading = False
        return Header(*elem.content, level=4)

    return elem

def prepare(doc):
    doc.in_list = False
    doc.requires_chapter_heading = False
    doc.requires_article_heading = False
    doc.list_items = []

def main(doc=None):
    return run_filter(action, prepare=prepare, doc=doc) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="COMMAND")

    subparsers = parser.add_subparsers()

    parser_stream = subparsers.add_parser("stream", help="Stream from stdin to stdout")

    parser_files = subparsers.add_parser("files", help="Input and output to files")
    parser_files.add_argument("input_filename")
    parser_files.add_argument("output_filename")

    parsed_args = parser.parse_args()

    if hasattr(parsed_args, "input_filename"):
        with open(parsed_args.input_filename, encoding="utf-8") as f:
            doc = load(f)
        doc = main(doc)
        with open(parsed_args.output_filename, "w", encoding="utf-8") as f:
            dump(doc, f)
    else:
        main()
