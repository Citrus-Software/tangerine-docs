---
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Document

The Document is the entry point of any Python script for Tangerine. It reflects the current state of Tangerine: the current shot data (animations, loaded rigs, cameras...), the selection, the undo/redo history, and it can synchronize all the windows and widgets from user editions. Its generic name is voluntarily basic so everyone can understand it's the root Python object of everything in Tangerine. 

Note that the Document is different from the Qt application object, and it's different from the Qt main window object.
Here is how you can get those in your scripts:

```python
from app.get_tang_app import get_tang_app
from tang_gui.get_tang_window import get_tang_window
from tang_core.document.get_document import get_document

app = get_tang_app()  # the Qt application, rarely used in your scripts
window = get_tang_window()  # the Qt main window (in GUI mode), use it to add custom menus/widgets
doc = get_document()  # the Tangerine API entry point, use it in ALL your scripts
```

Of course, you should not instanciate the Document class, there is only exactly one Document instance living in Tangerine.

Finally, know that all the multithreading stuff in Tangerine is handled by the Document too, especially stopping and relaunching its background engine to compute the rigs at each frame. Of course this is totally transparent to the developer, but in case you need a new export file format, you still need to ensure everything is computed before actually exporting any data, here is how:

```python
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

Example script:
```python
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

- `root()` returns to root node that hold all the scene graph in Tangerine (see the Nodes section for more details)
- `modify()` returns a Modifier (see the Modifiers section for more details), it **must** be used in the pythonic way "with".
- `node_selection()` returns a list of all selected controller nodes, as seen in the Channels view, the Timeline and the Curve Editor

We already used modify() before, see in the Hello Tangerine page. And we used root() too when we loaded an alembic file because we needed a parent node to attach the loaded hierarchy to. Here is an example script where we use modify() again but with the node selection this time:

```python
with document.modify("main functions example") as modifier:
	for node in document.node_selection():
		modifier.set_plug_value(node.tx, 2.0)
```

To test this script: add a few dummies in Tangerine, by default the Dummies windows is tabbed at the bottom right, with the Shot Constraints and Shot Clusters windows. Simply right click in the Dummies window and select "Create > cube" for example, add many dummies and press F to frame the camera viewport so you can see them. Press W for the Translation Tool and move them around. Then, copy/paste the script in the Command Line window and press Enter. See how the Translate X of each dummy selected has been set to 2.0 in the Channels view.

### Document functions related to shot files (*.shot)

To **save** a shot file, in both GUI mode or batch mode:
```python
from tang_core.document.shot import Shot
from tang_core.document.get_document import get_document

Shot.export_shot_file(file_path, get_document())
```

To **read** a shot file, it's different in GUI mode and batch mode:

- in GUI mode:
```python
from tang_gui.get_tang_window import get_tang_window

get_tang_window().import_shot_files([file_path])
```

- in batch mode (no GUI):
```python
from tang_core.document.shot import Shot
from tang_core.document.get_document import get_document

Shot.import_shot_files([file_path], get_document())
```

To **create** a new shot, it's also different in GUI mode and batch mode:

- in GUI mode:
```python
from tang_gui.get_tang_window import get_tang_window

get_tang_window().do_new_document(start_frame=1, end_frame=100, fps=24)
```

- in batch mode (no GUI):
```python
from tang_core.document.get_document import get_document

get_document().init_new(start_frame=1, end_frame=100, fps=24)
```

We have seen in this section what the Document is, and what are its main attributes and functions. The full documentation of the Document class is given in the Tangerine API Reference.
We have seen briefly how a modifier can alter the values of the shot by modifying node values. The next sections give more details about **Nodes** and **Modifiers**.
