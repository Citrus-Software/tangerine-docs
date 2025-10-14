---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Modifiers

For a matter of optimisation, stack clarity and engine and UI updates, you will need to encapsulate parts of script where you are modifying a document.
When closing a modifier, Tangerine will call every needed callback to compute values and update UI.

The only values of a document that do not need a modifier are `start_frame` and `end_frame`.

```python
from tang_core.anim import is_keyable, set_animated_plug_value
from tang_core.document.get_document import get_document

# selecting a plug
document = get_document()
node = document.root().find_first("c_face_up")
attribute = "el_blink_R"
plug = node.get_plug(attribute)

# add animation on plug in modifier
with document.modify("create anim curves") as modifier:
    if not is_keyable(plug):
        print("not keayble plug, skipping")
    else:
        set_animated_plug_value(plug, -0.2, frame=3, force_key=True, modifier=modifier)
        set_animated_plug_value(plug, -0.0, frame=10, force_key=True, modifier=modifier)
        set_animated_plug_value(plug, -0.1, frame=12, force_key=True, modifier=modifier)
```
