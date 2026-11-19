# Release Notes

<!--
  Version headings format (keep it for every new version, the anchors must stay stable):

    ## Version X.Y.Z (YYYY-MM-DD) {#vX-Y-Z}

  - The date is ISO 8601 (YYYY-MM-DD).
  - The explicit anchor {#vX-Y-Z} depends only on the version number: replace each dot by a dash.
    Example: 1.7.11 -> {#v1-7-11}, 1.71.1 -> {#v1-71-1}.
  - Do NOT rely on the auto-generated anchor: Docusaurus strips the dots, so 1.7.11 and 1.71.1
    would both become "version-1711", and changing the date would change the link.
-->

## Version 1.8.5 (2026-11-09) {#v1-8-5}

### What's new ✨

#### Layers
- **Override Layers**: when creating a layer, and when editing it afterwards, you can choose between Additive and Override. Careful: order matters! Layers can be moved up and down via the context menu. Override layers are shown as a circle (additive = square).
- **"Float only" option** for additive layers.
- **Layers for booleans (True/False) and integer values** (enumerated choices, like the Body/World/Face FPS on the World), override only (no additive for these types).
- **Usage plugs**: a plug inside a layer can be temporarily ignored. Enable the layer, right-click the plug in the layer (e.g. "Translate X") > Add Usage Plug. A new plug appears at the very bottom, with the same name and the " Usage" suffix (e.g. "Translate X Usage"). It is a keyable plug (a float for float-type plugs). Disabling it excludes the original plug from the calculation.

#### Tweak Tools
- **Bake**: bakes every X frames (with special handling of constraints) and deletes the keys that are not on the right frames.
- **Simplify Densify**: lets you add or remove keys on animation curves. Removal drops first the keys that affect the curve shape the least.
- **Smooth Rough**: smooths or accentuates animation curves.
- **Connect**: readjusts a block of the curve, or a block of selected keys, to connect it to the previous or next pose.
- **Blend to Neighbor**: blends the selected pose or keys toward the left or right neighbor. Unlike Tween, which ignores the current value and mixes based on both neighbors, this one starts from the current value and fades it toward a single neighbor, depending on the tweak direction.
- **Scale from Average**: scales keys using the average value of each contiguous block of selected keys as the pivot.
- **Scale from Mid-range**: scales keys using the average of the two extremes of each contiguous block of selected keys as the pivot.
- **Staggered Rephase**: similar to Rephase, but each controller gets a different offset, to sync the animation while keeping the key timing in sync.
- **Rephase**: new Frames mode, new Fit option (uncheck it so the tool doesn't modify existing tangent modes), and more precise behavior on curves containing small values.
- Tweak tools are 10 to 15% faster.

#### Misc
- Improved int channel editing via middle click, now also usable on booleans (true/false).
- Cycle baking now also works on boolean and integer curves (previously decimal curves only).
- Added a button to bake the selected constraints on every frame where they are active, then delete the constraints.

#### Timeline & Range slider
- **Frame** (shortcut "F") on the timeline: the range slider fits the selected keys.
- Double-click on the range slider: toggles between the full shot range and the previous one.

#### Import / Save / Library
- **Mocap file import in FBX.**
- Auto-save is enabled by default, and its folder is pinned in the sidebar of the "shot" file loading window.
- Auto-load now favors the file closest to the server root rather than the deepest one when two files are candidates.
- A dialog warns the user that a built (i.e. non-imported) asset cannot be saved in a .shot.

### Fixes 🐛
- Step curves with cycles are now displayed correctly in the curve editor.
- Inter-frame keys could produce non-deterministic results.
- Fixes on undo for layers without anims, and on deleting and renaming a layer.
- The quick fix for animated FPS is generalized to all rigs (it used to depend on TT rigs).
- 2D pan zoom: the reset (backspace key) caused inconsistent behavior with the enable/disable toggle, and the preview rectangle was wrong when panning without changing the zoom.
- The Blend to Bindpose tweak tool now works with dummies.
- Shot cluster creation is skipped when loading a shot if its parent controller no longer exists (modified asset).
- UDIM paths pointing to an inaccessible folder are ignored.
- Library:
  - Request now auto-increments items coming from layers with the same name instead of overwriting them.
  - Migration and import fixed for old baked clip formats containing shot rig (dummies, cluster, constraint…).
  - Import fixed when the clip contained only shot rig and no animation/pose data from an asset.
  - Various fixes on banked shot clusters (automatic stick controller addition, geometry identification issue).
- Random viewport crash when deleting a geometry node from the scene.
- Crash when deleting an asset or a dummy with an active motion trail.

### Dev/Rig ⚙
- `mg.get_attr("{ns}", "ctrl", "attribute")` is available for picker script buttons.
- Interpolation parameters for multi-target constraints are now set directly on the constraint node.
- **USD export**:
  - Camera apertures converted to millimeters.
  - Fixed a crash when directly exporting an asset node (camera case; workaround = export its "geo" and "world" nodes by name).
  - Better preservation of relative paths.
- Improved localized shot package export: takes referenced animations and pickers into account, adds a default server lib folder.
- Mikan 1.0.10.
