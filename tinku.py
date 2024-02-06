"""
Outputs web.py docs as html
version 2.0: documents all code, and indents nicely.
By Colin Rothwell (TheBoff)
"""

import inspect
import sys

import markdown

from web.net import websafe

sys.path.insert(0, "..")


ALL_MODULES = [
    "web.application",
    "web.contrib.template",
    "web.db",
    "web.debugerror",
    "web.form",
    "web.http",
    "web.httpserver",
    "web.net",
    "web.session",
    "web.template",
    "web.utils",
    "web.webapi",
    "web.wsgi",
]

item_start = '<code class="%s">'
item_end = "</code>"

indent_amount = 30

doc_these = (  # These are the types of object that should be docced
    "module",
    "classobj",
    "instancemethod",
    "function",
    "type",
    "property",
)
