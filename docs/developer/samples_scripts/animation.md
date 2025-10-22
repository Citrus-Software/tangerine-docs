---
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Animation

## List animated plugs, considering each anim layer

You can do several actions with python on curves objects and plugs.
Animation layers can be taken into consideration in code.
Here is a basic sample, getting the list of plugs that are animated in a scene.

Ask for more detail when needed.

```python
from tang_core.anim import find_anim_node
from tang_core.layer import former_plug_to_layer_plug, has_layer_plugs
from tang_core.callbacks import Callbacks
from tang_core.layer.layer import get_layers
from tang_core.document.get_document import get_document

def get_animated_plugs(plug, layers=[]):
    """Return a list of plug with animation, considering anim layers."""
    # get plug if animated, or get associated layers plugs instead if plug is connected to layers
    if has_layer_plugs(plug):
        animated_plugs = []
        for layer in layers:
            layer_plug = former_plug_to_layer_plug(plug, layer)
            if layer_plug:
                anim_node = find_anim_node(layer_plug)
                if anim_node:
                    animated_plugs.append(layer_plug)
        return animated_plugs
    else:
        anim_node = find_anim_node(plug)
        if anim_node:
            return [plug]
    return []

document = get_document()

ctrl_names = ["world", "move", "c_fly", "c_center", "c_camera_pos"] # filtering on nodes
attr_names = ["tx", "ty", "tz", "rx", "ry", "rz"] # filtering on attributs

# listing layers
layers = get_layers(document)

### parsing scene nodes to find plug with animation
root_node = document.root().find("YOUR_ROOT_NODE_NAME") # get this method definition
for ctrl in Callbacks().get_all_controllers_in_asset(root_node):
    # for plug in ctrl.get_plugs():
    #     print(plug.get_name())
    plugs = [plug for plug in ctrl.get_plugs() if plug.get_name() in attr_names]
    for plug in plugs:
        animated_plugs = get_animated_plugs(plug, layers=layers)
        for animated_plug in animated_plugs:
            anim_node = find_anim_node(animated_plug)
            print("node animated : %s.%s" %(anim_node.get_name(), animated_plug))
```
