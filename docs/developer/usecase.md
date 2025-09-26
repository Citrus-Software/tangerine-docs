---
sidebar_position: 3
---
# Use case

## creating a shot file outside Tangerine

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
## reading info in .shot files with json library

## Build shot
### option 1
```python
from tang_core.document.shot import Shot

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


## Exporting usefull and optimise data for pipeline chain


### Bake abc for parts of asset for extyernal software


```python
from tang_core.document.get_document import get_document

def setBakeTagOnNode(bake, node, tagger=None):
    """Helper function to set the :param node: tags "do_bake" and "do_not_bake" according to the :param bakable:
    Perform tag existence check before tagging or untagging.
    if you intend to use this method on a lot of nodes, please provide a tagger with the tags "do_bake" and
        "do_not bake" already created, for performance reasons.

    :param bake: Wether the node shall be tagged bakable or not.
    :type bake: bool
    :param node: Tangerine node instance to change tags
    :type node: Node
    :param tagger: Tagger instance to avoid create a new one each time, defaults to None
    :type tagger: Tagger, Optional
    """

    if not tagger:
        tagger = get_document().tagger
        tagger.create_tag("do_not_bake", show_in_gui=False)
        tagger.create_tag("do_bake", show_in_gui=False)

    if bake:
        if not tagger.has_tag("do_bake", node):
            tagger.tag_node("do_bake", node)
        if tagger.has_tag("do_not_bake", node):
            tagger.untag_node("do_not_bake", node)
    else:
        if tagger.has_tag("do_bake", node):
            tagger.untag_node("do_bake", node)
        if not tagger.has_tag("do_not_bake", node):
            tagger.tag_node("do_not_bake", node)
```
### Add preroll postrool before to export

## update your surfacing without editin abc

# Playblasting options
## add HUD on image

# Callback processes
## Activating actions after saving a document
## Activating actions after loading a document

# Manipulating .tang files
Across a production, you could need several times to
- update a plug value for an asset, that is use in hundreds of shots
- Check which shots use a controller to evaluate the cost of this controller to be modified
- Change start frame or end frame of several shots

