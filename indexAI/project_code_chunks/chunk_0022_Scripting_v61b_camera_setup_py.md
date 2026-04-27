# Project Code Chunk 22/212

- File: `Scripting/v61b/camera_setup.py`
- Part: `1`
- Lines: `1-29`

## Symbol Map
- Imports: `bpy`, `math`, `from config import CAMERA_BASE_LOCATION, CAMERA_BASE_LENS, CAMERA_DOF_FSTOP`
- Functions: `create_camera_rig()` line 7

## Content
```py
00001: import bpy
00002: import math
00003: 
00004: from config import CAMERA_BASE_LOCATION, CAMERA_BASE_LENS, CAMERA_DOF_FSTOP
00005: 
00006: 
00007: def create_camera_rig():
00008:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1.25))
00009:     target = bpy.context.active_object
00010:     target.name = 'CameraTarget'
00011: 
00012:     bpy.ops.object.camera_add(
00013:         location=CAMERA_BASE_LOCATION,
00014:         rotation=(math.radians(68.0), 0.0, 0.0),
00015:     )
00016:     cam = bpy.context.active_object
00017:     cam.name = 'MainCamera'
00018:     cam.data.lens = CAMERA_BASE_LENS
00019:     cam.data.dof.use_dof = True
00020:     cam.data.dof.focus_object = target
00021:     cam.data.dof.aperture_fstop = CAMERA_DOF_FSTOP
00022: 
00023:     con = cam.constraints.new(type='TRACK_TO')
00024:     con.target = target
00025:     con.track_axis = 'TRACK_NEGATIVE_Z'
00026:     con.up_axis = 'UP_Y'
00027: 
00028:     bpy.context.scene.camera = cam
00029:     return cam, target
```
