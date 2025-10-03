---
sidebar_position: 1
---
# General Concepts

## Tangerine Files

## Tangerine Files

The files handled by Tang, via the File menu, come in several types:

  - `.shot` files represent shots. This is the format animators use all the time.

  - `.tang` files represent assets. They are referenced by .shot files. Assets can be manually referenced in an empty shot during preproduction to build a scene, but in general animators do not work directly with `.tang` files.

  - `.action` files represent intermediate animation exports of an asset. They can be imported onto the same asset in another shot. They do not contain constraint data or layer creations, which are stored in external files.
  To transfer animation between shots, it is recommended to use the Library, as it provides greater flexibility and smoother integration for the animator.

Additionally, some hidden files are created by Tang for internal use:

  - Pose and animation clip files from the Library

  - Layout and preference files

Tang also indirectly handles other non-native file types:

  - `.abc` files (Alembic format) are baked animations, used later in the pipeline for rendering. This format is also used for meshes and rig curves, referenced from `.tang` files.

  - Texture files (PNG or JPEG)

  - Sound files (WAV)

:::info
Finally, Tangerine provides an auto-save feature, which stores directly in `.shot` format. Auto-saves are stored in the following folder:
```
%TEMP%/tang/auto_saves @seb @max est ce que toujours vrai tang et pas tangerine ?
```
:::

## How Tangerine's API is structured

Tangerine is developed in Python, it relies on a C++ core called meta_nodal.

In practice, Tang’s Python code imports the `meta_nodal` module implemented in *"meta_nodal.pyd"*.
Therefore, there are two API layers:

- **The meta_nodal API** handles all low-level operations, such as creating and managing the scene graph, modifying its data, and serializing it into `.tang` files.
- **The Tangerine API** provides higher-level batch operations (on shots and `.shot` files) and allows extension of the GUI with new tools (open/save dialogs, animation plugins, etc.).

As an example (**Mikan**)[https://citrus-software.github.io/mikan-docs/], the open source rigging toolbox developed by our rigging team, clearly illustrates both aspects:
- Asset builds directly use the meta_nodal API.
- Interactive rigging tools (e.g., pose flipping) are integrated into Tang’s GUI through the Tangerine API.

The Tangerine API itself is divided into two main categories:
- Submodules of the tang_core module, which handle data operations, particularly batch processes.
- Submodules of the tang_gui module, which handle GUI integration and scripting of existing widgets.

:::info
In the API documentation, you may notice two distinct development approaches:

- “Python for GUI mode”: Methods in this mode handle UI updates directly and notify the engine that the document has been modified, triggering the appropriate callbacks. UI elements, such as progress bars, are also displayed for the user.

- “Python for batch mode”: This mode allows you to modify objects in the most optimized way, without requiring any UI feedback.
:::

## Setup your environment
You will possibly need an environment for your studio, a given production or a group of users.

### User setup
Use TANG_ENV_PATH variable to define the path of a user_setup.py file.
This file will be executing at every launch of Tangerine, before executing another command.

### Custom menus
Tangerine as been developped to be the closest possible of animators needs. Everything you will find native in the software has been optimized in UX and performances way.
Please contact us if you think any of your tools should be part of Tangerine.
That said, you may need to develop some workaround tools to integrate Tangerine in the best way possible for your teams.

You can customize menus, add buttons with preconfigured actions, or even add tools for your teams.
You will find an example in the demo-package.

<details>

  <summary>Add Custom Menus Sample</summary>

    In a Terminal, use for example:
    ```
    SET TANG_ENV_PATH="E:/TEMP/tangerine/Tangerine Demo 2025/api_tests/sample_scripts/"
    "C:\Program Files\TeamTO\Tangerine\1.7.14\TangerineConsole.exe" --log_to_file --kernel release -l debug
    ```
    The user_setup file will execute user_setup script that will create the custom menu develpped in tangerineMenu.py

</details>

## Launching Tangerine from Command Line

You can use scripting in GUI mode or in batch mode.

`GUI Mode` : The main mode launch the application with main window only. These following code example are using this GUI Mode, using methods that will take in charge UI aspects (refreshing viewport, showing progres, etc).

`GUI Console Mode` : A "console" mode with main window and console window is available to have verbosity and can be usefull in your developments.

`Batch Mode` : The batch mode of tangerine is also available. Every methods that are linked to the UI application part won't be available in this mode. See our code example in "batch" page to adapt your scripts to batch mode. See [Batch mode guide](batch#batch-mode).

@max @seb on a un bouton dans l'UI qui permet de la réaffichée si jamais ou a oublié en le lancant ?


### UI Mode

To launch Tangerine in UI mode, use the following command:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --log_to_file --kernel release
```

If you want to enable monitoring, replace the `--log_to_file` flag with `--monitoring`:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --kernel release
```

---

### Batch Mode

To launch Tangerine in Batch mode, use the following command:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --log_to_file --no-hidden --no-gui --kernel release
```

If you want to enable monitoring, use:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release
```

---

### Script Execution

You can append the path to one or more Python scripts directly in the command line:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release example.tang my_python_script.py
```

Scripts will be executed

### Script Execution

You can append the path to one or more Python scripts directly in the command line:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release example.tang my_python_script.py
```

Scripts will be executed **in order**. If a listed script does not exist, Tangerine will simply skip it.

---

### Help

For more details about the Tangerine command line, run:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe -h
```
