---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Modifiers

When building assets or in any batch process without GUI, we don't have to undo our edits, and there is no GUI to synch, so the direct API on plugs is fine (see previous page with set_value and connect calls).
In an interactive tool, it's different: we need to ask Tangerine to stop any background process, and we want Tangerine to synch all the GUI once we have finished our edition. That's where the Modifier comes in.
In fact, we have used modifiers from the very beginning of this developer guide, see Hello Tangerine.

:::warning
It's important to respect the pythonic `with` statement when using Modifiers (except for *Mouse-Interactive* Modifiers, see at the bottom of this page)
:::

## Main Modifiers Functions

Here are the 3 main functions we commonly use in scripts to edit the shots in an interactive tool:

- `modifier.set_plug_value(plug, value)` equivalent to `plug.set_value(value)` with a modifier
- `modifier.connect_plug(plug_from, plug_to)` equivalent to `plug_from.connect(plug_to)` with a modifier
- `node = modifier.create_node(node_class, parent_node, node_name)` equivalent to `node = node_class(parent_node, node_name)` with a modifier

Please see in the API Reference for details, but they are very straightforward! Here is the very first example of the previous page (Nodes) rewritten with a modifier. Note you can now press Ctrl+Z and Ctrl+Y (after you copy/pasted this script in the Command Line window) to Undo and Redo (Open the Node Tree to see the nodes disappear on Undo and reappear on Redo).

```python
from meta_nodal_py import Add

r = document.root()

with document.modify("example") as modifier:
    A = modifier.create_node(Add, r, 'A')
    B = modifier.create_node(Add, r, 'B')

    modifier.set_plug_value(A.input1, 1.0)
    modifier.set_plug_value(A.input2, 2.0)

    print(A.output.get_value())  # prints 3.0

    modifier.connect_plugs(B.input1, A.output)
    modifier.set_plug_value(B.input2, -3.0)

    print(B.output.get_value())  # prints 0.0
```

When editing a value with an animation connected in, it may be tricky to add a key, especially if there is an animation Layer under the hood. This is why we provide this handy helper: `set_animated_plug_value` (see Hello Tangerine for a sample usage).

Finally, there are many other functions on modifiers (to remove nodes, and much more... see the API Reference for details).

:::warning
- The only plugs of the Document that do not need a modifier are `start_frame` and `end_frame`.
- Tangerine modifiers are **not** related to [Mikan modifiers](https://citrus-software.github.io/mikan-docs/usage/modifiers) which serve a different purpose.
:::

## Voluntarily skipping modifiers

In rare occasions, you want to make some changes without using a modifier. In this cas, follow this pattern:
- first synch everything to ensure no background engine is running: `document.synch_compute_all_frames()`
- make yout edits
- finally, call `document.rig_has_changed_without_modifiers()`

## Mouse-Interactive Modifiers

Modifiers are useful in interactive GUI mode, but they may require a real mouse interaction before they finish.
In all previous examples, we have seen one-shot modifiers: there were no user interaction between the time they start and the time they end.
Here is how to have "interactive" modifiers:
- in your "on mouse pressed" callback, call `modifier = document.begin_interact("my interactive modifier")`
- then in your "on mouse move" callback, call:
```python
modifier.start_group()
modifier.set_plug_value(plug, value)
modifier.set_plug_value(another_plug, another_value)
modifier.end_group()
document.interact_modify()  # update the GUI while interacting
```
- finally, in your "on mouse release" callback, call `document.end_modify_interactive()`


