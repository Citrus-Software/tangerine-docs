---
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Document

The Document is the entry point of any Python script for Tangerine. It reflects the current state of Tangerine: the current shot data (animations, loaded rigs, cameras...), the selection, the undo/redo history, and it can synchronize all the windows and widgets from user editions. Its generic name is voluntarily basic so everyone can understand it's the root Python object of everything in Tangerine. 

Note that the Document is different from the Qt application object, and it's different from the Qt main window object.
Here is how you can get those in your scripts:

```
from app.get_tang_app import get_tang_app
from tang_gui.get_tang_window import get_tang_window
from tang_core.document.get_document import get_document

app = get_tang_app()  # the Qt application, rarely used in your scripts
window = get_tang_window()  # the Qt main window (in GUI mode), use it to add custom menus/widgets
doc = get_document()  # the Tangerine API entry point, use it in ALL your scripts
```

Of course, you should not instanciate the Document class, there is only exactly one Document instance living in Tangerine.

Finally, know that all the multithreading stuff in Tangerine is handled by the Document too, especially stopping and relaunching its background engine to compute the rigs at each frame. Of course this is totally transparent to the developer, but in case you need a new export file format, you still need to ensure everything is computed before actually exporting any data, here is how:

```
from tang_core.document.get_document import get_document

doc = get_document()
doc.synch_compute_all_frames()  # ensure all rigs are computed at all frames

# ... export data in your format
```

This is automatically called when exporting to alembic or USD formats, and when playblasting, so call `synch_compute_all_frames()` only if you create a custom export function.

The following sections give the main Document attributes and functions.
The Tangerine API Reference lists all of them in a more exhaustively.

## Main Document Attributes

Here are the main attributes of the Document object that you can use in your scripts, for both read and write:

Attributes stored in the shot file:
- `start_frame` and `end_frame`: define the frame bounds of the current shot
- `fps`: usually 24 or 25, that's the number of frames per second the playback of Tangerine will give you
- `sound_path` and `sound_offset`: each shot can have a sound track, it's useful to synchronize the animation with actor voices and sound effetcs
- `library_server_path` and `picker_server_path`: paths you can setup for each production, this is where the library (preset poses and anim clips) and the pickers, all shared among animators, are stored.

Attributes **not** stored in the shot file:
- `saved_file_path`: used for both shot and asset files, it's empty until a file has been saved
- `current_frame`: that's the current frame for all viewports, you can see and edit it in the Timeline and the Curve Editor 
- `range_start_frame`and `range_end_frame`: see right above the Timeline, that's the range of playback the animator often need to focus on.
- `camera`: the camera set in the active viewport

Example script:
```
from tang_core.document.get_document import get_document

doc = get_document()
doc.fps = 25
doc.start_frame = 1
doc.end_frame = 40
doc.range_start_frame = 10
doc.range_end_frame = 30
doc.current_frame = 20
```

## Main Document Functions

### Document functions related to edition

- root() returns to root node that hold all the scene graph in Tangerine (see the Nodes section for more details)
- modify() returns a Modifier (see the Modifiers section for more details), it **must** be used in the pythonic way "with".
- node_selection() returns a list of all selected controller nodes, as seen in the Channels view, the Timeline and the Curve Editor

We already used modify() before, see in the Hello Tangerine page. And we used root() too when we loaded an alembic file because we needed a parent node to attach the loaded hierarchy to. Here is an example script where we use modify() again but with the node selection this time:

```
with document.modify("main functions example") as modifier:
	for node in document.node_selection():
		modifier.set_plug_value(node.tx, 2.0)
```

To test this script: add a few dummies in Tangerine, by default the Dummies windows is tabbed at the bottom right, with the Shot Constraints and Shot Clusters windows. Simply right click in the Dummies window and select "Create > cube" for example, add many dummies and press F to frame the camera viewport so you can see them. Press W for the Translation Tool and move them around. Then, copy/paste the script in the Command Line window and press Enter. See how the Translate X of each dummy selected has been set to 2.0 in the Channels view.

### Document functions related to shot files (*.shot)

To save a shot file, in both GUI mode or batch mode:
```
from tang_core.document.shot import Shot

Shot.export_shot_file(file_path, document)
```

To read a shot file, it's different in GUI mode and batch mode:

- in GUI mode:
```
from tang_gui.get_tang_window import get_tang_window

get_tang_window().import_shot_files([file_path])
```

- in batch mode (no GUI):
```
from tang_core.document.shot import Shot

Shot.import_shot_files([file_path], document)
```

----


Any asset node loaded in the document will have a top-node under `root` and all it's hierarchy under.
The top node of a reference is renamed using a namespace if needed.

Every nodes references in a document will be under the `root` node.

## Files operations

### Open document

<Tabs>
  <TabItem value="Python Code GUI" label="Python Code Tangerine GUI" default>
```python
# choose the references loading mode
from PySide2.QtWidgets import QApplication
from tang_core.asset.asset_load_mode import AssetLoadMode

TANG_LOAD_MODES = {
    "Load All": AssetLoadMode.ALL,
    "Load None": AssetLoadMode.NONE,
    "Load Default": AssetLoadMode.SAVED,
}

filePath = "[file_path]" # shot file

# get tangerine application instance
app = QApplication.instance()

# for this example we choose to load every reference
tangLoadMode = AssetLoadMode.ALL
# UI mode : specify to Tangerine we load shot file, so we have progression bar and relatives infos in tang
app.main_window.import_shot_files([filePath], load_mode=tangLoadMode)
```
  </TabItem>
  <TabItem value="Python Code batch" label="Python Code Tangerine batch" default>
In this mode, no api.main_window is available. Use following code to load your shot.

```python
from tang_core.document.shot import Shot
from tang_core.document.get_document import get_document

filePath = "[../../my_document_file_path.shot]"

document = get_document()
Shot.import_shot_files([filePath], document)
```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">

```python
from PySide2.QtWidgets import QApplication
from tang_core.asset.asset_load_mode import AssetLoadMode

DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"

# choose the references loading mode
TANG_LOAD_MODES = {
    "Load All": AssetLoadMode.ALL,
    "Load None": AssetLoadMode.NONE,
    "Load Default": AssetLoadMode.SAVED,
}

filePath = DEMO_FOLDER_PATH + "/api_samples/three_capy.shot" # shot file

# get tangerine application instance
app = QApplication.instance()

# for this example we choose to load every reference
tangLoadMode = AssetLoadMode.ALL
# UI mode : specify to Tangerine we load shot file, so we have progression bar and relatives infos in Tangerine
app.main_window.import_shot_files([filePath], load_mode=tangLoadMode)
```
  </TabItem>
</Tabs>

### Create new document
<Tabs>
  <TabItem value="Python Code GUI" label="Python Code Tangerine GUI" default>
    ```python
    from tang_gui.get_tang_window import get_tang_window

    # defining start and end frames of your shot
    startFrame = 1
    endFrame = 100
    fps = 24

    get_tang_window().do_new_document(self, start_frame=startFrame, end_frame=endFrame, fps=fps):
    ```
  </TabItem>
  <TabItem value="Python Code Batch" label="Python Code Tangerine Batch" default>
    ```python
    from tang_core.asset.asset_load_mode import AssetLoadMode
    from tang_core.document.get_document import get_document

    # defining start and end frames of your shot
    startFrame = 1
    endFrame = 100
    fps = 24

    # creating a document
    document = get_document()
    document.init_new(start_frame=startFrame, end_frame=endFrame, fps=fps)
    ```
  </TabItem>
</Tabs>

### Save document

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
    ```python
    from tang_core.document.shot import Shot
    from tang_core.document.get_document import get_document

    filePath = "[file_path]" # shot file

    document = get_document()
    Shot.export_shot_file(filePath, document)
    ```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">
    ```python
    from tang_core.document.shot import Shot
    from tang_core.document.get_document import get_document

    DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"
    filePath = DEMO_FOLDER_PATH + "/api_samples/my_saved_shot_2.shot"

    document = get_document()
    Shot.export_shot_file(filePath, document)
    ```
    As a result, a .shot file is created
    ![new file content](./../img/my_saved_shot.png)
  </TabItem>
</Tabs>


### Add custom document data
Custom data can be added to document using file infos as following.

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
    ```python
    from tang_core.document.get_document import get_document

    name = "[variable_name]" # name of the value you want to store
    text = "[you_text]"

    # adding a fileinfo of string type
    document = get_document()
    document.set_file_info(name, text)

    # getting the value in opened tangerine
    fileinfo = document.get_file_info(name, default=None)
    ```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">
    ```python
    from tang_core.document.get_document import get_document
    # name of the value you want to store
    name = "current pipeline version"
    text = "1.23.6"

    # adding a fileinfo of string type
    document = get_document()
    document.set_file_info(name, text)

    # getting the value in opened tangerine
    fileinfo = document.get_file_info(name, default=None)
    ```
    You can save again your file to see the added attribute in ascii.
    ![new file content](./../img/file_info_in_shot.png)
  </TabItem>
</Tabs>

## References
@seb @max a little explanation to add here

### List references

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
    ```python
    from tang_core.document.get_document import get_document
    from tang_core.asset.asset import Asset

    # getting root asset's nodes loaded
    nodes = list(Asset.loaded_assets(document))

    # add unloaded asset's nodes
    nodes += list(Asset.unloaded_assets(document))

    ## getting root nodes (not only assets)
    #nodes = document.root().get_children()

    nodes_dict = {node.get_name(): node for node in nodes}
    for node_name in nodes_dict.keys():
        print(node_name)
    ```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">
    Let's try to get roots node in scene of demo package.

    ```python
    from PySide2.QtWidgets import QApplication
    from tang_core.asset.asset import Asset
    from tang_core.asset.asset_load_mode import AssetLoadMode

    DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"

    # opening the scene in tangerine
    filePath = DEMO_FOLDER_PATH + "/api_samples/three_capy.shot" # shot file
    app = QApplication.instance()
    app.main_window.import_shot_files([filePath], load_mode=AssetLoadMode.ALL)

    # getting root asset's nodes loaded
    nodes = list(Asset.loaded_assets(document))

    # add unloaded asset's nodes
    nodes += list(Asset.unloaded_assets(document))

    nodes_dict = {node.get_name(): node for node in nodes}
    for node_name in nodes_dict.keys():
        print(node_name)
    ```
    As a result you will see in your Tangerine's console :
    ```
    capy_josh:jb
    capy_emily:jb
    character_n01_jb:jb
    camera:cam
    prop_n01_yuzu_logo:yuzu_logo
    set_n01_white_neutral_int:white_neutral_int
    prop_n01_tangerine_logo:tangerine_logo
    ```
  </TabItem>
</Tabs>

### Add references

An asset file should always have one and only one topnode.
See below how to reference an asset into a shot.

```python
from tang_core.document.get_document import get_document

@modifier
document = get_document()

filePath = "./capy_jb.tang"
namespace = "character"

# import_nodes(self, name, path, namespace='', modifier=None, asset_state=AssetState.LOADED)
document.import_nodes(None, filePath, modifier=modifier, namespace=namespace)
@sixtine to test
```
### Remove references


<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
    ```python
    from tang_core.document.get_document import get_document
    from tang_core.document.document import Undoable

    document = get_document()
    node = YOUR_ROOT_NODE # this is the root node that you want to remove

    # use modifier to certify your scene modifications that impacts nodal will be managed properly
    with document.modify("removing reference", undoable=Undoable.NO_AND_CLEAR_STACK) as modifier:

        # We delete pointers to the node
        node_name = node.get_name()
        del node

        document.unload_asset_from_name(node_name, modifier=modifier)
    ```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">

    ```python
    from PySide2.QtWidgets import QApplication
    from tang_core.asset.asset_load_mode import AssetLoadMode
    from tang_core.document.get_document import get_document
    from tang_core.document.document import Undoable

    DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"

    # opening the scene in tangerine
    filePath = DEMO_FOLDER_PATH + "/api_samples/three_capy.shot" # shot file
    app = QApplication.instance()
    app.main_window.import_shot_files([filePath], load_mode=AssetLoadMode.ALL)

    document = get_document()
    node = document.root().find("character_n01_jb:jb") # only asset nodes can be removed.

    with document.modify("removing reference", undoable=Undoable.NO_AND_CLEAR_STACK) as modifier:

        # We delete pointers to the node
        node_name = node.get_name() # name of the top node of the asset
        print("Removing node %s" % node_name)
        del node

        document.unload_asset_from_name(node_name, modifier=modifier)
    ```
    See the result in your node tree or in the asset manager.
    ![new file content](./../img/remove_reference.png)

  </TabItem>
</Tabs>

:::tip
It is necessary to remove any pointer to a node that you want to remove.
`del node`
:::

### Edit references path

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
```python
from tang_core.asset.asset_loader import AssetLoader
from tang_core.document.get_document import get_document

document = get_document()

newfilePath = "NEW_TANG_FILE_PATH" # path of .tang asset file you want to use
node_name = node.get_name()

with document.modify("update reference path", undoable=Undoable.NO_AND_CLEAR_STACK) as modifier:
    del node
    AssetLoader.replace_asset(node_name, newfilePath, modifier)

```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">

```python
from tang_core.asset.asset_loader import AssetLoader
from tang_core.document.get_document import get_document

document = get_document()

DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"
newfilePath = DEMO_FOLDER_PATH + "/api_samples/yuzu_logo.tang"

node = document.root().find("prop_n01_tangerine_logo:tangerine_logo")
node_name = node.get_name()

with document.modify("update reference path", undoable=Undoable.NO_AND_CLEAR_STACK) as modifier:
    del node
    AssetLoader.replace_asset(node_name, newfilePath, modifier)
```
  </TabItem>
</Tabs>

### Rename reference node

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
```python
from tang_core.document.document import Undoable
from tang_core.document.get_document import get_document

document = get_document()

# We want to rename node
node_name = node.get_name() # node is the node you want to rename
new_name = "NEW_ASSET_NAME"

with document.modify("rename_%s_to_%s" % (node_name, new_name), undoable=Undoable.NO_AND_CLEAR_STACK) as modifier:
    modifier.rename_node(assetNodesDict[node_name], new_name)
```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">

```python
from PySide2.QtWidgets import QApplication
from tang_core.asset.asset_load_mode import AssetLoadMode
from tang_core.document.get_document import get_document
from tang_core.document.document import Undoable

DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"

# opening the scene in tangerine
filePath = DEMO_FOLDER_PATH + "/api_samples/three_capy.shot" # shot file
app = QApplication.instance()
app.main_window.import_shot_files([filePath], load_mode=AssetLoadMode.ALL)

document = get_document()

# We want to rename node
node = document.root().find("character_n01_jb:jb/geo")
node_name = node.get_full_name() # node is the node you want to rename
new_name = "geometry"

with document.modify("rename_%s_to_%s" % (node_name, new_name), undoable=Undoable.NO_AND_CLEAR_STACK) as modifier:
    modifier.rename_node(node, new_name)

# if you want to change a namespace
node = document.root().find("character_n01_jb:jb")
node_name = node.get_full_name() # node is the node you want to rename
new_name = "character_kung_fu:jb"

with document.modify("rename_%s_to_%s" % (node_name, new_name), undoable=Undoable.NO_AND_CLEAR_STACK) as modifier:
    modifier.rename_node(node, new_name)

```
  </TabItem>
</Tabs>
