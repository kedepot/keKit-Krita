# keKit [](#)  

A simple general purpose script collection plug-in.

Designed to be as compact as possible when used as a docker:

![img_docker](https://github.com/kedepot/keKit-Krita/assets/95410139/d03a03b9-958e-4b74-8142-39e8d68db54d)

&nbsp;
### Installation [](###)  
1. Download zip file (from 'Releases' --> )
3. Follow the Installation Guide in [Krita Docs](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin)

Note: All the scripts can be assigned to shortcuts:

![img_shortcuts2](https://github.com/kedepot/keKit-Krita/assets/95410139/017ca795-6f67-4c4d-945c-5725ae1fcefe)


&nbsp;
&nbsp;
### keKit Scripts: [](###)  

&nbsp;
#### Center
Centers the selected/active layer

&nbsp;
#### keGrid
![img_grid](https://github.com/kedepot/keKit-Krita/assets/95410139/a9ae7e37-6be3-446e-8851-a0d492b27419)

Calculates a relative grid (with two subdivisions) based on the document size

Options:
- **Snap**: Also toggles snapping on/off.
  _Note: Krita layer snapping only uses *the mouse pointer*: Layer bounds+center snapping TBD_
- **3rd**: Uses Rule of Thirds instead for quad grid layout.

&nbsp; 
#### keBatch
![img_batchexport](https://github.com/kedepot/keKit-Krita/assets/95410139/8bb6f406-a491-496a-8bb8-ada4a6a5e70b)

- Batch Exports **visible Groups/Folders**.
- Automatically creates a subfolder for the exports based on the document name & location.
    - Thus requires new documents to be **saved** before batch operation
- Visible **root layers** (& groups that are named 'Fx' & 'Background') are **excluded**:
    - Useful for processing each of the exported groups with the same effects and/or backdrop

Option:
- **JPG**: keBatch uses JPG instead of PNG.
    - Defaults (override in ke_batch.py if needed):
    - PNG: Alpha, Level 0/Uncompressed. *For maximum speed now - [pngcrush](https://en.wikipedia.org/wiki/Pngcrush) later*
    - JPG: 85%. *For WIP & quality insensitive use-cases*

*Note: Slow - the process can take a long time in big documents with a lot groups*

&nbsp;
#### Half & Double
Scale selected layer 50% or 200%

&nbsp;
#### Fit Bounds
Stretches selected layer to fit the document bounds
Option:
- **Aspect**: Fit Bounds maintains aspect ratio of the image

&nbsp;
#### Transform Method
Choose preferred pixel transform processing method for Half, Double & Fit Bounds:
- Mitchell, Lanczos3 etc.

&nbsp;
### Feedback: [](###)
Right here, leave messages (with appropriate tags & description) in Issues tab at the top!
