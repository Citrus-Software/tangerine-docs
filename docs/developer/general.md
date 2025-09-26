---
sidebar_position: 1
---
# General Concepts

# How Tangerine's API is structured

Tangerine is developed in Python, Tangerine relies on a C++ core called **meta_nodal**.

In practice, Tang’s Python code imports the `meta_nodal` module implemented in *"meta_nodal.pyd"*.
Therefore, there are two API layers:

- **The meta_nodal API** for all low-level operations, such as creating and managing a scene graph, modifying its data, and serializing it into files (called `.tang`).
- **The Tangerine API** for batch operations provided by Tangerine (on shots, `.shot` files) and for extending its GUI with new tools (open/save dialogs, animation plugins, etc.).

As an example **Mikan**, the open source rigging toolbox developed by our rigging team, clearly illustrates both aspects:
- Asset builds directly use the meta_nodal API.
- Interactive rigging tools (pose flipping, etc.) integrated into Tang’s GUI via its API.

Finally, the Tangerine API itself is divided into two categories:
- Submodules of the **tang_core** module (handling data operations, especially batch processes).
- Submodules of the **tang_gui** module (handling integration into Tang’s GUI or scripting of existing widgets).

## Use Tangerine's API with UI

In Tangerine API you will find code that you can use for main actions in Tangerine : file operations, playblast operations, exports operations. These sample uses objects that exists only in UI mode, and are adapted the user showing him progressions and dealing with UI updates. Please find [the documention here](api)

## Use Tangerine's API in Batch mode

If you want to develop features without GUI, accelerating processes and not needed any UI feedback, you will find sample code adapted to batch mode when needed in code tabs.
For example, we would not use the ```app.main_window``` that exists only in GUI mode.

# Setup your environment
You will possibely need an environment for your studio, a given production or a group of users.

## User setup

Use TANG_ENV_PATH variable to define the path of a user_setup.py file.
This file will be executing at every launch of Tangerine, before executing another command.
You will find an example in the demo-package.

# Launching Tangerine from Command Line

## Tangerine Launching Modes
You can use scripting in GUI mode or in batch mode.

`GUI Mode` : The main mode launch the application with main window only. These following code example are using this GUI Mode, using methods that will take in charge UI aspects (refreshing viewport, showing progres, etc).

`GUI Console Mode` : A "console" mode with main window and console window is available to have verbosity and can be usefull in your developments.

`Batch Mode` : The batch mode of tangerine is also available. Every methods that are linked to the UI application part won't be available in this mode. See our code example in "batch" page to adapt your scripts to batch mode. See [Batch mode guide](batch#batch-mode).

@max @seb on a un bouton dans l'UI qui permet de la réaffichée si jamais ou a oublié en le lancant ?


## UI Mode
Use this command line to launch Tangerine in UI mode:

```
c:/"program files"/Tangerine/tangerineConsole.exe --log_to_file --kernel release
```

If you want to enable monitoring, add the `--monitoring` flag instead of `--log_to_file`:

```
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --kernel release
```

## Batch Mode

Use this command line to launch Tangerine in Batch mode:
```
c:/"program files"/Tangerine/tangerineConsole.exe --log_to_file --no-hidden --no-gui --kernel release
```

If you want to enable monitoring, add the `--monitoring` flag :
```
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release
```

:::tip
Usefull when you want to have different behaviours depending on the mode : UI or Batch
```python
# Return True if actual instance of Tangerine is a batch instance
isBatchMode = tangSoftwareApi.isBatchMode()
```
:::

## Script execution
Add any python script path to the command line as :

```
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release example.tang my_python_script.py
```
Python script will be executed ***in order***. If some scripts listed doesn't exists, Tangerine will skip it.
:::tip
You can call a tang file and several python files in the order you want.
```
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release before_loading.py scene.tang after_loading.py
```
You can also add a script that will take care of loading for you. See [use-case](usecase#activating-actions-after-saving-a-document)
:::

## help
Find more details about tangerine command line using :
```
c:/"program files"/Tangerine/tangerineConsole.exe -h
```

