Geoff's ComfyUI Tweaks
=======

## Requirements

Download this branch, patch changes onto upstream HEAD, or patch into self-contained ComfyUI (detailed patching instructions below)

If missing, install python-osc


## OSC

Comfy runs an OSC server on port 8189

Send messages in the format /which/what value

- 'which' is the title of the node 
- 'what' is the index of the widget in that node
- 'value' is the value to set that widget to

For instance, the following messages work against the default graph:

- /Empty Latent Image/0 256    # Sets width
- /Empty Latent Image/1 256    # Sets height
- /KSampler/2 23               # Sets number of steps
- /CLIP Text Encode (Prompt)/0 "bottle, galaxy, purple"  # sets prompt

Note that you can edit the titles of nodes in Comfy using the Properties panel to ensure unique titles for each node. In the default graph there are two nodes titled "/CLIP Text Encode (Prompt)/0" and the above OSC message only works as expected because the positive one ("bottle galaxy") is encountered before the negative one ("text, watermark") when iterating the nodes.

To control something which is an input rather than a widget, use ComfyUI menu's Add Node -> utils -> Primitive option to create a Primitive Node, give it a unique title, connect it to the input you want to control, and drive the Primitive's widget via OSC.


## Framing

There are additional OSC messages to control the framing of the graph in the ComfyUI:

- /canvas_print   # print the current x, y, and zoom to the javascript console (view on chrome by opening "More Tools -> Developer Tools")
- /canvas_offset_zoom 0.0 0.0 1.0   # Set x and y offset and zoom level
- /canvas_save foo    # Save current canvas framing (offset and zoom) with name 'foo'
- /canvas_load bar    # Load canvas framing previously saved with name 'bar'

canvas_offset_zoom is performant enough to drive with e.g. 30 OSC messages per second, from a smoothing algorithm or curve in a timeline. canvas_load applies smoothing on load.

To maximize the frame, the menu panel auto-minimizes to the right edge of the screen ([credit](https://pastebin.com/dvcH8nfY)).

 
## Patching a self-contained Comfy to include Geoff's changes

- double-click ComfyUI_windows_portable\update\update_comfyui_and_python_dependencies.bat as a sanity check that updates are working
- Download [.ci/update_windows/update_geoff.py](https://github.com/gmatters/ComfyUI/blob/master/.ci/update_windows/update_geoff.py)
 from this (Geoff's) repo
- rename to update.py
- use this to overwrite the file update.py in ComfyUI_windows_portable\update\
- double-click ComfyUI_windows_portable\update\update_comfyui_and_python_dependencies.bat

This will update the self-contained ComfyUI to Geoff's HEAD. If Geoff's HEAD is behind the state of origin when self-contained was built, some features may be rewound. An alternate solution is to generate a patch of changes to Geoff's branch and apply it to the self-contained code, although that will also stop working once there is a merge conflict.

