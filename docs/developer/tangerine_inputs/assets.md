---
sidebar_position: 4
---
# Assets for Tangerine

## Create Assets with Mikan

@max @seb add explanation here
(**Mikan**)[https://citrus-software.github.io/mikan-docs/]

## Create Assets with Mikan

## Export .tang Asset File

`.tang` asset files are normaly generated using the Mikan rigging toolkit.
However, if you need to integrate unrigged geometry, you can use the export asset feature to create a `.tang` file.


<Tabs>
  <TabItem value="Python Code" label="Python Code" default>
    ```python
    from tang_core.document.get_document import get_document

    path = "YOUR_ASSET_FILE_PATH.tang"
    document = get_document()

    # import an alembic with modeling
    alembic_path = "ALEMBIC_PATH_WITH_MODELISATION.abc"
    document.import_abc_in_new_asset(alembic_path, namespace="set")

    # find the top node created from your modeling alembic
    node = document.root().find("YOUR_ROOT_NODE_NAME")

    # export this root node as an asset in a .tang file
    document.export_asset(node, path)
    ```
  </TabItem>
  <TabItem value="Package sample" label="Package sample">
    ```python
        from tang_core.document.get_document import get_document

        DEMO_FOLDER_PATH = "E:/TEMP/Tangerine/Tangerine Demo 2025/"
        path = DEMO_FOLDER_PATH + "/api_samples/my_new_set_asset_file.tang"
        document = get_document()

        alembic_path = DEMO_FOLDER_PATH + "/api_samples/set_neutral_modeling.abc"
        document.import_abc_in_new_asset(alembic_path, namespace="set")

        node = document.root().find("set:set_neutral_modeling")

        document.export_asset(node, path)
        ```
  </TabItem>
</Tabs>

You are now capable to load your .tang file using "import asset" menu in tangerine.
This methodology is only available if you don't need any controls on this asset.
If you need to move, animate it, please use Mikan system to ccreate a tang asset with rig properly.
