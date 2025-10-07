---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Callback Processes

You can easily add custom code overrides, either using menu buttons or by specifying script paths on the command line.

## Add Custom Code Around Manual Actions

When you want to execute code after an action manually triggered from the UI:

- Replace the native menu button with your own [(see here).](general#custom-menus)
- Insert your custom code around the base action called by the button.

Below is the code executed behind the default items.

```python
from PySide2.QtWidgets import QApplication
tang_window = QApplication.instance().main_window
```

"File > Load Shot" : `tang_window.load_shot_files()`
"File > Save Shot" : `tang_window.export_shot_file()`
"File > New" : `tang_window.new_document()`

## Add Custom Code Around Loading Actions

If you want to inject code during Tangerine's loading actions, you can use the command line and provide a script path to execute.
This script should contain the algorithm that defines the order of actions to perform.

You can also pass arguments to the script by adding them after the script path.
Tangerine will skip any arguments it does not recognize.

See the command line documentation for details, and refer to the demo package for an example.

<details>
  <summary>Demo package command</summary>

    ```
    "C:\Program Files\TeamTO\Tangerine\1.7.14\TangerineConsole.exe" --log_to_file --kernel release --no-gui -l debug "E:/TEMP/tangerine/Tangerine Demo 2025/hook.py" E:\work\sandbox\tang-docs\docs\runTangContainerBatch.py --firstarg --secondarg 42 --filePath "E:\TEMP\tangerine\Tangerine Demo 2025\api_samples\three_capy.shot"
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
