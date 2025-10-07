---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Edit tang file with Json library

During production, you may need to:
- Update a plug value for an asset that is used in hundreds of shots.
- Check which shots use a specific controller to evaluate the cost of modifying it.
- Change the start or end frame of multiple shots.

`.tang` files are JSON-readable, so you can search and manipulate their data using Python's built-in `json` library.

<Tabs>
  <TabItem value="List references" label="List references" default>
    ```python
    # -*- coding: utf-8 -*-
    import json

    filePath = "E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/three_capy.shot"

    with open(filePath, "r") as tangFile:
        data = json.load(tangFile)
        allCurrentReferences = data.get("assets", None)
    referencesInfosDict = {
        reference.split(":")[0]: allCurrentReferences[reference]["file_path"] for reference in allCurrentReferences
    }

    print("\n".join("%s : %s" % (k, v) for k, v in referencesInfosDict.items()))
    ```
  </TabItem>
  <TabItem value="Get Plug values" label="Get plug values" default>
    ```python
    # -*- coding: utf-8 -*-
    import json

    def checkAnimationOnMikanVisibility(animFile):

        control = "world"
        plug = "mikan_vis"
        for asset in animFile["assets"]:
            # searching in animation curves if this plug has data
            plugAnimCurve = animFile["assets"][asset].get("action", []).get("anims", []).get("%s.%s" % (control, plug), [])
            if plugAnimCurve:
                # parsing anim curve values
                for keyData in plugAnimCurve:
                    print("%s key on %s at time %s" % (asset + "." + control + "." + plug, keyData[1], keyData[0]))
            else:
                # searching if their is a static value for this plug set
                plugStaticValue = animFile["assets"][asset].get("action", []).get("values", []).get("%s.%s" % (control, plug), [])
                if plugStaticValue:
                    print("%s visibility set to %s " % (asset + "." + control + "." + plug, plugStaticValue))

    filePath = "E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/three_capy.shot"

    with open(filePath, "r") as sceneFile:
        animFile = json.load(sceneFile)

    animFile = checkAnimationOnMikanVisibility(animFile)
    ```
  </TabItem>
</Tabs>
