---
sidebar_position: 4
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Layout shot creation

In your Pipeline, you could be interested into getting your layout positions and posing directly into Tangerine.
To do so, you can create an `.action` file that describes positions of controls of each asset. This file is then imported in Tangerine using following code sample.

## Exporting Animation to load it into Tangerine

Animations without deformations can be easily stored in a `.action` file.

Sample code to export a Maya animation to Tangerine.
In this sample, you will find a basic animation. To have more infos about possible bridges, [please contact us](https://www.citrus-software.com/).

<Tabs>
  <TabItem value="from Maya to Tangerine" label="from Maya to Tangerine" default>

    ```python
    from math import cos, sin, radians

    plugRequired = "%s.%s" % (node, attribut)

    # We force conversion to weightedTangent because we need the exact wheight to give a norm to the Tang tangent
    cmds.keyTangent(plugRequired, e=1, weightedTangents=1)

    listValues = []
    times = cmds.keyframe(plugRequired, q=1)
    values = cmds.keyframe(plugRequired, q=1, valueChange=1)

    # since auto and spline mode can be slighlty different between tang and maya we convert these tangents
    # to custom to have the same shape
    tangentsITT = cmds.keyTangent(plugRequired, itt=1, q=1)
    tangentsOTT = cmds.keyTangent(plugRequired, ott=1, q=1)
    conv_type = ("auto", "spline", "plateau", "fixed")
    conv_in_tangent_index = [(i,) for i, itt in enumerate(tangentsITT) if itt in conv_type]
    conv_out_tangent_index = [(i,) for i, ott in enumerate(tangentsOTT) if ott in conv_type]
    cmds.keyTangent(plugRequired, e=1, itt="fixed", index=conv_in_tangent_index)
    cmds.keyTangent(plugRequired, e=1, ott="fixed", index=conv_out_tangent_index)

    tangentsIA = cmds.keyTangent(plugRequired, ia=1, q=1)
    tangentsOA = cmds.keyTangent(plugRequired, oa=1, q=1)
    tangentsInWeight = cmds.keyTangent(plugRequired, inWeight=1, q=1)
    tangentsOutWeight = cmds.keyTangent(plugRequired, outWeight=1, q=1)
    tangentsITT = cmds.keyTangent(plugRequired, itt=1, q=1)  # get a new once with converted type
    tangentsOTT = cmds.keyTangent(plugRequired, ott=1, q=1)  # get a new once with converted type

    # to take into consideration tangeant coeff are independant from eachother, or linked
    weightLocks = cmds.keyTangent(plugRequired, q=1, l=1)
    tangentsRatioOIT = 0.333333333  # no matter value, will be recompute in tang
    tangentsRatioOTT = 0.333333333  # no matter value, will be recompute in tang

    modeValueDict = {"linear": 0, "auto": 1, "custom": 2, "spline": 3, "flat": 4, "step": 5, "plateau": 1}

    for t in range(len(times)):
        keyTime = times[t]
        value = values[t]
        weightLock = float(weightLocks[t])
        if not animCurve:
            if (
                cmds.attributeQuery(attribut, node=node, attributeType=True) == "enum"
                or cmds.attributeQuery(attribut, node=node, attributeType=True) == "long"
            ):
                value = int(value)
            if cmds.attributeQuery(attribut, node=node, attributeType=True) == "bool":
                value = bool(value)

        if not type(value) is float:
            # do not need tangeant infos
            listValues.append(
                [keyTime, value]
            )  # inverse regarding float curve value (under) because developped like that in tang
            continue

        itt = tangentsITT[t]
        ott = tangentsOTT[t]
        left_tangent_mode = modeValueDict.get(itt, 2)
        right_tangent_mode = modeValueDict.get(ott, 2)

        ia = tangentsIA[t]
        oa = tangentsOA[t]
        inweight = tangentsInWeight[t]
        outweight = tangentsOutWeight[t]

        input_angle = radians(float(ia) + 180.0)
        output_angle = radians(float(oa))
        input_weight = inweight
        output_weight = outweight

        dxl = input_weight * round(cos(input_angle), 6)
        dyl = input_weight * round(sin(input_angle), 6)

        dxr = output_weight * round(cos(output_angle), 6)
        dyr = output_weight * round(sin(output_angle), 6)

        listValues.append(
            [
                value,
                keyTime,
                dxl,
                dyl,
                dxr,
                dyr,
                left_tangent_mode,
                right_tangent_mode,
                tangentsRatioOIT,
                tangentsRatioOTT,
                weightLock,
            ]
        )
    ```
  </TabItem>
</Tabs>

You can now store this Tangerine compatible animation dictionnaryle into a `.action`
```python
import json

actionDict = {"values": {}, "anims": {}}
actionDict["anims"][keyName] = listValues

jsonFile = open(jsonPath, "w")
json.dump(actionDict, jsonFile, indent=4)
jsonFile.close()
```

### Uploading in Tangerine

Find a sample of an `.action` file in the demo package. This file contains set values and animation curves for an asset.
For more advanced examples, including importing constraints, dummies, and other animation types, [ask for further guidance](https://www.citrus-software.com/).

```python

file_path = "E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/maya_layout/character_n01_jb.action"
action = Action("my_action")
action.load(file_path)
with get_document().modify('Apply Action') as modifier:
    action.apply(asset_node, modifier)
```

