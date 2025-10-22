# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QApplication
from tang_gui.tang_action import add_action
from tang_core.document.get_document import get_document


from tang_gui.get_tang_window import get_tang_window


def set_pipeline_menu():
    """
    Add Tools menu UI and Pipeline Actions in File menu (ex: Pipeline SaveAs, Pipeline Open, etc)
    """
    app = QApplication.instance()
    doc = get_document()

    manager = doc.shortcuts_manager

    # Pipeline Actions
    manager.start_register_block()

    # File Menu
    tang_menu_bar = app.main_window.menuBar()
    main_menu_actions = tang_menu_bar.actions()

    file_menu = None
    for action in main_menu_actions:
        if action.text() == "File":
            file_menu = action.parent()
            break

    playblast_menu = None
    for action in main_menu_actions:
        if action.text() == "Playblast":
            playblast_menu = action.parent()
            break

    if file_menu is None:
        print("File menu not found")
        return

    action_file_menu = file_menu.actions()

    # New
    pipeline_new = add_action(app.main_window, "Pipeline Build...", build_file, shortcut="Ctrl+B")
    # pipeline_new.setText('Pipeline New...')
    file_menu.insertAction(action_file_menu[0], pipeline_new)

    # # Save
    pipeline_save = add_action(app.main_window, "Pipeline Save as", save_as_file, shortcut="Ctrl+S+Shift", override=True)
    pipeline_save.setText("Pipeline Save As")
    file_menu.insertAction(action_file_menu[0], pipeline_save)

    file_menu.insertSeparator(action_file_menu[0])

    # tools menu
    production_menu = tang_menu_bar.addMenu("Production tools")
    # refresh file references
    tools_action = add_action(app.main_window, "my tool action", tool_action)
    tools_action.setText("my tool action")
    production_menu.insertAction(None, tools_action)

    manager.end_register_block()

def create_menu(app):
    """Overwrite Tangerine menu names and add Pipeline actions and menus"""
    menu_bar = app.main_window.menuBar()
    main_menu_actions = menu_bar.actions()

    # Rename classic actions
    for action_button in main_menu_actions:
        if action_button.text() == "New...":
            action_button.setText("Tangerine New...")
        if action_button.text() == "Load...":
            action_button.setText("Tangerine Open...")
        if action_button.text() == "Save":
            action_button.setText("Tangerine Save")
        if action_button.text() == "Save As...":
            action_button.setText("Tangerine Save As...")

    # set pipeline actions
    set_pipeline_menu()

def build_file():
    """Call here the action code you want execute"""
    # check first if actual work has been saved or not
    if get_document().dirty:
        get_tang_window().ask_to_save_document() # ask user to save document first
    print("Launching Build")

def save_as_file():
    """Call here the action code you want execute"""
    print("Launching SaveAs")

def tool_action():
    """Call here the action code you want execute"""
    print("Launching toolAction")
