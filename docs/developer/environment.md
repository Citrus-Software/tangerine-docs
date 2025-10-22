---
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Running scripts

The previous section explained how to run a script from within Tangerine by using the Command Line window, but in general we run Tangerine scripts through a pipeline by calling the software in a system terminal or in a shell script:

- Script to launch Tangerine and directly run your script:

```
.\Tangerine.exe path_to/your_script.shot
```

- Script to launch Tangerine, open a shot file and call your script:

```
.\Tangerine.exe path_to/your_show.shot other_path_to/your_batch_script.py
```

Note you may add multiple scripts in the command.

- Batch processes that don't need any GUI can be called with the `--no-gui` argument:

```
.\Tangerine.exe --no-gui path_to/your_show.shot other_path_to/your_batch_script.py
```

In this case, Tangerine is launched but does not pop any window, it exits once the script is over.

:::important
The working directory (cwd) should always be set to the installation directory where Tangerine.exe is located before launching Tangerine.exe.
:::

See the Command Line Arguments page to list all the possible argument you can pass to Tangerine.

## Production Environment

You will possibly need an environment for your studio, a given production or a group of users. In this case, you may want to ensure a given script is actually executed first every time Tangerine is launched. In this script you would setup some paths (for libraries, and pickers) and initialize your own tools to customize the Tangerine GUI.

To do so, use the `TANG_ENV_PATH` environment variable on your system to define the path of a `user_setup.py` file.
This file will be executing at every launch of Tangerine, before executing another command.

## Custom menu and GUI

Tangerine as been developped to be the closest possible of animators needs. Everything you will find native in the software has been optimized in UX and performances way.
Please contact us if you think any of your tools should be part of Tangerine.
That said, you may need to develop some workaround tools to integrate Tangerine in the best way possible for your teams.

You can customize menus, add buttons with preconfigured actions, or even add tools for your teams.
Here is a very simple startup script to add your own menu in Tangerine, with a command to show a custom Qt Window:

```python
from tang_gui.get_tang_window import get_tang_window
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget

main_window = get_tang_window()

def show_my_tool_window():
    my_tool_widget = QWidget(main_window)
    my_tool_widget.setWindowTitle('My Tool')
    my_tool_widget.setFixedHeight(100)  # replace this with your layout of widgets
    main_window.add_dock_for_view(my_tool_widget, Qt.RightDockWidgetArea)

if main_window:  # safety in case Tangerine is called in --no-gui mode
    from tang_gui.tang_action import add_action
    menu_bar = main_window.menuBar()
    my_menu = menu_bar.addMenu('My Studio')
    my_menu.addAction(add_action(main_window, "My Tool", show_my_tool_window))
```

Save this file in my_tool.py and call:

```
.\Tangerine.exe path_to/my_tool.py
```

Now, you have the "My Studio" menu with the "My Tool" menu item and if you select it the "My Tool" window appears docked at the bottom left of the Tangerine GUI!

:::tip
You may call .\TangerineConsole.exe instead of .\Tangerine.exe to see your script output (and errors) in the Console. Otherwise you should look at the log file in %TEMP%/Tangerine/logs
:::

Tangerine doesn't have a full blown script editor and debugger, that's because today most TDs prefer to use standard Python editors for that purpose. The main Python IDEs today are VS Code from Microsoft (free) and PyCharm from Jetbrains (a free community edition is available).

## Editing and Debugging your scripts with VS Code

You first need to have the Python langage extension from Microsoft added to VS Code.

Then, set this configuration in your `launch.json` file:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "debugpy",
            "name": "Attach Tangerine App",
            "request": "attach",
            "processId": "${command:pickProcess}",
            "connect": { "host": "127.0.0.1", "port": 5678 }
        }
    ]
}
```

As we don't provide the `debugpy` module in the Tangerine interpreter, you need to create a compatible venv (ie **Python 3.9**) and pip install this module in it:

```
MyScripts
   |
   +-- my_tool.py <= use the script above
   |
   +-- wait_debug.py <= see below
   |
   +-- .venv <= Python 3.9 virtual environment where you added the debugpy module
   |
   +-- .vscode
         |	
         +-- launch.json
```

Here is the `wait_debug.py` code:

```python
from pathlib import Path
import os
import site

# we activate the site-packages of a compatible venv:
here = Path(__file__).resolve().parent
venv = here / ".venv"
if os.name == "nt":
    sp = venv / "Lib" / "site-packages"  # Windows: <venv>\Lib\site-packages
else:
    pyver = f"python{sys.version_info.major}.{sys.version_info.minor}"
    sp = venv / "lib" / pyver / "site-packages"  # Linux: <venv>/lib/pythonX.Y/site-packages
if sp.exists():
    site.addsitedir(str(sp))
else:
	raise RuntimeError("Cannot find site-packages in the venv")
	
# we import debugpy from the venv above and wait for the connection
try:
    import debugpy
except ImportError:
    raise RuntimeError("debugpy is not installed in the venv")
debugpy.listen(("127.0.0.1", "5678"))
debugpy.wait_for_client()
```

Then, launch Tangerine with this new script **first**:
```
.\TangerineConsole.exe C:\MyScripts\wait_debug.py C:\MyScripts\my_tool.py
```

In VS Code, set a breakpoint anywhere in `my_tool.py`, launch "Attach Tangerine App" and select the Tangerine process in the dropdown menu. You should break on the breakpoint!

:::tip
**Aucompletion in VS Code!**

In your `settings.json` add the following lines to get autocompletion with the Tangerine API (you may have to replace the path with your custom Tangerine installation directory):
```json
    "python.analysis.extraPaths": [
        "C:/Program Files/Tangerine/stubs",
    ],    
    "python.autoComplete.extraPaths": [
        "C:/Program Files/Tangerine/stubs",
    ],
```
:::

## Hot reload of scripts

Sometimes you make changes to your script and you want Tangerine to take the changes into account without relaunching it.
You can do that with hot reload of modules. Indeed, Tangerine uses `importlib.import_module(your_script_name)` where your_script_name is the filename of your script without the py extension. So, hot reloading a script is equivalent to reloading a python module with the same name. Enter the following in the Command Line window of Tangerine when your script has changed:

```python
import sys
sys.modules.pop(script_name, None)
```

:::warning
You cannot hot reload scripts where a reference to your script objects/functions has been given to the Tangerine interpreter.
For example, in the above script my_tool.py we give a reference to the function `show_my_tool_window()` to Tangerine so this script cannot be hot reloaded. In practice, add your updatable code in another module loaded via import_module, and hot reload only this module where no reference has been given in Tangerine or if you can delete them before the reload (see example below).
:::

In the following example, the second script (my_edit.py) can be hot reloaded:

1. Modify my_tool.py:

```python
from tang_gui.get_tang_window import get_tang_window
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QPushButton
import importlib

main_window = get_tang_window()

def on_clicked():
    my_edit = importlib.import_module("my_edit")
    my_edit.do_it()
	
def show_my_tool_window():
    my_tool_widget = QWidget(main_window)
    my_tool_widget.setWindowTitle('My Tool')
    btn = QPushButton('Do it!', my_tool_widget)
    btn.clicked.connect(on_clicked)
    main_window.add_dock_for_view(my_tool_widget, Qt.RightDockWidgetArea)

if main_window:  # safety in case Tangerine is called in --no-gui mode
    from tang_gui.tang_action import add_action
    menu_bar = main_window.menuBar()
    my_menu = menu_bar.addMenu('My Studio')
    my_menu.addAction(add_action(main_window, "My Tool", show_my_tool_window))
```

2. Add my_edit.py:

```python
from tang_core.document.get_document import get_document
from tang_core.callbacks import Callbacks

doc = get_document()

asset_node = doc.root().find("character1:capy_jb")

with doc.modify("animate the capy") as modifier:
    controller = Callbacks().find_controller_in_asset(asset_node, "c_face_up")
    set_animated_plug_value(controller.el_blink_L, 0.0, modifier, frame=1, force_key=True)
    set_animated_plug_value(controller.el_blink_L, 1.0, modifier, frame=7)
    set_animated_plug_value(controller.el_blink_L, 0.0, modifier, frame=14)
```

3. Launch Tangerine with my_tool.py as the argument.

4. Import JB the Capy asset via the File menu, or by using this script in the Command Line window:
```python
import os
capy_path = os.getcwd() + "/demo/assets/capy_jb/capy_jb.tang"
document.import_nodes("character1:capy_jb", capy_path) 
```

4. Click on "Do it!", the Capy now blinks just like in Hello Tangerine

5. Undo (Ctrl+Z) and select **Clear History** in the Edit menu to **remove the Tangerine reference to the modifier**

6. Modify my_edit.py, put 0.5 instead of 1.0 in the second call of set_animated_plug_value (frame 7) so that the Capy will half blink.
```python
    # ...
    set_animated_plug_value(controller.el_blink_L, 0.5, modifier, frame=7)
    # ...                                          ^^^
```
7. Call this in the Command Line window:

```python
import sys
sys.modules.pop("my_edit", None)
```

8. Click on "Do it!" again and see the Capy half blinks!

:::tip
The following works too, it may be more convenient because sys.modules.pop is not required then:
```python
def on_clicked():
    import importlib, my_edit
    importlib.reload(my_edit)  # force the reload of the module (even if it has not changed)
```
:::
