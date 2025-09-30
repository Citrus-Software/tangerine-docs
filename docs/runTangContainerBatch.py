# -*- coding: utf-8 -*-

import os
import sys

try:
    from PySide2.QtWidgets import QApplication
except ImportError:
    print("Tang modules not loaded")


args = {}
for element in " ".join(sys.argv).split(" --"):
    if not element.count(" ") >= 1:
        args[element.split(" ")[0]] = True
    else:
        args[element.split(" ")[0]] = " ".join(element.split(" ")[1:])


firstArg = args.get("[firstarg]", None)
secondarg = args.get("[secondarg]", None)
filePath = args.get("filePath", None)


# Develop here depending on your needs and args. Sample opening a document and printing a list of top nodes.

# opening filepath
from tang_core.document.shot import Shot
from tang_core.document.get_document import get_document

document = get_document()
Shot.import_shot_files([filePath], document)

# listing top nodes and printing nodes full name
nodes = document.root().get_children()
for node in nodes:
    print(node.get_full_name())

# to match a pipeline idea, could be opening > playblasting > exporting > saving in another location




