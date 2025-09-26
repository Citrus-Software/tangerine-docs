# -*- coding: utf-8 -*-

import os
import sys
import platform
import imp

if "teamto" not in sys.modules or "srv-bin/scripts/modules" not in sys.modules["teamto"].__path__[0]:
    baseDir = "/mnt/" if platform.os.name == "posix" else "//"
    sys.path.append(baseDir + "srv-bin/scripts/modules")

import teamto.ttImport

from jad_pipe.core.pipe import Pipe
from jad_pipe.core.context import Context
from jad_pipe.logger import logger

try:
    from PySide2.QtWidgets import QApplication
except ImportError:
    logger.info("Tang modules not loaded")


args = {}
for element in " ".join(sys.argv).split(" --"):
    if not element.count(" ") >= 1:
        args[element.split(" ")[0]] = True
    else:
        args[element.split(" ")[0]] = " ".join(element.split(" ")[1:])


def runContainer(actionType, args):
    context = Pipe.getContext()

    if actionType == "Export":
        # If .abc files are about to be exported outside the standard publishing process (case of .abc files exported
        # from the work scene for occlusion pass purposes)
        if args.count("withPublishAnimActions=True"):
            runResult = eval("Pipe.get(context.containerName).PublishAnimActions.run()")
            args = args.replace("withPublishAnimActions=True,", "").strip(" ,")

    elif actionType == "Playblast":
        # At playblast, we don't ant to override context, we want to keep given version of scene path
        # At build, for exemple, we want to have different behaviour, nevermind the given version the build will take v000
        if not args.count("forceUpdateContext"):
            args = args + ",forceUpdateContext=False" if args else "forceUpdateContext=False"

    logger.info("python > eval(Pipe.get(context.containerName)." + actionType + ".run(" + args + "))")
    runResult = eval("Pipe.get(context.containerName)." + actionType + ".run(" + args + ")")
    if actionType == "Playblast":
        container = Pipe.get(context.containerName)
        versionOverride = None
        if args:
            for arg in args.split(","):
                if arg.startswith("version="):
                    versionOverride = arg.split("=")[1]

        imgPath = container.Playblast.image_path
        if versionOverride:
            imgPath = imgPath.replace("v001", "v%s" % versionOverride)

        container.Playblast.postRender(imageDir=os.path.dirname(imgPath) + "/")


contextPath = args.get("contextPath", None)
filePath = args.get("filePath", None)
actionName = args.get("actionName", None)
actionArgs = args.get("actionArgs", "")
scriptArg = args.get("script", None)

# runResult = Pipe.get(context.containerName)." + $actionType + ".run(" + $args + ")

if contextPath is not None:
    context = Context.initFromPath(contextPath)
    Pipe.setContext(context)
elif filePath is not None:
    # filePath = Context.getCurrentFilePath()
    # context = Context.initFromPath(filePath)
    soft = Pipe.getSoft(Context.getSoftware())
    soft.open(filePath)

runContainer(actionName, actionArgs)

if scriptArg is not None:
    import imp

    modulesName = os.path.splitext(os.path.basename(scriptArg))[0]

    fp, pathname, description = imp.find_module(modulesName, [os.path.dirname(scriptArg)])
    script = imp.load_module(modulesName, fp, pathname, description)
    script.main()
