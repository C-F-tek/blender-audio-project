import math

import bpy

from config import CAMERA_BASE_LENS, CAMERA_BASE_LOCATION, CAMERA_DOF_FSTOP


def create_camera_rig():
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 1.25))
    target = bpy.context.active_object
    target.name = "CameraTarget"

    bpy.ops.object.camera_add(
        location=CAMERA_BASE_LOCATION,
        rotation=(math.radians(68.0), 0.0, 0.0),
    )
    cam = bpy.context.active_object
    cam.name = "MainCamera"
    cam.data.lens = CAMERA_BASE_LENS
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = target
    cam.data.dof.aperture_fstop = CAMERA_DOF_FSTOP

    con = cam.constraints.new(type="TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"

    bpy.context.scene.camera = cam
    return cam, target
