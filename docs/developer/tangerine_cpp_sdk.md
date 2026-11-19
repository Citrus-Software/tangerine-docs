---
sidebar_position: 10
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Tangerine C++ SDK

The Tangerine C++ SDK allows you to create custom deformers as well as custom general nodes for Tangerine.
Custom nodes use the **xNode** class, while custom deformers use the **xDeformer** class. Both classes are internal to Tangerine, and creating a custom node/deformer is not about subclassing xNode/xDeformer but it's configuring it with dynamic plugs and evaluation functions. So, for each custom node or deformer, we need two files:
- the json file which describes the plug structure
- the shared library ("dll" on windows, "so" on Linux) where evaluation functions are coded in C++

## Tools and compilers

We use CMake for the provided samples in the SDK, but you are free to use your preferred build system.

### Windows

You need to use Microsoft Visual Studio 2022 to compile your shared library.

### Linux

On Linux, the existing gcc of the distribution is used (gcc 11 on Rocky 9.x and gcc 13 Ubuntu 24.x).

## Content of the SDK

The SDK is installed with Tangerine in its installation folder, it's the Tangerine-SDK.zip file (on Linux: Tangerine-SDK.tar.gz). You can extract this archive wherever you like. It's composed of the following folders:
- include and lib: include files and release library needed to build a shared library for Tangerine.
- third_party: prebuilt dependencies are provided here (Intel TBB, Imath, Boost and Sentry) as well as their headers, and header-only libraries (rapidjson and gsl).
- samples: many samples of custom nodes and deformers you can draw inspiration from (including the examples described below)

## Custom Nodes

Let's jump into an example of a custom node named Log10:

1. Here is the content of **log10_node.json**:
```json
{
  "class": "xNode",
  "version": "1.0",
  "author": "Tangerine Team",
  "plugs": [
    [ "input", "float" ],
    [ "output", "float", ["input"] ]
  ]
}
```

See how **plugs are defined using this schema: [name, type, [dependencies if any]]**
xNode is a subclass of Node, so the only existing plug is "name", this is why you need to add more plugs using this method.

:::info
All plugs defined in the json file have a default value directly set internaly by Tangerine: float and integer values are initialized with zero, booleans values with true, 3D vectors with null vectors, matrices with identity and strings and all arrays with empty values.
:::

2. Here is the content of **Log10.cpp** (used to compile the shared library):
```cpp
// Log10 Node sample

#include "stdafx.h"

#ifdef _WIN32
#  define LOG10_API extern "C" __declspec(dllexport)
#else
#  define LOG10_API extern "C"
#endif

#include <any>

LOG10_API int sdk_version() {
    return META_NODAL_SDK_VERSION;
}

LOG10_API void eval_output(
    std::any* output,
    const std::vector<std::any>* args)
{
    static std::once_flag flag;
    std::call_once(flag, [&]() { LOG_INFO("Hello Tangerine SDK!"); });

    if (args->size() != 1) {
        LOG_ERROR("Parameter count in Log10 should be 1");
        return;
    }

    float input;

    try {
        input = std::any_cast<float>((*args)[0]);
    }
    catch (const std::bad_any_cast& e) {
        LOG_ERROR("Bad parameters in Log10: " << e.what());
        return;
    }

    *output = std::log10(input);
}
```

See how **the evaluation fonction is named: "eval_" + plug name**
And see how std::any is used to transport the input parameters and the output value.

3. Here is how to use it in your Python scripts:
```python
from meta_nodal_py import xNode

# (...)

log10 = xNode(parent, name, log10_json_path, log10_dll_path)
```

Along with the common parent and name, you need to give the paths of the "configuration" files (json file and the compiled shared library).

## Custom Deformers

Custom Deformers are easier to configure because they all have the same structure: they deform vertices.
So configuring a custom deformers is just:
- providing the plugs from which the deformation depends in the json file
- providing the **deform** function (fixed name) in the shared library

Let's jump into an example of a custom node named Spherizer:

1. Here is the content of **spherizer_deformer.json**:
```json
{
  "class": "xDeformer",
  "version": "1.0",
  "author": "Tangerine Team",
  "plugs": [
    [ "radius", "float" ],
    [ "center", "meta_nodal_py.Imath.V3f" ],
    [ "strength", "float" ]
  ]
}
```
As you can see, no mesh nor spline are defined, that's because they are already in the xDeformer class (it's a subclass of Deformer).
The plugs list defines here only all dependencies the of mesh_out and spline_out plugs.

2. Here is the content of **Spherizer.cpp** (used to compile the shared library):
```cpp
// Spherizer Deformer sample

#include "stdafx.h"

#ifdef _WIN32
#  define SPHERIZER_API extern "C" __declspec(dllexport)
#else
#  define SPHERIZER_API extern "C"
#endif

#include <any>

SPHERIZER_API int sdk_version() {
    return META_NODAL_SDK_VERSION;
}

SPHERIZER_API void deform(
    size_t count,
    const Imath::V3f* src,
    Imath::V3f* dest,
    const std::vector<std::any>* args)
{
    static std::once_flag flag;
    std::call_once(flag, [&]() { LOG_INFO("Hello Tangerine SDK!"); });

    if (args->size() != 3) {
        LOG_ERROR("Parameter count in Spherizer should be 3");
        return;
    }

    float radius;
    Imath::V3f center;
    float strength;

    try {
        radius = std::any_cast<float>((*args)[0]);
        center = std::any_cast<Imath::V3f>((*args)[1]);
        strength = std::any_cast<float>((*args)[2]);
    }
    catch (const std::bad_any_cast& e) {
        LOG_ERROR("Bad parameters in Spherizer: " << e.what());
        return;
    }

    strength = std::clamp(strength, 0.f, 1.f);

    tbb::this_task_arena::isolate([&] {
        tbb::parallel_for(tbb::blocked_range<size_t>(0, count), [&](const tbb::blocked_range<size_t>& r) {
            for (size_t i = r.begin(); i < r.end(); ++i) {
                const auto& src_vertex = *(src + i);
                auto& dest_vertex = *(dest + i);
                auto test_vertex = src_vertex - center;
                const float d = test_vertex.length();
                if (d > 1e-6f && d < radius) {
                    auto sphere_vertex = center + radius * test_vertex.normalized();
                    dest_vertex = Imath::lerp<Imath::V3f, float>(src_vertex, sphere_vertex, strength);
                }
            }
        });
    });
}
```

### No "vertices only" deformations

If you need other data from the Mesh or Spline than just the vertice positions (but the way they are connected for example), to create smarter deformations, it's possible to implement in your shared library those functions:

```cpp
#include "Mesh.h"

// (...)

YOUR_API void mesh_deform(
    const meta_nodal::Mesh* src,
    meta_nodal::Mesh* dest,
    const std::vector<std::any>* args)
{
	// modify the output 'dest' Mesh as you wish
}
```

Same thing for Spline:

```cpp
#include "Spline.h"

// (...)

YOUR_API void spline_deform(
    const meta_nodal::Spline* src,
    meta_nodal::Spline* dest,
    const std::vector<std::any>* args)
{
	// modify the output 'dest' Spline as you wish
}
```