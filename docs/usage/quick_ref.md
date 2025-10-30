# Quick Reference

:::tip
All the following keyboard shortcuts can be customized via the Shortcuts window (menu Windows)
:::

## Time control

- **Space** = Play/Stop animation
- **Ctrl+Space** = Play/Stop animation at alternate speed (hold keys down to set the ratio in overlay tool, default is half speed)
- **Right** = Next frame = **Mouse Wheel Down**
- **Left** = Previous frame = **Mouse Wheel Up**
- **Up** = Next key = **Alt+Mouse Wheel Down**
- **Down** = Previous key = **Alt+Mouse Wheel Up**

## General

- **Ctrl+Z** = Undo
- **Ctrl+Y** = Redo
- **Ctrl+G** = Repeat last action

## Keys

- **S** = Add Key on selection
- **Alt+S** = Insert Key on selection (freeze tangents to keep the curve shape unchanged)
- **Del** = Delete Keys (or, depending on Focused Window: Delete Selected Tag, Dummy, Constraint or Cluster)
- **Ctrl+C** = Copy Keys
- **Ctrl+V** = Paste Keys
- **Ctrl+Shift+C** = Copy World: copy the transform of the selected controller in world space
- **Ctrl+Shift+V** = Paste World: adapt the selected controller local transform to reach the copied world transform

Preferences (Channels Right-clic contextual menu):
- **Undo/Redo Restore Channels** (default is OFF)
- **'Create Keys' Key All**, all plugs are keyed when pressing S, not only the selected plugs (default is ON)
- **'Create Keys' Key Extra Exclusive**, extra plugs (layer weights and fps dividers) are not keyed when pressing S unless they are exclusively selected (default is ON)

## Viewport

### Gizmos
- **E** = Rotation, press again E to cycle through modes:
	- Object: around Rotated axes depending on the rotate order
	- World: around fixed world axes
	- Gimbal: around each axis independently (no rotate order dependency)
- **W** = Translation, press again W to cycle through modes:
	- Object: along Rotated axes (of each selected controller)
	- Object Last: along Rotated axes (of the last selected controller)
	- World: along fixed world axes
	- Parent: along *Parent* Rotated axes (hence independant of current Rotation)
- **R** = Scale (Object mode, ie along Rotated axes)
- **Q** = No Gizmo (selection only)
- **Alt+Up/Down/Left/Right** = Translate selected controllers in camera space by one pixel
- **Mid-drag** = TODO 🚧

Gizmo Display:
- **Ctrl+Plus** = Increase size of Gizmos
- **Ctrl+Minus** = Decrease size of Gizmos
- **Alt+Plus** = Increase thickness of Gizmos
- **Alt+Minus** = Decrease thickness of Gizmos

### Selection

- **Ctrl+A** = select all nodes in assets: the selection should have at least 1 controller in each asset you want to select, otherwise (empty selection) all controllers of all assets are selected (caution!)

### Overlay tools

**Hold the key down:**
- **B** = Tween Machine
- **M** = Motion Trail
- **C** = 2D Pan/Zoom

### Toggle modes
- **Ctrl+R** = Animation Reference Mode
- **Ctrl+D** = Annotation Tool

### Cameras
- **F** = Frame view on controller selection (or all if no selection)
- **Ctrl+0** = Shot Camera
- **Ctrl+1** = Front Camera
- **Ctrl+2** = Bottom Camera
- **Ctrl+3** = Back Camera
- **Ctrl+4** = Left Camera
- **Ctrl+5** = Persp Camera
- **Ctrl+6** = Right Camera
- **Ctrl+7** = Stalker Camera (if any)
- **Ctrl+8** = Top Camera
- **Alt+0** = Opposite Camera

### Shading
- **F1** = Shaded (default)
- **F2** = Wireframe
- **F3** = Wireframe on Shaded

## Mouse

### Timeline
- **Hold Left-clic** = loop sound at this frame
- **Alt+Mid-clic and drag** = insert/remove spacing
- **Mid-clic at any frame** = add key at this frame
- **Mid-clic at frame A, drag to frame B and release** = Copy Pose of frame A to frame B

Preferences:
- Right-clic contextual menu: Undo/Redo Restore Current Frame (default is ON)

### Library

TODO 🚧

Preferences:
- Right-clic contextual menu: Anim Merge Mode > Replace (default)

### Channels

TODO 🚧

### Curve Editor

- **F** = Frame view on selected keys (or all if no selection)

For all Keys and Tangents tools:
	- **Mid-drag anywhere** (with non-empty key/tangent selection)
	- **Left-drag on any selected** key/tangent
	- **Left-drag on 1 unselected** key/tangent for both selection+tool

Keys Edition (no tangent selected ; time of keys are locked unless Shift is hold *after* the mouse has been pressed):
- **W** or **E** = Move value of selected keys
- **R** = Scale value of selected Keys (scaling ratio cannot be negative if Ctrl is hold *after* the mouse has been pressed), press R again to toggle between the two modes:
	- default mode (icon with two squares): the scale center is where you first pressed the mouse
	- relative mode (icon with a cross): the scale center is the interection point of the curve and the vertical line where you first pressed the mouse

Tangents Edition (at least one tangent is selected):
- **W** = Move selected tangents (scale and rotation together)
- **E** = Rotate selected tangents
- **R** = Scale selected tangents

Tangent Modes (on selected keys/tangents):
- **Shift+A** = Auto tangents
- **Shift+P** = Step tangents
- **Shift+L** = Linear tangents
- **Shift+F** = Flat tangents
- **Shift+I** = Spline tangents
- **Shift+C** = Custom tangents
- **Shift+B** = Break left/right tangents
- **Shift+U** = Unify left/right tangents

Preferences:
- Right-clic contextual menu: Tangents > Default Tangent Mode > Auto (default)
