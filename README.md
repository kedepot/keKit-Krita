# keKit [](#)  

A simple general purpose script collection plug-in. 

Designed to be as compact as possible when used as a docker:

<img width="40%" alt="docker" src="https://github.com/user-attachments/assets/8d6fc693-c39c-4541-a459-2e6754f34a9e" />

&nbsp;
### Installation [](###)  
1. Download zip file (from 'Releases' --> )
3. Follow the Installation Guide in [Krita Docs](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin) (Use the manual steps, easy enough!)
&nbsp;
### Updating [](###)  
1. Close Krita
2. Manually overwrite the **kekit folder** in **your plugin directory** (See [Krita Docs](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin) for system specific locatation)
3. Restart Krita
   
&nbsp;

Note: Some scripts can be assigned to shortcuts:

<img width="50%" src="https://github.com/kedepot/keKit-Krita/assets/95410139/017ca795-6f67-4c4d-945c-5725ae1fcefe" />

&nbsp;
&nbsp;
## keKit Scripts: [](###)  

### Center 
Centers the selected/active layer  
Variants:
- H : Centers layer to Horizontal center (only)
- V : Centers layer to Vertical center (only)

&nbsp;
### keGrid
![img_grid](https://github.com/kedepot/keKit-Krita/assets/95410139/a9ae7e37-6be3-446e-8851-a0d492b27419)

Calculates a relative grid (with two subdivisions) based on the document size.  
- Will automatically clear "grid offset" values.
- Relative, but not "dynamic": Requires updating (toggle on/off) if your document size changes.  
- _Some smaller visual glitches may occur - it is just auto-calculating the regular fixed grid._

Options:
- **Snap**: Also toggles snapping on/off  
  _Note: <ins>Kritas layer snapping only uses **the mouse pointer**</ins>_  
         _A layer bounding box (or center) based grid snapping solution does not exist afaict_
- **3rd**: Uses Rule of Thirds instead for quad grid layout

&nbsp; 
### Batch
![img_batchexport](https://github.com/kedepot/keKit-Krita/assets/95410139/8bb6f406-a491-496a-8bb8-ada4a6a5e70b)

- Batch-exports paint, group, clone & vector **layers**, **set to visible**, from the current active document.
- Automatically creates a sub directory for the exports based on the document name & location
    - The document needs to be **saved** before the batch operation
- Visible **root** layers & groups that are named 'Fx', 'Background', "fg" or "bg" are **excluded**:
    - Useful for processing different groups with the *same effects* and/or *backdrop* (for example)
    - Capitalization indifferent - any style will work: fx, FX, Fx etc.

Options:
- **JPG**: keBatch uses JPG instead of PNG.
- Format Defaults: (override in ke_batch.py if needed)
  - PNG: Alpha, Level 0/Uncompressed. *For maximum speed now - [oxipng](https://github.com/oxipng/oxipng) (or [pngcrush](https://en.wikipedia.org/wiki/Pngcrush)) later*
  - JPG: 85%. *For WIP & quality insensitive use-cases*
    
#### BET
Batch Export Textures - a PBR game/vfx-ish texture export workflow:
  - Exports will be placed in the same dir as the doc (**not** in a generated sub-dir as Batch above)
  - Layers/groups named "b","d","r","m","ao","e","bump", "disp", "displacement", "roughness", "rough", "metal", "metallic", "emissive", or "mask",
    will be exported as **8-bit grayscale**
  - All others (such as "c" or "n") will be exported as **8-bit RGB**.
  - The layers/groups will use the document name as basename and add the the layer/group names as suffixes. E.g: "concrete01.kra" exports becomes "concrete01_c", "concrete01_r" etc. (if the layers are named "c" and "r")
  - Note: The export will autosave (saved doc must be latest, far less annoying than to forget...)
  - PNG-only. Level 0/Uncompressed. *For maximum speed now - [oxipng](https://github.com/oxipng/oxipng) (or [pngcrush](https://en.wikipedia.org/wiki/Pngcrush)) later*

*Note: Slow - it can take some time in big documents with a lot groups*

&nbsp;
### Half & Double
Scale selected layer 50% or 200%

&nbsp;
### Fit Bounds
Stretches selected layer to fit the document bounds  
Option:
- **Aspect**: Fit Bounds maintains aspect ratio of the layer

&nbsp;
### Transform Method
Choose preferred pixel transform processing method for Half, Double & Fit Bounds etc.
- Mitchell, Lanczos3 etc.

&nbsp;
### Average Color (AVG)
[![VIDEO DEMO](https://github.com/user-attachments/assets/471338e5-993b-49d3-b709-243bbfb6964f)][vid_avg]

[vid_avg]: https://github.com/kedepot/keKit-Krita/assets/95410139/984bff2e-867f-4d89-aca9-87c1fb493fff

Set selection (or entire layer, if you have no selection) to the average color of all the pixels.  
Ignores color from transparent pixels - for a better/expected average
- (F) Option:
  - FAST: (On) Limited pixel sample size for substantial speed increase (any image size)
  - ACCURATE: (Off) Process every single pixel for more accurate result (*Very* slow on large selections/images)  


&nbsp;
### chPack (RGBA Channel Packing)
![2023-10-23_16-51-23](https://github.com/kedepot/keKit-Krita/assets/95410139/e837f3d1-ee43-4093-9f3c-37b062778b28)

Automates Channel-packing 3-4 layers into a single image using the RGBA channels.  
Often used in real-time 3D. ['Splat-maps'](https://en.wikipedia.org/wiki/Texture_splatting) or ['ORM Textures'](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) for example. 

- The "New" option toggled will create a new document for the setup
   
**To Export RGB (No Alpha Channel)**:
- Select 3 layers - **Select one by one in intended RGB order**
- Run **chPack** & the selected layers will be arranged in a group, prepared for export
- Export/save as usual  
  
**To Export RGBA**:  
The standard Krita PNG Export will erase data in the RGB channels when using Alpha.  
Instead, Kritas ["Split-Alpha"](https://docs.krita.org/en/reference_manual/layers_and_masks/split_alpha.html) feature is used for full RGBA channel export:  

- Select 4 Layers - in RGBA selection order
- Run **chPack** & the selected layers will be arranged in a group, prepared for export
- Use RMB on the created Group Transparency Mask (as the "Alpha Channel") and use *Split-Alpha / Save as Merged*


&nbsp;
### Tile
![kekit_krita_tile](https://github.com/user-attachments/assets/a017467a-b1aa-4fc5-a56a-061052863dc4)
Scales, duplicates and places 4 tiles (copies) of the selected layer to fit the image bounds 
- Make sure the layer is trimmed to image size!


&nbsp;
### Seamless Tiling (ST)
[![VIDEO DEMO](https://github.com/user-attachments/assets/d4d83bed-9656-459c-a57e-9c5952a090ff)][vid_st]

[vid_st]: https://github.com/user-attachments/assets/d4d83bed-9656-459c-a57e-9c5952a090ff

Simple 'cross-offset' seamless tiling - creates a group of masked layers.
- This is a very simple method, do not expect every case to work well 
- The mask is a regular PNG included in keKit, adjust to your liking if needed
- Tip: Tweak with Kritas Wrap-around mode.


&nbsp;
### Feedback: [](###)
Right here. Leave messages (with appropriate tags & description) in Issues tab at the top!

Alternatively, check the [keKit thread](https://krita-artists.org/t/kekit-for-krita/74504) on the krita-artists.org forum.
