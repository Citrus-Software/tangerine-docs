---
sidebar_position: 1
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Tags

Tags allow you to group elements in your hierarchy for quick access.
They can be used for various purposes, such as [baking with tags](usecase/#bake-tag-for-alembic).
For example, Tangerine uses tags to enable fast selection in the UI.

```python
from tang_core.document.get_document import get_document

tagger = get_document().tagger
super_tag = tagger.create_tag("YOUR_SUPER_TAG_NAME", show_in_gui=True)
tag = tagger.create_tag("YOUR_TAG_NAME", super_tag=super_tag, show_in_gui=True) # YOUR_TAG_NAME will also be considered as a YOUR_SUPER_TAG_NAME tag. You can think of it as inheritance in OOP.

nodes = [YOUR_NODE]
for node in nodes:
  tagger.tag_node(tag, node) @max il doit me doner un truc
```
