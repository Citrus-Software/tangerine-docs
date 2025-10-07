---
sidebar_position: 1
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Hello Tangerine

Welcome to the Tangerine Developer Guide! This part of the Tangerine documentation is intended to *Python developers*. With its scripting API, Tangerine allows you to develop custom Animation Tools, Pipeline scripts, Shot and Asset build scripts, and more! Here is our Hello Tangerine script, a quick start to jump straight into Tangerine Python development:

1. Launch Tangerine

2. Opens the "Command Line" via the Windows menu

3. Copy the following script, paste it into the Command Line window and press Enter:
```
# some module imports:
from tang_core.document.get_document import get_document
from tang_core.anim import set_animated_plug_value
from tang_core.callbacks import Callbacks

# please, replace SAMPLE_FOLDER_PATH with the folder where samples are installed:
capy_path = SAMPLE_FOLDER_PATH + "capy_jb.tang"

doc = get_document()  # the document is our main entry point to the Tangerine API

asset_node = doc.import_nodes("character1:capy_jb", capy_path)  

# with a "modifier", you interact with the current shot:
with doc.modify("import and anim capy") as modifier:
    controller = Callbacks().find_controller_in_asset(asset_node, "c_face_up")
    set_animated_plug_value(controller.el_blink_L, 0.0, modifier, frame=1, force_key=True)
    set_animated_plug_value(controller.el_blink_L, 1.0, modifier, frame=7)
    set_animated_plug_value(controller.el_blink_L, 0.0, modifier, frame=14)
```

4. Orbit the camera around the Capy to see its left eye and press Space to play the animation. You should see this:

**mettre ici un gif animé du clin d'oeil sous-titré Hello Tangerine**