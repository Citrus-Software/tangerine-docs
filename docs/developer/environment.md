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

## Debugging your scripts with VS Code

TODO

## Debugging your scripts with PyCharm

TODO
