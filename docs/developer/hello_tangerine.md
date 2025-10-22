---
sidebar_position: 1
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Hello Tangerine

**Welcome to the Tangerine Developer Guide!** This part of the Tangerine documentation is intended to **Python developers**. With its scripting API, Tangerine allows you to develop custom Animation Tools, Pipeline scripts, Shot and Asset build scripts, and more! Here is our Hello Tangerine script, a quick start to jump straight into Tangerine Python development:

1. Launch Tangerine

2. Opens the "Command Line" via the Windows menu (it should pop under the Library window and above the Picker window).

3. Copy the following script, and paste it into the Command Line window and press Enter:
```python
# some module imports:
from tang_core.document.get_document import get_document
from tang_core.anim import set_animated_plug_value
from tang_core.callbacks import Callbacks
from tang_gui.get_tang_window import get_tang_window
import os

doc = get_document()  # the document is our main entry point to the Tangerine API

# we load JB the Capy asset
capy_path = os.getcwd() + "/demo/assets/capy_jb/capy_jb.tang"
asset_node = doc.import_nodes("character1:capy_jb", capy_path)  

# with a "modifier", we interact with the current shot to add keys:
with doc.modify("animate the capy") as modifier:
    controller = Callbacks().find_controller_in_asset(asset_node, "c_face_up")
    set_animated_plug_value(controller.el_blink_L, 0.0, modifier, frame=1, force_key=True)
    set_animated_plug_value(controller.el_blink_L, 1.0, modifier, frame=7)
    set_animated_plug_value(controller.el_blink_L, 0.0, modifier, frame=14)

# we change the main viewport camera to see our new animation!
viewport = get_tang_window().main_viewport
viewport.set_camera('cameras/right/Right')
viewport.frame_view()

```

4. Click anywhere outside the Command Line window, and press Space to play the animation. You should see this:

<div align="center">![console tangerine](./img/HelloTangerine.gif)</div>

<div align="center">**JB the Capy says Hello Tangerine!**</div>

&nbsp;
&nbsp;
  
:::info
Optionally copy/paste this script too in the Command Line to actually select the controller and see the keys in Tangerine Timeline, Channels window and Curve Editor:

```python
with doc.modify("select controller") as modifier:
	modifier.select_nodes([controller])
```
:::

In case you want a logged feedback of the script, just open the "Log View" window via the Windows menu. It appears by default next to the Tags window (in the top right tabbed views).

If you don't launch Tangerine.exe but TangerineConsole.exe the log is written in the system console too (be careful in this case: if you accidentaly close the console, Tangerine is closed too).

A log file is also written in the %TEMP%/Tangerine/logs folder.

The next section explains how to run scripts beyond the Command Line window, and after that we will see the Tangerine API Structure and discover some key concepts...