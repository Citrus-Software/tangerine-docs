---
sidebar_position: 2
---
# General Concepts

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
%TEMP%/Tangerine/auto_saves
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

