---
sidebar_position: 4
---
# Libraries


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

# read references from ascii

```python
def listReferencesFromASCII(self):
        """
        Return a dict of filepath per namespace in the ASCII shot
        """
        context = Pipe.getContext()
        with open(context.filePath, "r") as tangFile:
            data = json.load(tangFile)
            allCurrentReferences = data.get("assets", None)
        referencesInfosDict = {
            reference.split(":")[0]: allCurrentReferences[reference]["file_path"] for reference in allCurrentReferences
        }

        return referencesInfosDict
```
