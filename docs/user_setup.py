# -*- coding: utf-8 -*-
# here is a user_setup.py script.
# You could use it to add external code/repo you will need for your production.
# You could use it to set some parameters for you production's users, such as library path of the production.
# you could use it as following adding custom menus in Tangerine menu bar

LIBRARY_PATH = "my/library/main/folder/path/"
print("user_setup execution")
try:
    from PySide2.QtWidgets import QApplication
except ImportError:
    pass

app = QApplication.instance()
# load opensave only in gui mode
batchMode = app.config.no_gui()
if not batchMode:
    from tangerineMenu import createMenu
    createMenu(app)
