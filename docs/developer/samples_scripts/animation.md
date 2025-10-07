---
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Animation

## List animated plugs, considering each anim layer

<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
    ```python
    ```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">
    ```python
    from tang_core.anim import find_anim_node
    from tang_core.layer import former_plug_to_layer_plug, has_layer_plugs
    from tang_core.callbacks import Callbacks

    def getAnimatedPlugs(plug)
        """Return a list of plug with animation, considering anim layers."""
        # get plug if animated, or get associated layers plugs instead if plug is connected to layers
        if has_layer_plugs(plug):
            animatedPlugs = []
            for layer in layers:
                layer_plug = former_plug_to_layer_plug(plug, layer)
                if layer_plug:
                    anim_node = find_anim_node(layer_plug)
                    if anim_node:
                        animatedPlugs.append(layer_plug)
            return animatedPlugs
        else:
            anim_node = find_anim_node(plug)
            if anim_node:
                return [plug]
        return []

    ctrlNames = ["world", "move", "c_fly", "c_center", "c_camera_pos"] # filtering on nodes
    attrNames = ["tx", "ty", "tz", "rx", "ry", "rz"] # filtering on attributs

    ### parsing scene nodes to find plug with animation
    rootNodes = getRootNodes(assetType=True) # get this method definition
    for rootNode in rootNodes:
        for ctrl in Callbacks().get_all_controllers_in_asset(rootNode):
            plugs = [plug for plug in ctrl.get_plugs() if plug.get_name() in attrNames]
            for plug in plugs:
                animatedPlugs = soft.getAnimatedPlugs(plug, layers=layers)
                for animatedPlug in animatedPlugs:
                    anim_node = find_anim_node(animatedPlug)
    ```
  </TabItem>
</Tabs>
