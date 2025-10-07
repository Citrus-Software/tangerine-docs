---
sidebar_position: 1
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Playblast

## Create playblast settings

Create a `PlayblastSettings` object to specify the characteristics of your playblast, such as SSAO, camera, time range, and more.

```python
from tang_core.playblast.playblast_settings import PlayblastSettings
from tang_core.document.get_document import get_document

width = 1280
height = 720

document = get_document()
startFrame = document.start_frame
endFrame = document.end_frame


playblastSettings = PlayblastSettings(start=startFrame, end=endFrame, width=width, height=height)

playblastSettings.export_audio = False


playblastSettings.texture = True # default value
playblastSettings.smooth = True # default value

playblastSettings.auto_open = False # Open folder of exported playblast at the end # default value
playblastSettings.overwrite = True # Authorize overwriting output files is already exists # default value
playblastSettings.ignore_types = "Joint,Curve" # Do not include in viewport these types of objects, could be also grid,tool,corneas,__dummies__ # default value

playblastSettings.enable_ssao = True # default value
playblastSettings.ssao_kernel_size = 64 # default value
playblastSettings.ssao_power = 2.0 # default value
playblastSettings.ssao_radius = 0.3 # default value
```

## Launch playblast settings

```python
from tang_core.document.get_document import get_document
from tang_core.playblast.playblast import Playblast

document = get_document()

# search for the camera node in scene you want to use for playblast
camera = "cameras/persp/Persp"
cameraNode = document.root().find(camera)

imagePath = "E:/TEMP/Tangerine/Tangerine Demo 2025/api_samples/playblast_folder/my_playblast_images.jpg"

Playblast.playblast(document, cameraNode, imagePath, settings=playblastSettings) # see previous part to create playblast settings
```

## Viewport subdivision

To apply subdivision, use the following lines of code.
The subdivision values you set here will be used if the "smooth" option in the Playblast settings is enabled.

```python
from tang_core.shape import SubdivisionOverride, set_general_subdivision_override
from tang_core.document.get_document import get_document

document = get_document()

# choose subdivision value, ON = full smooth value, HALF_LEVEL = Half the smooth value, OFF = not smoothed at all
subdivOverride = SubdivisionOverride.ON
with document.modify("subdiv_override") as modifier:
    set_general_subdivision_override(subdivOverride, modifier)
```

You can see level of subdivision applied, in plugs view selecting a mesh.
The subdivision value used is the value stored in plug `subdivision_level`
![subdivision level override](./../img/subdivision_level.png)

If you need some mesh to have different subdivision properties, use these lines:

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
```python
from tang_core.shape import SubdivisionOverride, set_subdivision_override
from tang_core.document.get_document import get_document

document = get_document()

subdivOverride = SubdivisionOverride.OFF  # ON = full smooth value, HALF_LEVEL = Half the smooth value, OFF = not smoothed at all

mesh = [YOUR_NODE] # node of type Geometry
with document.modify("subdiv_override") as modifier:
    set_subdivision_override(mesh, subdivOverride, modifier)

```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">
```python
from tang_core.shape import SubdivisionOverride, set_subdivision_override, set_general_subdivision_override
from tang_core.asset.asset_load_mode import AssetLoadMode
from tang_core.document.get_document import get_document
from PySide2.QtWidgets import QApplication
from meta_nodal_py import Geometry

# opening scene
DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"
filePath = DEMO_FOLDER_PATH + "/api_samples/three_capy.shot" # shot file
app = QApplication.instance()
app.main_window.import_shot_files([filePath], load_mode=AssetLoadMode.ALL)

document = get_document()

# set full subdivision on all meshs of the scene
subdivOverride = SubdivisionOverride.ON
with document.modify("subdiv_override") as modifier:
    set_general_subdivision_override(subdivOverride, modifier)

# set OFF subdivision on set hierarchy
assetNode = document.root().find("set_n01_white_neutral_int:white_neutral_int")
# listing Geometry nodes in assetNode hierarchy
subdivOverride = SubdivisionOverride.OFF  # ON = full smooth value, HALF_LEVEL = Half the smooth value, OFF = not smoothed at all
with document.modify("subdiv_override") as modifier:
    for it in assetNode.depth_first_skippable_iterator():
        node = it.node
        if isinstance(node, Geometry):
            print(node.get_name())
            set_subdivision_override(node, subdivOverride, modifier)
```
  </TabItem>
</Tabs>
