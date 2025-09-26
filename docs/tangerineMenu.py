# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QApplication
from tang_gui.tang_action import add_action
from tang_core.document.get_document import get_document


from tang_gui.get_tang_window import get_tang_window


def setPipelineMenu():
    """
    Add Tools menu UI and Pipeline Actions in File menu (ex: Pipeline SaveAs, Pipeline Open, etc)
    """
    app = QApplication.instance()
    doc = get_document()

    manager = doc.shortcuts_manager

    # Pipeline Actions
    manager.start_register_block()

    # File Menu
    tangMenuBar = app.main_window.menuBar()
    mainMenuActions = tangMenuBar.actions()

    fileMenu = None
    for action in mainMenuActions:
        if action.text() == "File":
            fileMenu = action.parent()
            break

    playblastMenu = None
    for action in mainMenuActions:
        if action.text() == "Playblast":
            playblastMenu = action.parent()
            break

    if fileMenu is None:
        print("File menu not found")
        return

    actionFileMenu = fileMenu.actions()

    # New
    pipelineNew = add_action(app.main_window, "Pipeline Build...", buildFile, shortcut="Ctrl+B")
    # pipelineNew.setText('Pipeline New...')
    fileMenu.insertAction(actionFileMenu[0], pipelineNew)

    # # Save
    pipelineSave = add_action(app.main_window, "Pipeline Save as", saveAsFile, shortcut="Ctrl+S+Shift", override=True)
    pipelineSave.setText("Pipeline Save As")
    fileMenu.insertAction(actionFileMenu[0], pipelineSave)

    fileMenu.insertSeparator(actionFileMenu[0])

    # tools menu
    productionMenu = tangMenuBar.addMenu("Production tools")
    # refresh file references
    toolsAction = add_action(app.main_window, "my tool action", toolAction)
    toolsAction.setText("my tool action")
    productionMenu.insertAction(None, toolsAction)

    manager.end_register_block()

def createMenu(app):
    """Overwrite Tangerine menu names and add Pipeline actions and menus"""
    menu_bar = app.main_window.menuBar()
    mainMenuActions = menu_bar.actions()

    # Rename classic actions
    for actionButton in mainMenuActions:
        if actionButton.text() == "New...":
            actionButton.setText("Tangerine New...")
        if actionButton.text() == "Load...":
            actionButton.setText("Tangerine Open...")
        if actionButton.text() == "Save":
            actionButton.setText("Tangerine Save")
        if actionButton.text() == "Save As...":
            actionButton.setText("Tangerine Save As...")

    # set pipeline actions
    setPipelineMenu()

def buildFile():
    """Call here the action code you want execute"""
    # check first if actual work has been saved or not
    if get_document().dirty:
        get_tang_window().ask_to_save_document() # ask user to save document first
    print("Launching Build")

def saveAsFile():
    """Call here the action code you want execute"""
    print("Launching SaveAs")

def toolAction():
    """Call here the action code you want execute"""
    print("Launching toolAction")
