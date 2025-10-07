---
sidebar_position: 4
---
# Assets for Tangerine

## Create Assets with Mikan

@max @seb add explanation here
(**Mikan**)[https://citrus-software.github.io/mikan-docs/]

## Create Assets with Mikan

## Export .tang Asset File

`.tang` asset files are normally generated using the Mikan rigging toolkit.
However, if you need to integrate unrigged geometry, you can use the export asset feature to create a `.tang` file.

```python
from tang_core.document.get_document import get_document

DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"
filePath = DEMO_FOLDER_PATH + "/api_samples/my_node_asset_file.abc"
document = get_document()
node = document.root().find("character_jb:capy_modeling")

document.export_asset(node, path) @sixtine test
```
