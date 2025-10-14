---
sidebar_position: 1
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# API Structure

Tangerine is developed in Python 3.9, it relies on a C++ core called **meta_nodal** for everything related to performance (OpenGL viewports, multithreading evaluation of rigs, etc).
All the GUI is handled by the [Qt for Python library](https://doc.qt.io/archives/qtforpython-5/), also known as PySide2.
You may write your own tools with your custom graphic interfaces by using Qt just as we does.

In practice, Tang’s Python code imports the `meta_nodal` module implemented in *"meta_nodal.pyd"*.
Therefore, there are two API layers:

- **The meta_nodal API** handles all low-level operations, such as creating and managing the scene graph, modifying its data, and serializing it into `.tang` files.
- **The Tangerine API** provides higher-level batch operations (on `.shot` files) and allows extension of the GUI with new tools (open/save dialogs, animation plugins, etc.).

As an example, [**Mikan**](https://citrus-software.github.io/mikan-docs/), the open source rigging toolbox developed by our rigging team, clearly illustrates both aspects:
- Asset build is a batch process that directly use the meta_nodal API.
- Interactive rigging tools (pose flip and mirror, IK/FK switches, etc.) are integrated into Tang’s GUI through the Tangerine API.

## The meta_nodal API

The meta_nodal API is mainly used when we want to access the rigging nodes, or math nodes and data, or any load/export of abc/usd files.
All the meta_nodal API is in one module - **meta_nodal_py** - and it holds the **Imath** submodule for all mathematical classes and functions.
For example, in the following script we load the modeling of JB the Capy, the asset we used in the previous page (see Hello Tangerine), by using the load_abc function from the meta_nodal API:
```
from meta_nodal_py import load_abc
import os
load_abc(document.root(), os.getcwd() + "/demo/assets/capy_jb/capy_modeling.abc")
document.rig_has_changed_without_modifiers()
```
You can copy/paste this script in the Command Line window and press Enter, just like you did on the previous page.
Note, by the way, that the `document` variable is always predefined in the Command Line window.

Here is another example of the meta_nodal API, using the Imath submodule, it double the scale of the imported 'geo' node from the previous script:
```
from meta_nodal_py.Imath import V3f, M44f
xform = M44f()
xform.setScale(V3f(2.0))
document.root().find('geo').transform.set_value(xform)
document.rig_has_changed_without_modifiers()
```
Note that we always need to call `document.rig_has_changed_without_modifiers()` to update the internals of Tangerine, including the GUI, when we use the meta_nodal API and when no modifier is used.
The modifier concept will be explained in the next sections, it's part of the Tangerine API.

## The Tangerine API

In fact, we use the Tangerine API most of the time, it is divided itself into two main categories:
- Submodules of the **tang_core** module, which handle data operations, particularly batch processes.
- Submodules of the **tang_gui** module, which handle GUI integration and scripting of existing widgets.

On the previous page (see Hello Tangerine), we have seen how the script import python modules from both of them:
```
from tang_core.document.get_document import get_document
from tang_core.anim import set_animated_plug_value
from tang_core.callbacks import Callbacks
from tang_gui.get_tang_window import get_tang_window
```

As you can see in all the scripts we've seen so far, and for all APIs, the **Document** is always the entry point. It reflects the current state of Tangerine, it holds all the data of the current shot, as well as other edition states.
The next section details this concept.
