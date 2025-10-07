---
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Nodes

@max @seb ajouter text, un peu de verbose ici
### Get Asset Nodes from selection

```python
from tang_core.document.get_document import get_document
from tang_core.asset.asset import Asset
from meta_nodal_py import SceneGraphNode

document = get_document()

nodes = []

for node in document.node_selection():
    if type(node) == SceneGraphNode and Asset.is_asset(node.get_name()) and Asset.is_asset_loaded(node):
        nodes.append(node)

nodeDict = {node.get_name(): node for node in nodes}
print(nodeDict.keys())
```
### Access Nodes, Controllers, and Plugs

You can manipulate nodes within your scene.
Some nodes have special functions, such as Asset nodes. These specific nodes are defined as the main nodes of a referenced asset by `Mikan`.

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>

  Be sure this script is a startup script, so UI will update at the end only once.
  If not, use a modifier for your creation nodes @sixtine
```python
from tang_core.callbacks import Callbacks
from tang_core.document.get_document import get_document
import meta_nodal_py as kl

# get a root node
document = get_document()
rootNodeName = "[name_of_a_root_node]" # this is the name of a root node
assetNode = document.root().find(rootNodeName) # finding your node

# create a node
trash = kl.SceneGraphNode(document.root(), "trash")

# delete a node
trash.remove_from_parent()
del trash

# list children
children = assetNode.get_children()
for child in children:
    print(child.get_full_name())

# hide a node
assetNode.show.set_value(False)

# get a controller in asset hierarchy, using Mikan Callbacks
ctrl = "CONTROL_NAME" #
node = Callbacks().find_controller_in_asset(assetNode, ctrl)

# Plugs
# list plugs of a node
plugs = node.get_plugs()

# get a plug on node
attribute = "NAME_OF_ATTRIBUTE"
plug = node.get_plug(attribute)
```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">

```python
from tang_core.callbacks import Callbacks
from tang_core.document.get_document import get_document
from PySide2.QtWidgets import QApplication
from tang_core.asset.asset_load_mode import AssetLoadMode
import meta_nodal_py as kl

# opening scene
DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"
filePath = DEMO_FOLDER_PATH + "/api_samples/three_capy.shot" # shot file
app = QApplication.instance()
tangLoadMode = AssetLoadMode.ALL
app.main_window.import_shot_files([filePath], load_mode=tangLoadMode)

document = get_document()

# create a node
trash = kl.SceneGraphNode(document.root(), "trash")

# delete a node
trash.remove_from_parent()
del trash

# get a root node
rootNodeName = "character_n01_jb:jb" # this is the name of a root node
assetNode = document.root().find(rootNodeName) # finding your node

# list children
children = assetNode.get_children()
for child in children:
    print(child.get_full_name())

# hide a node
assetNode.show.set_value(False)

# get a controller in asset hierarchy
ctrl = "move" # name of a controler you are searching for
ctrlNode = Callbacks().find_controller_in_asset(assetNode, ctrl)

# Plugs
# list plugs
nodePlugs = ctrlNode.get_dynamic_plugs()
for plug in nodePlugs:
    print("%s.%s" % (ctrlNode, plug.get_name()))

# get a specific attribut plug
attribute = "tx"
plug = ctrlNode.get_plug(attribute)

print(plug.get_full_name())

```
  </TabItem>
</Tabs>
