---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Build Shots in Pipeline

In a pipeline vision, you will need to create automations and build many shots at once.
You can create a `Shot` object, which allows you to add all necessary attributes directly to the new object and save it to a file.
This approach skips loading data into Tangerine when it is not needed.

For example, if you want to quickly generate all `.shot` files for a sequence.

```python
from tang_core.document.shot import Shot

# create shot instance
shot = Shot()

# set shot frames settings
shot.start_frame = 1
shot.end_frame = 15
shot.fps = 24

# add sound file to shot
shot.sound_path = "" # editing this attribute will reload the sound file

# add references to assets, using fullpath
shot.add_asset("prop_n01_yuzu_logo:yuzu_logo", {"file_path": "E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/yuzu_logo.tang"})
shot.add_asset("character_n01_jb:jb", {"file_path": "E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/capy_jb.tang"})

# saving to a file
filePath = "E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/built_shot.shot"
shot.export_file(filePath)

```
:::tip
Editing the frame range will force the cache to reload.
In your workflow, if you need to change the frame range using the API, it is preferable to do this in the ASCII `.shot` file **before** loading it into Tangerine to minimize cache computation.

```python
import json

with open(filePath, "r") as fileIO:
    data = json.load(fileIO)

startFrame = data["start_frame"]
endFrame = data["end_frame"]
```
:::
