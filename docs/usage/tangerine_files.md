# Tangerine Files

The files handled by Tangerine, via the File menu, come in several types:

  - `.shot` files represent shots. This is the format animators use all the time.
  - `.tang` files represent assets. They are referenced by .shot files. Assets can be manually referenced in an empty shot during preproduction to build a scene, but in general animators do not work directly with `.tang` files.
  - `.action` files represent intermediate animation exports of an asset. They can be imported onto the same asset in another shot. They do not contain constraint data or layer creations, which are stored in external files.
  To transfer animation between shots, it is recommended to use the Library, as it provides greater flexibility and smoother integration for the animator.

Additionally, some hidden files are created by Tangerine for internal use:

  - Pose and animation clip files from the Library
  - Layout and preference files

Tangerine also indirectly handles other non-native file types:

  - `.abc` files (Alembic format) are baked animations, used later in the pipeline for rendering. This format is also used for meshes and rig curves, referenced from `.tang` files.
  - Texture files (PNG or JPEG)
  - Sound files (WAV)

:::info
Finally, Tangerine provides an auto-save feature, which stores directly in `.shot` format. Auto-saves are stored in the following folder:
```
%TEMP%/Tangerine/auto_saves
```
