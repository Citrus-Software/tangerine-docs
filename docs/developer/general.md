---
sidebar_position: 1
---
# General Concepts

Tang is developed in Python, Tang relies on a C++ core called **meta_nodal**.

In practice, Tang’s Python code imports the `meta_nodal` module implemented in *"meta_nodal.pyd"*.
Therefore, there are two API layers:

- **The meta_nodal API** for all low-level operations, such as creating and managing a scene graph, modifying its data, and serializing it into files (called `.tang`).
- **The Tang API** for batch operations provided by Tang (on shots, `.shot` files) and for extending its GUI with new tools (open/save dialogs, animation plugins, etc.).

As an example **Mikan**, the open source rigging toolbox developed by our rigging team, clearly illustrates both aspects:
- Asset builds directly use the meta_nodal API.
- Interactive rigging tools (pose flipping, etc.) integrated into Tang’s GUI via its API.

Finally, the Tang API itself is divided into two categories:
- Submodules of the **tang_core** module (handling data operations, especially batch processes).
- Submodules of the **tang_gui** module (handling integration into Tang’s GUI or scripting of existing widgets).

## Use API in Tang

If you want to develop feature using Tang in GUI mode please refer to this GUI Mode guide.
You will have the adapted way to do things taking into consideration the user that sees Tang Interface.

API in GUI mode starts from Application and uses modules loaded only in GUI mode, for example modules linked to viewport.

## Use API in Tang Batch

If you want to develop features without GUI, accelerating processes and not needed any UI feedback, please use the Batch Mode guide.

## Use Tang Library

If you need to develop features around tang's files structure, simply use the Library guide.




### Batch Mode
```python
from tang_core.document.shot import Shot
from tang_core.asset.asset_load_mode import AssetLoadMode
from tang_core.document.get_document import get_document

# choose the references loading mode
TANG_LOAD_MODES = {
    "Load All": AssetLoadMode.ALL,
    "Load None": AssetLoadMode.NONE,
    "Load Default": AssetLoadMode.SAVED,
}

# .tang filepath
filePath = "./my_tang_file.tang"

# for this example we choose to load every reference
tangLoadMode = AssetLoadMode.ALL

# open given filepath to current document
doc = get_document()
Shot.import_shot_files([filePath], doc)
```


# User setup

Use TANG_ENV_PATH vairable to define the path of a user_setup.py file.
This file will be executing at every launch of Tangerine, before executing another command.

[Download Minion](url_bat "download")

# Command line

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

## Script execution
Add any python script path to the command line as :

```
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release example.tang my_python_script.py
```
Python script will be executed after .tang files opening. @seb @max ya un ordre dexecution ??

:::tip
Find more details about tangerine command line using :
```
c:/"program files"/Tangerine/tangerineConsole.exe -h
```
:::
## Launching Tangerine in batch mode

## Query mode
Usefull when you want to have different behaviours depending on the mode : UI or Batch
```python
# Return True if actual instance of Tangerine is a batch instance
isBatchMode = tangSoftwareApi.isBatchMode()
```

## Restarting Tangerine
Restart tang opening the filePath given
```python
filePath = "./my_tang_file.tang"

app = get_tang_app()
args = app.tang_cmd_with_same_config(
    load_mode=AssetLoadMode.SAVED, extra_args=["--opensave=open", "--filePath=%s" % filePath]
)
app.restart_tang(args)

# Callbacks









