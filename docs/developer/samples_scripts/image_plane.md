---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Image plane

## animation references

A tool is available for animators to see in their camera image or image sequences references.
This tool is called "animation reference" and can be pre-configured in the pipeline as following.

```python
document = get_document()
imgPath = "E:/TEMP/Maya/Tangerine Demo 2025/api_samples/image_plane_sequence/anim_reference_image_plane.001.jpg"

ref = document.animation_references.register(imgPath)
ref.label = "animatic"
```
## Image plane on camera

If you need to create a specific image plane in your shot, you can create the following nodes by script.
Adding it to your asset trough Mikan features would be the best practise but sometimes you only need the node in animation and want to keep your cameras `.tang` clean.

...sample to come...
