# FTA to Markdown converter

A Pandoc filter to convert FTA docx chapter files into Markdown files.

## Installation

[Install Pandoc](https://pandoc.org/installing.html) for your operating system.

Then install the Python requirements.

    $ pip install -r requirements.txt

## Usage

    $ pandoc -s chapter1.docx -t json | ./filter.py stream | pandoc -s -f json -o chapter1.md

## What it does

It converts docx files into Markdown files. It takes the Pandoc AST JSON and applies a filter to it attempting to convert the relevant elements from the original Word document into the corresponding Markdown.

At present this consists of stripping out unwanted formatting as well as marking up headings correctly.

## What it doesn't do

The main thing it doesn't do at present is lists. Any additional work on this filter should look at translating the lists from docx into Markdown.

The translation of lists is especially problematic as the lists in the docx aren't actually formatted as real lists so all that can be relied upon is the numbering system of the lists to know when a list has begun, this is somewhat simple for top level lists but gets complicated when we want to handle lists within lists.
