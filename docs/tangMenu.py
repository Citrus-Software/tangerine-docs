# -*- coding: utf-8 -*-

import sys
import os
import imp
import copy

from opensave.osMainWindow import OSMainWindow

from jad_pipe.core.pipe import Pipe
from jad_pipe.core.context import Context
from jad_pipe.ui.dialogs import showMessage, selectAction, validationUi, suggestSaveUi
from jad_pipe.tools.reUseManager.reUseManager import ReUseManager
from jad_pipe.ui.tangUI.occlusionLauncherUI import OcclusionLauncherUI
from jad_pipe.core.pipeReader import PipeReader
from jad_pipe.logger import logger

try:
    from PySide2.QtWidgets import QApplication, QMessageBox
    from tang_gui.tang_action import add_action
    from tang_core.document.get_document import get_document
    from tang_core.asset.asset import Asset
    from tang_core.asset.asset_loader import AssetLoader

    osWindow = OSMainWindow(parent=QApplication.instance().main_window, mode="Open", software="tang")
    from tang_gui.get_tang_window import get_tang_window
except ImportError:
    logger.info("Couldn't import tang modules")


class RollbackImporter(object):
    dependencies = list()

    def __init__(self, _filter=None):
        self.filter = _filter
        self.previousModules = sys.modules.copy()
        if _filter:
            for module in sys.modules.keys():
                if _filter in module:
                    self.previousModules.pop(module)

    def rollback(self):
        # force reload when modname next imported
        for module in set(sys.modules).difference(set(self.previousModules)):
            if self.filter:
                if self.filter not in module:
                    continue
            if module.startswith("raven"):
                continue
            if module in sys.modules:
                if sys.modules[module]:
                    print("reload %s" % sys.modules[module])
                sys.modules.pop(module)

        # clean sys.modules dict
        for module in sys.modules.keys():
            if not sys.modules[module]:
                sys.modules.pop(module)

        # delete registered UI
        for win in self.dependencies:
            try:
                win.delete()
            except Exception:
                pass

        RollbackImporter.dependencies = list()

    @classmethod
    def registerDependency(cls, win):
        cls.dependencies.append(win)
        print("#registered %s" % win)


def setPipelineMenu():
    """
    Add Production menu UI and Pipeline action in File menu (ex: Pipeline Publish, Pipeline SaveIncr, etc)
    """
    app = QApplication.instance()
    doc = get_document()

    manager = doc.shortcuts_manager

    # Pipeline Actions
    manager.start_register_block()

    # File Menu
    tangMenuBar = app.main_window.menuBar()
    mainMenuActions = tangMenuBar.actions()

    fileMenu = None
    for action in mainMenuActions:
        if action.text() == "File":
            if os.getenv("TT_DEVSTEP") is not None and os.getenv("TT_DEVSTEP") != "release":
                action.setText("File (%s)" % os.getenv("TT_DEVSTEP"))
            fileMenu = action.parent()
            break

    playblastMenu = None
    for action in mainMenuActions:
        if action.text() == "Playblast":
            playblastMenu = action.parent()
            break

    if fileMenu is None:
        logger.info("File menu not found")
        return

    actionFileMenu = fileMenu.actions()

    # New
    pipelineNew = add_action(app.main_window, "Pipeline Build...", buildFile, shortcut="Ctrl+B")
    # pipelineNew.setText('Pipeline New...')
    fileMenu.insertAction(actionFileMenu[0], pipelineNew)

    # Open
    pipelineOpen = add_action(app.main_window, "Pipeline Open", openFile, shortcut="Ctrl+O", override=True)
    pipelineOpen.setText("Pipeline Open...")
    fileMenu.insertAction(actionFileMenu[0], pipelineOpen)

    # # Save
    pipelineSave = add_action(app.main_window, "Pipeline Save", saveFile, shortcut="Ctrl+S", override=True)
    pipelineSave.setText("Pipeline Save")
    fileMenu.insertAction(actionFileMenu[0], pipelineSave)

    # # Save
    pipelineSave = add_action(app.main_window, "Pipeline Save as", saveAsFile, shortcut="Ctrl+S+Shift", override=True)
    pipelineSave.setText("Pipeline Save As")
    fileMenu.insertAction(actionFileMenu[0], pipelineSave)

    # Publish
    pipelineCheckPublishability = add_action(app.main_window, "Pipeline Check Publishability", checkPublishability)
    pipelineCheckPublishability.setText("Pipeline Check Publishability")
    fileMenu.insertAction(actionFileMenu[0], pipelineCheckPublishability)

    # Publish
    pipelinePublish = add_action(app.main_window, "Pipeline Publish", publish)
    pipelinePublish.setText("Pipeline Publish")
    fileMenu.insertAction(actionFileMenu[0], pipelinePublish)

    fileMenu.insertSeparator(actionFileMenu[0])

    # ## Playblast Menu
    playblastsActions = playblastMenu.actions()

    # Playblast Server
    pipelinePlayblastServer = add_action(app.main_window, "Pipeline Playblast Server", playblastServer)
    playblastMenu.insertAction(playblastsActions[0], pipelinePlayblastServer)

    # Playblast Deported
    pipelinePlayblastDeported = add_action(app.main_window, "Pipeline Playblast Deported", playblastDeported)
    playblastMenu.insertAction(playblastsActions[0], pipelinePlayblastDeported)

    # PROD Menu
    productionMenu = tangMenuBar.addMenu(os.getenv("TT_PROD_NAME"))
    # refresh file references
    refreshReferencesAction = add_action(app.main_window, "Refresh breakdown references", refreshReferences)
    refreshReferencesAction.setText("Refresh breakdown references")
    productionMenu.insertAction(None, refreshReferencesAction)

    if os.getenv("TT_PROD_NAME") == "city-of-ghosts":
        refreshLayoutBackground = add_action(app.main_window, "Refresh background from layout", refreshBackground)
        refreshLayoutBackground.setText("Refresh background from layout")
        productionMenu.insertAction(None, refreshLayoutBackground)

    refreshAnimFromLayoutButton = add_action(
        app.main_window, "Refresh selected assets anim from layout", refreshAnimFromLayout
    )
    refreshAnimFromLayoutButton.setText("Refresh selected assets anim from layout")
    productionMenu.insertAction(None, refreshAnimFromLayoutButton)

    getCamFromSceneButton = add_action(app.main_window, "Get cameras from scene", getCamFromScene)
    getCamFromSceneButton.setText("Get the camera previously exported")
    productionMenu.insertAction(None, getCamFromSceneButton)

    animateCheckAssetShotAction = add_action(
        app.main_window, "Animate check-models shot's assets", animateCheckAssetShot
    )
    animateCheckAssetShotAction.setText("Animate check-models shot's assets")
    productionMenu.insertAction(None, animateCheckAssetShotAction)

    launchOcclusionButton = add_action(app.main_window, "Launch occlusion", launchOcclusion)
    launchOcclusionButton.setText("Launch occlusion job to farm")
    productionMenu.insertAction(None, launchOcclusionButton)

    reUseManagerButton = add_action(app.main_window, "ReUse Manager", launchReUseManager)
    reUseManagerButton.setText("Launch ReUse manager menu")
    productionMenu.insertAction(None, reUseManagerButton)

    sys.path.append("//srv-bin/bin/tang/menu")
    import tangTTMenu

    tangTTMenu.create_menu()

    # ## Dev Menu
    assetManager = Pipe.getAssetManager()
    if assetManager.isCurrentUserInOvmGroupbyName(groupList=["pipeline"]):
        helpMenu = tangMenuBar.addMenu("dev_menu")
        devsActions = helpMenu.actions()
        # Reload script
        pipelineReloadScripts = add_action(
            app.main_window, "Reload Scripts", reloadScripts, shortcut="F5", override=True
        )
        pipelineReloadScripts.setText("Reload Scripts")
        helpMenu.insertAction(devsActions[0] if devsActions else None, pipelineReloadScripts)

    # TODO add separator end of menu

    manager.end_register_block()


def createMenu(app):
    """Overwrite Classic tang menu names and add Pipeline actions and menus"""
    menu_bar = app.main_window.menuBar()
    mainMenuActions = menu_bar.actions()

    # Rename classic actions
    for actionButton in mainMenuActions:
        if actionButton.text() == "New...":
            actionButton.setText("Classic New...")
        if actionButton.text() == "Load...":
            actionButton.setText("Classic Open...")
        if actionButton.text() == "Save":
            actionButton.setText("Classic Save")
        if actionButton.text() == "Save As...":
            actionButton.setText("Classic Save As...")

    # set pipeline actions
    setPipelineMenu()


def openFile():
    """Launch Opensave to select file and open it"""
    userSelect = suggestSaveWhenDirty()
    if userSelect == "Cancel":
        return
    osWindow.openFile()


def playblastServer():
    doc = get_document()

    # Check that all assets are loaded before launching playblast.
    # Show dialog to continue or cancel playblast.
    unloadedAssets = list(Asset.unloaded_assets(doc))
    if unloadedAssets:
        proceed = validationUi(
            "All assets will be loaded before launching the playblast. This will take some time.",
            "Do you want to continue ?",
            title="Load assets before playblast",
        )
        if not proceed:
            return

        AssetLoader.load_all_unloaded_assets()
    else:
        proceed = validationUi(
            "You're about to launch a playblast. This may imply some performance issue.",
            "Do you want to continue ?",
            title="Proceed with playblast",
        )
        if not proceed:
            return

    context = Pipe.getContext()
    stepContainer = Pipe.get(context.containerName)
    stepContainer.Playblast.run(forceUpdateContext=False)
    stepContainer.Playblast.postRender(imageDir=os.path.dirname(stepContainer.Playblast.image_path) + "/")

    if Pipe.get("PlayblastPreroll") is not None and context.shot["ovm_dynamicInfos"].get(
        "needed-dynamic-by-model", {}
    ).get("cloth", {}):
        stepContainer.PlayblastPreroll.run(mode="deported", forceUpdateContext=False)

    if Pipe.get("PlayblastInterframe"):
        stepContainer.PlayblastInterframe.run(mode="deported", forceUpdateContext=False)


def playblastDeported():
    # @Guard: only on site valence
    site = os.getenv("TEAMTO_NETWORK")
    if site == "PARIS":
        showMessage("Deported playblast must be sent from valence.", "Playblast Aborted")
        return

    message = "Please select an action for Playblasting"
    action = selectAction(message, action1="currentShot", action2="select another shot")
    currentContext = copy.copy(Pipe.getContext())  # don't want alteration of variable
    if action == "currentShot":
        get_tang_window().ask_to_save_document()  # TODO : Should have a callback to be able to cancel the playblast process when select cancel
        stepContainer = Pipe.get(currentContext.containerName)
        stepContainer.Playblast.run(mode="deported", forceUpdateContext=False)

        if hasattr(stepContainer, "PlayblastPreroll"):
            neededDynamicByModel = {}
            if currentContext.shot["ovm_dynamicInfos"] is not None:
                neededDynamicByModel = currentContext.shot["ovm_dynamicInfos"].get("needed-dynamic-by-model", {})
            if neededDynamicByModel.get("cloth", {}):
                stepContainer.PlayblastPreroll.run(mode="deported", forceUpdateContext=False)

        if hasattr(stepContainer, "PlayblastInterframe"):
            stepContainer.PlayblastInterframe.run(mode="deported", forceUpdateContext=False)

    elif action == "select another shot":
        scenePath = osWindow.select(selectMode="SelectFile")
        if scenePath:
            context = Context.initFromPath(scenePath)
            Pipe.setContext(context)
            stepContainer = Pipe.get(context.containerName)
            stepContainer.Playblast.run(mode="deported", forceUpdateContext=False)

            if hasattr(stepContainer, "PlayblastPreroll"):
                neededDynamicByModel = {}
                if context.shot["ovm_dynamicInfos"] is not None:
                    neededDynamicByModel = context.shot["ovm_dynamicInfos"].get("needed-dynamic-by-model", {})
                if neededDynamicByModel.get("cloth", {}):
                    stepContainer.PlayblastPreroll.run(mode="deported", forceUpdateContext=False)

            if hasattr(stepContainer, "PlayblastInterframe"):
                stepContainer.PlayblastInterframe.run(mode="deported", forceUpdateContext=False)
            # restore the context
            if currentContext is not None:
                Pipe.setContext(currentContext)


def checkPublishability():
    """Launch check Action of current step"""
    context = Pipe.getContext()
    stepContainer = Pipe.get(context.containerName)
    stepContainer.Check.run(display=True)


def publish():
    """Launch Opensave to select file and publish it"""
    osWindow.publishFile()


def saveFile():
    osWindow.saveFile()


def saveAsFile():
    osWindow.saveAsFile()


def buildFile():
    userSelect = suggestSaveWhenDirty()
    if userSelect == "Cancel":
        return
    osWindow.buildFile()


def refreshReferences():
    Pipe.getAssetManager().makeEmptyCache()
    soft = Pipe.getSoft(Pipe.getContext().software)
    filePath = soft.getCurrentFilePath()
    Pipe.setContext(Context.initFromPath(filePath))
    toolbox = Pipe.getToolbox("BuildTangToolbox")
    toolbox.updateSceneReferences(display=True)


def launchReUseManager():
    ReUseManager()


def suggestSaveWhenDirty():
    if get_document().dirty:
        soft = Pipe.getSoft(Pipe.getContext().software)
        currentScenePath = soft.getCurrentFilePath()
        userClickedButton = suggestSaveUi(currentScenePath)
        if userClickedButton == "Cancel":
            return "Cancel"
        elif userClickedButton == "Save":
            soft.save(currentScenePath)
        elif userClickedButton == "Increment and Save":
            currentVersion = currentScenePath.rsplit("_v")[1].split(".")[0]
            nextVersion = str(int(currentVersion) + 1).zfill(3)
            nextScenePath = currentScenePath.replace("_v%s." % currentVersion, "_v%s." % nextVersion)
            soft.save(nextScenePath)
        elif userClickedButton == "Don't Save":
            # Do not do anything
            pass


def animateCheckAssetShot():
    context = Pipe.getContext()
    if context is None or context.episode is None or context.episode["name"] != "check-models":
        showMessage('First open a shot from "check-models" episode and then clic on this button')
    else:
        tool = Pipe.getTool("CheckModelsTool")
        if tool:
            PipeReader.processAction("checkModelsTool", toolbox=tool)
            return

        showMessage("No animation defined for this production, ask youdata manager for it")


def reloadScripts():
    rollbackImporter = RollbackImporter("jad_pipe")
    rollbackImporter.rollback()

    from jad_pipe.core.pipe import Pipe

    Pipe.__graph__ = None
    Pipe.initGraph()

    logger.info("Scripts Reloaded")


def refreshBackground():
    toolbox = Pipe.getToolbox("BuildTangToolbox")
    toolbox.addLayoutAssets()


def refreshAnimFromLayout():
    toolbox = Pipe.getToolbox("BuildTangToolbox")
    toolbox.refreshAnimFromLayout()


def getCamFromScene():
    toolbox = Pipe.getToolbox("BuildTangToolbox")
    toolbox.getCamFromScene()


def launchOcclusion():
    tangWindow = QApplication.instance().main_window
    OcclusionLauncherUI(parent=tangWindow)
