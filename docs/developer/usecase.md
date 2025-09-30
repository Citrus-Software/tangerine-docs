---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Use case

## Exporting animation in Tangerine format to upload it in Tangerine

Tangerine uses `.action` files names to store animation and set values data.
You can write these files from another software and import it into Tangerine:
- Select the top node of an asset
- Use button `File > Load action on selected asset...`
- Choose the .action file containing animation on controls matching the selected asset controls

@seb @max c'est quoi la version simple de l'import de json action, juste ce qu'il y a derrière le bouton laod action on selected asset ^^ ?

### Uploding in Tangerine
Here is an example of a simple .action containing set values and animations curves on an asset.
Ask for a more advance sample to know about how to import constraints, dummies, and other animation types.

```python
def importAnimation(animDict=None, cstrDicts=None, offset=0):
    animDict = animDict or {}
    cstrDicts = cstrDicts or {}
    doc = get_document()

    modifierMessage = "pipeline : import asset animation"
    if offset:
        modifierMessage += " with offset %s" % offset
    with doc.modify(modifierMessage, undoable=Undoable.YES) as modifier:
        globalConstraintNode = get_shot_constraints(modifier=modifier)
        for cstrDict in cstrDicts:
            # remove asset constraint first
            controller = Callbacks().find_controller_in_asset(
                doc.root().find(cstrDict["constrained"]["asset"]), cstrDict["constrained"]["node_key"]
            )

            if controller and is_constrained(controller):
                constraint = get_constraint(controller)
                remove_shot_constraint(constraint, modifier)

            # only keep targets that exist in Tang
            constraintTargetsNodes = []
            for target in cstrDict["targets"]:
                targetNode = Callbacks().find_controller_in_asset(
                    doc.root().find(target["asset"]), target["node_key"]
                )
                if targetNode is not None:
                    constraintTargetsNodes.append(targetNode)

            constraintName = cstrDict["name"]
            existingConstraintName = [const.get_name() for const in shot_constraints(doc)]

            if constraintName in existingConstraintName:
                index = 1
                while (constraintName + str(index)) in existingConstraintName:
                    index += 1
                constraintName = constraintName + str(index)

            constraintAxes = TransformAxes(*cstrDict["axes"])
            constraintType = CONSTRAINT_TYPE_BY_NAME.get(cstrDict["type"].lower(), None)
            if not controller or not constraintTargetsNodes or not constraintType:
                continue
            # use tang api now instead of json interpretation to avoid refacto due to some tang changes
            add_shot_constraint(
                controller,
                constraintTargetsNodes,
                modifier,
                name=constraintName,
                axes=constraintAxes,
                add_key=False,
                constraint_type=constraintType,
                select=False,
            )
        for assetName, actionDict in animDict.items():
            node = doc.root().find(assetName)
            if node is not None:
                action = Action(node.get_name())
                constraintAction = Action("constraint_" + node.get_name())

                actionDict, constraintActionDict = extractConstraintActionFromAssetAction(
                    node.get_name(), actionDict, doc
                )
                action.init_from_json_dict(actionDict)
                constraintAction.init_from_json_dict(constraintActionDict)
                if offset:
                    action.apply(node, modifier, mode=Merge.replace_all_at_time, target_frame=offset)
                    constraintAction.apply(
                        globalConstraintNode, modifier, mode=Merge.replace_all_at_time, target_frame=offset
                    )
                else:
                    action.apply(node, modifier)
                    constraintAction.apply(globalConstraintNode, modifier)
            else:
                logger.info("Node %s not found to add action", assetName)
```
### Exporting .action from Maya simple animation
Animation with no deformations can be store easilly in a `.action` file using following dictionnary


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

You can now store this Tangerine compatible animation file into a `.action`
```python
import json

actionDict = {"values": {}, "anims": {}}
actionDict["anims"][keyName] = listValues

jsonFile = open(jsonPath, "w")
json.dump(actionDict, jsonFile, indent=4)
jsonFile.close()
```

## Build a Shot

You have the possibility to create a `Shot` object.
In this way, you can add every attribute needed directly this new object and save it to a file.
You skip the loading of data into Tangerine when not needed.

For exemple, if you want to generate every `.shot` of a sequence or an episode really fast, use this.

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
shot.add_asset("prop_n01_yuzu_logo:yuzu_logo", {"file_path": "E:/TEMP/tangerine/Tangerine Demo 2025/api_tests/yuzu_logo.tang"})
shot.add_asset("character_n01_jb:jb", {"file_path": "E:/TEMP/tangerine/Tangerine Demo 2025/api_tests/capy_jb.tang"})

# saving to a file
filePath = "E:/TEMP/tangerine/Tangerine Demo 2025/api_tests/built_shot.shot"
shot.export_file(filePath)

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


## Exporting usefull and optimise data for pipeline chain

### Bake abc for parts of asset for external software

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

### Add preroll postroll before to export

Some post treatments will need a preroll and postroll into the alembic file.

In the export command, you can choos a framerange that is different that document' framerange.
[See bake documentation.](api#export-to-alembic)
```python
frameRangeParams = {"start_frame": -20, "end_frame":50}

bake(
    filename=outputPathLocal,
    exclude_tag="do_not_bake",
    included_spline_tag="do_bake",
    roots=nodes,
    write_uv=True,
    document=document,
    sub_samples=subsamples,
    write_full_matrix=writeFullMatrix,
    **frameRangeParams
)
```
Usually, you will need to add keys on these preroll part to ensure positions for physical engines for example.
You can change the range for your document editing document.startFrame and document.endFrame.
If your animation is already validated, and includes dynamic, the dynamic is calculating depending on the first frame of the document.
Changing the range would edit it.
You can bake this dynamic before to export.

```python
from tang_core.callbacks import Callbacks
from tang_core.document.get_document import get_document
from gemini.meta_nodal.lib import dynamic @seb c'est le nom gemini ? comme dans les logs

dynamicControllers = []

document = get_document()

for assetNode in document.root().get_children():
    if not Callbacks().is_asset_node(document, assetNode):
        continue
    dynamicControllers += dynamic.filter_dynamic_controllers(
        Callbacks().get_all_controllers_in_asset(assetNode)
    )

alreadyBakedControllers = dynamic.filter_baked_dynamic_controllers(dynamicControllers)
dynamicControllers = [n for n in dynamicControllers if n not in alreadyBakedControllers]

if dynamicControllers:
    dynamic.bake_dynamic_controllers(dynamicControllers, document)
```

### Merging efficiently in maya for production chain
To be as efficient as possible, it is sense to seperate steps as much as possible, to reduce dependencies between steps.
For example, the surfacing and uvs for rendering are not linked to animation (except feature animation of uvs).
Here is a workflow to keep it independant, getting into maya the "renderable" version of an asset (uvs,shaders) and merging in a certain way into maya an alembic file from Tangerine.


# Playblasting options

## add HUD on image
Use a post process to add HUD on your images as you need.
Possibility to have a sample if needed.

# Callback processes

You will be able to add code overrides quite easily, using menu's button or scripts path in command line.

## Add custom code around manual actions
When you want to add code after a manually launched action from UI:
- Change the Menu button to put yours instead of native one [(see here).](general#custom-menus)
- Add your code around the basic called action.

Here are the code called behind default buttons.

@seb @max j'ai besoin du code des boutons
"File > Load Shot" : ``
"File > Save Shot" : ``
"File > New" : ``
"Playblast > With playblast Settings > Persp" : ``

## Add custom code around loading actions
When you want to inject some code in between Tangerine loading actions, use command line with script path to execute.
This script path should contain the algorithm that will draw your order of actions.
You can send to this script args, just adding the args after the script path.
Tangerine will skip it not understanding these args.
Please find the command line documentation, and an example in the demo package.


<details>
  <summary>Demo package command</summary>

    ```
    "C:\Program Files\TeamTO\Tangerine\1.7.14\TangerineConsole.exe" --log_to_file --kernel release --no-gui -l debug "E:/TEMP/tangerine/Tangerine Demo 2025/hook.py" E:\work\sandbox\tang-docs\docs\runTangContainerBatch.py --firstarg --secondarg 42 --filePath "E:\TEMP\tangerine\Tangerine Demo 2025\api_tests\three_capy.shot"
    ```

    <details>
      <summary> Sample code for script with args</summary>

        ```
        # -*- coding: utf-8 -*-
        import os
        import sys

        try:
            from PySide2.QtWidgets import QApplication
        except ImportError:
            print("Tang modules not loaded")


        args = {}
        for element in " ".join(sys.argv).split(" --"):
            if not element.count(" ") >= 1:
                args[element.split(" ")[0]] = True
            else:
                args[element.split(" ")[0]] = " ".join(element.split(" ")[1:])


        firstArg = args.get("[firstarg]", None)
        secondarg = args.get("[secondarg]", None)
        filePath = args.get("filePath", None)


        # Develop here depending on your needs and args. Sample opening a document and printing a list of top nodes.

        # opening filepath
        from tang_core.document.shot import Shot
        from tang_core.document.get_document import get_document

        document = get_document()
        Shot.import_shot_files([filePath], document)

        # listing top nodes and printing nodes full name
        nodes = document.root().get_children()
        for node in nodes:
            print(node.get_full_name())

        # to match a pipeline idea, could be opening > playblasting > exporting > saving in another location
        ```
    </details>
</details>

# Manipulating .tang files using Json's python library
Across a production, you could need several times to
- update a plug value for an asset, that is use in hundreds of shots
- Check which shots use a controller to evaluate the cost of this controller to be modified
- Change start frame or end frame of several shots

Tang files are json readable file and you will be able to search into data just using json python library.

<Tabs>
  <TabItem value="List references" label="List references" default>
    ```python
    # -*- coding: utf-8 -*-
    import json

    filePath = "E:/TEMP/tangerine/Tangerine Demo 2025/api_tests/three_capy.shot"

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

    filePath = "E:/TEMP/tangerine/Tangerine Demo 2025/api_tests/three_capy.shot"

    with open(filePath, "r") as sceneFile:
        animFile = json.load(sceneFile)

    animFile = checkAnimationOnMikanVisibility(animFile)
    ```
  </TabItem>
</Tabs>
