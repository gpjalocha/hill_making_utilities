# OBJ to XML _<3dmodel../>_ wrapper

This script allow you to convert OBJ and MTL exported models from blender to xml `<3dmodel...>` code. It separates exported model into batches by assigned materials. It also suppors assigning specific textures and materials by specifying those in material names in blender. This script also extracts UV data from OBJ so you can map the texture on your model in blender's UV editor.

## Prerequisite

* Model needs to be triangulated before export(more about triangulation in next paragraph)
* To extract colours model must have assigned material(for example principled BSDF) with  base color from which converter extracts HEX
* If you specify `Textures\<texture_name>.png`or/and `Materials\<material_name>.xml`, then converter extracts those from material name and assigns those to the batch.

## Model triangulation
Before exporting your model it needs to be triangulated. You can do that in 3 ways:

1. Select *Triangulate Faces* checkbox in export menu under *Geometry* tab:
![trian](pics/trian.jpg)

2. Apply *Decimate* modifier with *triangulate* option. It's the best way if you have model with big vertices count, so you can compress it before exporting to XML


![decimate](pics/decimate.jpg)

3. Apply *Triangulate* modifier to your model.

## Setting up the materials and textures
You can assign the Texture and Material in material name. If it's not specified correctly(or not specified at all) then it assigns by default `Material\material1.xml` and `Textures\concrete5.png`.
![material](pics/material.jpg)
### Zbias and alphatest
Script also reads from material `'zbias=[0-9]'` if specified. Also alphatest is supported, but it's giving a poor results.

## Setting up the UV mapping
If you create some model from scratch, it's good to check if UV mapping is correct. You can check that in UV editor while being in Edit Mode(Tab) and selecting all the object vertices(a).

## Export instruction
* Make sure, that you have your model selected.

> **tip**: If you have multiple objects, you can merge them into one by selecting all of them in object mode, and then press *ctrl+j*

* File->Export->Wavefront(.obj)
* Select *Selection only* checkbox and set *Z forward* in transform panel
* Export to the folder where the script is located 

## Usage

Required arguments
| Attribute | Type   | Description                                               |
| --------- | ------  | --------------------------------------------------------- |
| <style>input_obj | String   | Input file path (without .obj .mtl extension)                                   |
| output_xml| String   | Output file path           |

Optional arguments:
| Attribute | Type | Default value  | Description                                               |
| --------- | ------  | --------- |--------------------------------------------------------- |
| inv_faces | Bool  | 0           | Flag whether to invert model faces           |
| scale_uv  | Float  | 1.0           | Scale for UV coordinates        |
| scale     | Float |     1         | Scale for the model vertices |
| model_tag | String |     model     | Model tag. From DSJ 1.8.0 it is `model` not `3dmodel` |
| use_normals| String |   n           | If 'y' - script uses normals defined in obj which are assigned to every vertex |


Example usage: navigate to this folder and launch command below:
```{bash}
python obj_wrapper_3d.py\
--input_obj=cube \
--output_xml=cube \
--inv_faces=0 \
--scale_uv=1 \
--model_tag=3dmodel
--scale=1
--use_normals=n
```

After executing that command, cube.xml file should appear. Copy the content of this file into your hill xml and it should result with this.
![res](pics/res.jpg)
