from math import cos, sin, radians
import json
import random

def get_transform_attributes(node_name):
    """Get the transform attributes list for a node.
    This function return an empty list if the node is not a transform node.
    Will list only usable attributes (input cant be modified, not linked by other node).
    param node_name: string, The name of the node
    return: list, list of attributes short names
    """
    transform_attributes = []
    nodes = cmds.ls(node_name, exactType="transform") + cmds.ls(node_name, exactType="joint")

    if not nodes:
        return transform_attributes

    for attribute in ("t", "r", "s"):
        for dimension in ("x", "y", "z"):
            attribute_name = node_name + "." + attribute + dimension
            if cmds.getAttr(attribute_name, lock=True):
                continue
            connections = cmds.listConnections(attribute_name, destination=False, source=True) or []
            for connection in connections:
                if not cmds.objectType(connection, isAType="animCurve"):
                    continue
            if not cmds.getAttr(attribute_name, keyable=True):
                continue
            transform_attributes.append(attribute + dimension)

    return transform_attributes


def get_anim_curve_values_list(node="", attribut="", anim_curve=""):
    """In tang, list of value is as following for a key
    [
        value, temps, tangente_gauche_x, tangente_gauche_y,
        tangente_droite_x, tangent_droite_y, tangente_gauche_mode,
        tangente_droite_mode, tangente_gauche_ratio,
        tangente_droite_ratio,
        break_tangent (1.0 ou 0.0 pour true/false)
    ]
    """
    curve_requested = ""
    if anim_curve:
        curve_requested = anim_curve
    elif node and attribut:
        curve_requested = "%s.%s" % (node, attribut)
    if not curve_requested:
        print("Missing argument in get_anim_curve_values_list")
        return []

    mode_value_dict = {"linear": 0, "auto": 1, "custom": 2, "spline": 3, "flat": 4, "step": 5, "plateau": 1}

    # We force conversion to weightedTangent because we need the exact wheight to give a norm to the Tang tangent
    cmds.keyTangent(curve_requested, e=1, weightedTangents=1)

    list_values = []
    times = cmds.keyframe(curve_requested, q=1)
    values = cmds.keyframe(curve_requested, q=1, valueChange=1)

    # since auto and spline mode can be slighlty different between tang and maya we convert these tangents
    # to custom to have the same shape
    tangents_itt = cmds.keyTangent(curve_requested, itt=1, q=1)
    tangents_ott = cmds.keyTangent(curve_requested, ott=1, q=1)
    conv_type = ("auto", "spline", "plateau", "fixed")
    conv_in_tangent_index = [(i,) for i, itt in enumerate(tangents_itt) if itt in conv_type]
    conv_out_tangent_index = [(i,) for i, ott in enumerate(tangents_ott) if ott in conv_type]
    cmds.keyTangent(curve_requested, e=1, itt="fixed", index=conv_in_tangent_index)
    cmds.keyTangent(curve_requested, e=1, ott="fixed", index=conv_out_tangent_index)

    tangents_ia = cmds.keyTangent(curve_requested, ia=1, q=1)
    tangents_oa = cmds.keyTangent(curve_requested, oa=1, q=1)
    tangents_in_weight = cmds.keyTangent(curve_requested, inWeight=1, q=1)
    tangents_out_weight = cmds.keyTangent(curve_requested, outWeight=1, q=1)
    tangents_itt = cmds.keyTangent(curve_requested, itt=1, q=1)  # get a new once with converted type
    tangents_ott = cmds.keyTangent(curve_requested, ott=1, q=1)  # get a new once with converted type

    # to take into consideration tangeant coeff are independant from eachother, or linked
    weight_locks = cmds.keyTangent(curve_requested, q=1, l=1)
    tangents_ratio_oit = 0.333333333  # no matter value, will be recompute in tang
    tangents_ratio_ott = 0.333333333  # no matter value, will be recompute in tang

    for t in range(len(times)):
        key_time = times[t]
        value = values[t]
        weight_lock = float(weight_locks[t])
        if not anim_curve:
            if (
                cmds.attributeQuery(attribut, node=node, attributeType=True) == "enum"
                or cmds.attributeQuery(attribut, node=node, attributeType=True) == "long"
            ):
                value = int(value)
            if cmds.attributeQuery(attribut, node=node, attributeType=True) == "bool":
                value = bool(value)

        if not type(value) is float:
            # do not need tangeant infos
            list_values.append(
                [key_time, value]
            )  # inverse regarding float curve value (under) because developped like that in tang
            continue

        itt = tangents_itt[t]
        ott = tangents_ott[t]
        left_tangent_mode = mode_value_dict.get(itt, 2)
        right_tangent_mode = mode_value_dict.get(ott, 2)

        ia = tangents_ia[t]
        oa = tangents_oa[t]
        inweight = tangents_in_weight[t]
        outweight = tangents_out_weight[t]

        input_angle = radians(float(ia) + 180.0)
        output_angle = radians(float(oa))
        input_weight = inweight
        output_weight = outweight

        dxl = input_weight * round(cos(input_angle), 6)
        dyl = input_weight * round(sin(input_angle), 6)

        dxr = output_weight * round(cos(output_angle), 6)
        dyr = output_weight * round(sin(output_angle), 6)

        list_values.append(
            [
                value,
                key_time,
                dxl,
                dyl,
                dxr,
                dyr,
                left_tangent_mode,
                right_tangent_mode,
                tangents_ratio_oit,
                tangents_ratio_ott,
                weight_lock,
            ]
        )

    return list_values

def get_anim_layers(layers_infos):
    layers = {}
    for layer in layers_infos:
        if layer == "BaseAnimation":
            continue
        color = ([random.random() for i in range(0, 4)])
        tang_name = layers_infos[layer]["name"]
        layers[tang_name] = {
            "nice_name": layer,
            "color": color,
            "plugs": layers_infos[layer]["plugs"],
            "action": {
                "values": {
                    "%s.enable" % tang_name: True,
                },
                "anims": {},
            },
        }
        weight_curves = cmds.listConnections("%s.weight" % layer, type="animCurve") or []
        if not weight_curves:
            layers[tang_name]["action"]["values"]["%s.weight" % tang_name] = cmds.getAttr("%s.weight" % layer)
        else:
            layers[tang_name]["action"]["anims"]["%s.weight" % tang_name] = self.get_anim_curve_values_list(
                anim_curve=weight_curves[0]
            )

        return layers

def store_animation_dict():
    """
    Store in json file tang animation et set attribute on controls defined with mikan attributes.
    One json file will be exported per asset (top node with gem attr asset) at
    sub folder "layout-animation" in work anim folder of shot.
    Some maya attribute could not exists in tang (or wont have the same name) and won't be intepretd.
    Json file exported can be loaded in tang as an action.
    """
    version_override = {}
    allAnimLayers = cmds.ls(type="animLayer")
    animLayersAssignementDict = {}
    layerIndex = 1
    for layer in allAnimLayers:
        if layer == "BaseAnimation":
            animLayersAssignementDict[layer] = {"name": "base", "plugs": []}
        else:
            animLayersAssignementDict[layer] = {"name": "Anim_Layer_%s" % str(layerIndex), "plugs": []}
            layerIndex += 1


    assetNodes = cmds.ls("|*:*", type="transform", l=True)
    for assetNode in assetNodes:
        actionDict = {"values": {}, "anims": {}}
        namespace = assetNode.split(":")[0].lstrip("|")

        ctrls = [
            x
            for x in cmds.listRelatives(assetNode, allDescendents=True, fullPath=True) or []
            if cmds.attributeQuery("gem_type", n=x, ex=True) and cmds.getAttr(x + ".gem_type") == "control"
        ]

        for ctrl in ctrls:
            # using long name cause only one name in tang, the long attribute's name
            userAttributes = cmds.listAttr(ctrl, userDefined=True)

            transformAttributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
            # customAttributes = getCustomAttributes(ctrl) # to code if needed
            attributes = transformAttributes # + customAttributes

            attribute = attributes[0]
            for attribute in attributes:
                ctrlName = ctrl #can be updated if there is pair blend
                attributeName = attribute #can be updated if there is pair blend

                if not cmds.attributeQuery(attributeName, n=ctrlName, ex=True):
                    # possibly, attribute has been removed for pairblend in for execution
                    continue

                # exception, for transform attributes in tang, we have equivalent of maya short attribute name
                attributeLongName = attributeName
                if any(attributeName.startswith(attrName) for attrName in ("rotate", "translate", "scale")):
                    attributeName = cmds.attributeQuery(attributeName, node=ctrlName, shortName=True)
                if attributeLongName == attributeName:
                    attributeLongName = cmds.attributeQuery(attributeName, node=ctrlName, longName=True)

                keyName = (
                    ctrlName.split(":")[-1] + "." + attributeName
                )  # no need namespace in tang cause loaded with model top node
                tangNamePrefix = ctrlName[1:].split("|")[0]

                # possible code to deal with contraints and pairblend nodes. Ask specifically if needed.

                # checking for anim curves on attributs
                animCurves = [
                    animCurve
                    for animCurve in cmds.listConnections(ctrlName + "." + attributeName, type="animCurve") or []
                    if not cmds.referenceQuery(animCurve, isNodeReferenced=True)
                ]

                blendAnimlayers = [
                    blendLayer
                    for blendLayer in cmds.listConnections(ctrlName + "." + attributeName, type="animBlendNodeAdditiveDL")
                    or []
                    if not cmds.referenceQuery(blendLayer, isNodeReferenced=True)
                ]

                if animCurves:
                    curvValuesList = getAnimCurveValuesList(node=ctrlName, attribut=attributeName)
                    actionDict["anims"][keyName] = curvValuesList
                elif blendAnimlayers:
                    for aLayer in allAnimLayers:
                        layeredCurve = cmds.animLayer(aLayer, fcv="%s.%s" % (ctrl, attribute), q=True)
                        if layeredCurve:
                            animLayersAssignementDict[aLayer]["plugs"].append("%s.%s" % (tangNamePrefix, keyName))
                            curvValuesList = getAnimCurveValuesList(animCurve=layeredCurve)
                            actionDict["anims"][
                                "%s_%s" % (keyName, animLayersAssignementDict[aLayer]["name"])
                            ] = curvValuesList
                elif not cmds.attributeQuery(attributeName, node=ctrlName, multi=True):  # for no multi attributes
                    # message has no data to get
                    if cmds.attributeQuery(attributeName, node=ctrlName, attributeType=True) == "message":
                        continue

                    value = cmds.getAttr(ctrlName + "." + attributeName)

                    if cmds.attributeQuery(attributeName, node=ctrlName, attributeType=True) == "enum":
                        value = int(value)

                    actionDict["values"][keyName] = value
                else:
                    multiAttributes = cmds.listAttr(ctrlName + "." + attributeName, multi=True)
                    # TODO : Do recursive
                    actionDict["values"][keyName] = {
                        multiAttribute: cmds.getAttr(ctrlName + "." + multiAttribute)
                        for multiAttribute in multiAttributes
                        if cmds.attributeQuery(multiAttribute, node=ctrlName, attributeType=True) != "message"
                    }
        jsonPath = os.path.join("E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/maya_layout/%s.action" % namespace)

        if actionDict:
            jsonFile = open(jsonPath, "w")
            json.dump(actionDict, jsonFile, indent=4)
            jsonFile.close()

    if animLayersAssignementDict:
        jsonLayerPath = os.path.join("E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/maya_layout/%s_layer.action" % namespace)
        layersDict = getAnimLayers(animLayersAssignementDict)
        jsonFile = open(jsonLayerPath, "w")
        json.dump(layersDict, jsonFile, indent=4)
        jsonFile.close()
        print("JSON file created at %s", jsonLayerPath)
