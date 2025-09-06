# keKit [](#)  

A simple general purpose script collection plug-in. 

Designed to be as compact as possible when used as a docker:

![2023-10-46_16-14-46](https://github.com/kedepot/keKit-Krita/assets/95410139/e9511413-1fa6-41a3-b449-27f598940441)

&nbsp;
### Installation [](###)  
1. Download zip file (from 'Releases' --> )
3. Follow the Installation Guide in [Krita Docs](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin)
&nbsp;
### Updating [](###)  
1. Close Krita
2. Manually overwrite the **kekit folder** in **your plugin directory** (See [Krita Docs](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin) for system specific locatation)
3. Restart Krita

&nbsp;


Note: All the scripts can be assigned to shortcuts:

![img_shortcuts2](https://github.com/kedepot/keKit-Krita/assets/95410139/017ca795-6f67-4c4d-945c-5725ae1fcefe)


&nbsp;
&nbsp;
### keKit Scripts: [](###)  

&nbsp;
#### Center 
Centers the selected/active layer  
Variants:
- H : Centers layer to Horizontal center (only)
- V : Centers layer to Vertical center (only)

&nbsp;
#### keGrid
![img_grid](https://github.com/kedepot/keKit-Krita/assets/95410139/a9ae7e37-6be3-446e-8851-a0d492b27419)

Calculates a relative grid (with two subdivisions) based on the document size.  
Note: Relative - not "Dynamic": Requires updating (toggle on&off) if your document size changes.  
_Also: Some smaller visual glitches may occur - it is just auto-calculating the regular fixed grid._

Options:
- **Snap**: Also toggles snapping on/off  
  _Note: <ins>Krita layer snapping only uses **the mouse pointer**</ins>_  
         _A layer bounding box (or center) based grid snapping solution does not exist afaict_
- **3rd**: Uses Rule of Thirds instead for quad grid layout

&nbsp; 
#### keBatch
![img_batchexport](https://github.com/kedepot/keKit-Krita/assets/95410139/8bb6f406-a491-496a-8bb8-ada4a6a5e70b)

- Batch-exports paint, group, clone & vector **layers**, **set to visible**, from the current active document.
- Automatically creates a sub directory for the exports based on the document name & location
    - The document needs to be **saved** before the batch operation
- Visible **root** layers & groups that are named 'Fx' & 'Background' are **excluded**:
    - Useful for processing different groups with the *same effects* and/or *backdrop* (for example)
    - **Any** capitalization style of 'Fx' and 'Background' will work (e.g: fx, FX, Fx etc.)

Option:
- **JPG**: keBatch uses JPG instead of PNG.
- Format Defaults: (override in ke_batch.py if needed)
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
#### Average Color (AVG)
Set selection (or entire layer, if you have no selection) to the average color of all the pixels.  
Ignores color from transparent pixels - for a better/expected average
- (F) Option:
  - FAST: (On) Limited pixel sample size for substantial speed increase (any image size)
  - ACCURATE: (Off) Process every single pixel for more accurate result (*Very* slow on large selections/images)  

[![VIDEO DEMO](https://github.com/user-attachments/assets/471338e5-993b-49d3-b709-243bbfb6964f)][vid_avg]

[vid_avg]: https://github.com/kedepot/keKit-Krita/assets/95410139/984bff2e-867f-4d89-aca9-87c1fb493fff

&nbsp;
#### toRBGA (Channel Packing)
![2023-10-23_16-51-23](https://github.com/kedepot/keKit-Krita/assets/95410139/e837f3d1-ee43-4093-9f3c-37b062778b28)

Automates Channel-packing 3-4 layers into a single image using the RGBA channels. Often used in real-time 3D. ['Splat-maps'](https://en.wikipedia.org/wiki/Texture_splatting) or ['ORM Textures'](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) for example. 

- The "New" option toggled will create a new document for the setup
   
**Instructions: RGB (No Alpha Channel)**
- Select 3 layers : Selection order is important: **Select each layer in intended RGB order**
- Run **toRGBA** & the selected layers will be arranged in a group, prepared for export
- Export/save as usual  
  
**Instructions: RGBA**  
The Alpha channel in Krita is not editable separately (it will always destroy data in the RGB channels in standard PNG export).
Instead, Kritas "Split-Alpha" export can be used in these cases, including toRGBA, for full RGBA-packing export.*

- Select 4 Layers in RGBA selection order
- Run **toRGBA** & the selected layers will be arranged in a group, prepared for export
- The Alpha layer will need to be manually converted to a *Transparency Mask* (RMB, convert...)
- RMB the Alpha layer (as Group Transparency Mask) and select *Split-Alpha / Save as Merged*
  - As described the [Krita docs](https://docs.krita.org/en/reference_manual/layers_and_masks/split_alpha.html).
- Note: The alpha layer will be selected & named "makeTM-SplitAlphaMerged" as a reminder/guide ;>

  
&nbsp;
### Feedback: [](###)
Right here. Leave messages (with appropriate tags & description) in Issues tab at the top!

Alternatively, check the [keKit thread](https://krita-artists.org/t/kekit-for-krita/74504) on the krita-artists.org forum.
