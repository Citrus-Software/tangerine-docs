# Developper guide

# Document

## Open document

### References loading modes

```python
# choose the references loading mode
from tang_core.asset.asset_load_mode import AssetLoadMode

TANG_LOAD_MODES = {
    "Load All": AssetLoadMode.ALL,
    "Load None": AssetLoadMode.NONE,
    "Load Default": AssetLoadMode.SAVED,
}
```

### UI Mode
```python
from PySide2.QtWidgets import QApplication
from tang_core.asset.asset_load_mode import AssetLoadMode

# get tangerine application instance
app = QApplication.instance()

# for this example we choose to load every reference
tangLoadMode = AssetLoadMode.ALL
# UI mode : specify to tang we load shot file, so we have progression bar and relatives infos in tang
app.main_window.import_shot_files([filePath], load_mode=tangLoadMode)
```
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

## Create new document
```python
from tang_core.document.shot import Shot
from tang_core.asset.asset_load_mode import AssetLoadMode
from tang_core.document.get_document import get_document

# defining start and end frames of your shot
startFrame = 1
endFrame = 100
fpd = 24

# creating a Shot in current document
doc = get_document()
doc.init_new(start_frame=startFrame, end_frame=endFrame, fps=fps)

# setting actual document filePath. will be stored in a file only at save.
doc.file_path = filePath
```

## Build shot
### option 1
```python

# create shot instance
shot = Shot()

# set shot frames settings
shot.start_frame = startFrame
shot.end_frame = endFrame
shot.fps = fps

# add sound file to shot
shot.sound_path = soundPath #editing this attribute will reload the sound file
```
@max @seb c'est quoi la dif entre les shot et le doc. Ya des element en plus dans le doc je dirais. Mais si je change le start et end du shot, je change celui du doc right ?

:::tip
Editing frame range will force the cache to reload.
In your workflow, if you need to change framerange using API, you would prefer to do it in ascii before loading your shot to minimize cache computing.

```python
import json
with open(filePath, "r") as fileIO:
    data = json.load(fileIO)
startFrame = fileJson["start_frame"]
endFrame = fileJson["end_frame"]
```
:::

### option 2
## Save shot

## Custom document data
Custom data can be added to document using file infos as following:
```python
from tang_core.document.get_document import get_document
# name of the value you want to store
name = "current pipeline version"
text = "1.23.6"

# adding a fileinfo of string type
doc = get_document()
doc.set_file_info(name, text)

# getting the value in opened tangerine
fileinfo = doc.get_file_info(name, default=None)
```

# References
## adding references
## removing references
## editing namespaces

# Playblasting

# Export

## export to alembic

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









