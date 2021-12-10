#!/bin/bash python
import argparse

from panflute import *


def remove_strong(elem, doc):
    if isinstance(elem, Strong):
        return Span(*elem.content)

    return elem


def create_heading(elem, level=1):
    removed_strong = elem.walk(remove_strong)

    return Header(*removed_strong.content, level=level)



def action(elem, doc):
    if isinstance(elem, BlockQuote):
        return [e for e in elem.content if not isinstance(e, Null)]

    if isinstance(elem, Para) and stringify(elem).lower().startswith("chapter"):
        doc.requires_chapter_heading = True
        return create_heading(elem)
    if isinstance(elem, Para) and doc.requires_chapter_heading:
        doc.requires_chapter_heading = False
        return create_heading(elem, level=2)

    if isinstance(elem, Para) and stringify(elem).lower().startswith("article"):
        doc.requires_article_heading = True
        return create_heading(elem, level=3)
    if isinstance(elem, Para) and doc.requires_article_heading:
        doc.requires_article_heading = False
        return create_heading(elem, level=4)

    return elem


def main(doc=None):
    return run_filter(action, doc=doc) 

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
