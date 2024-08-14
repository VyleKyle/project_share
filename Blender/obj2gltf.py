import bpy
import os
import sys
import glob

# Clear mesh objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

try:
    argv_idx = sys.argv.index("--")
except ValueError:
    argv_idx = len(sys.argv)

# Define the path to the directory containing the .obj and .mtl files
input_directory = sys.argv[argv_idx + 1]
print(sys.argv)

# Define the output directory for the .gltf file
output_directory = "obj2gltf/"

# List all .obj files in the input directory
obj_files = glob.glob(os.path.join(input_directory, "*.obj"))

# Loop over all .obj files
for obj_file_path in obj_files:
    # Clear mesh objects in the scene
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Import .obj
    bpy.ops.import_scene.obj(filepath=obj_file_path)
    
    # Export to .gltf
    obj_file_name = os.path.basename(obj_file_path)
    gltf_file_name = os.path.splitext(obj_file_name)[0] + ".gltf"
    gltf_file_path = os.path.join(output_directory, gltf_file_name)
    
    bpy.ops.export_scene.gltf(filepath=gltf_file_path)
    
    print(f"Exported {obj_file_path} to {gltf_file_path}")
