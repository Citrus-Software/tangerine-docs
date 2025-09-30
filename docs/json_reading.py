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
