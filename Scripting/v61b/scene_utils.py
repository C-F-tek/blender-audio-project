import bpy


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    datablocks = [
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.lights,
        bpy.data.cameras,
        bpy.data.curves,
        bpy.data.actions,
        bpy.data.images,
        bpy.data.worlds,
        bpy.data.collections,
    ]

    for collection in datablocks:
        for block in list(collection):
            try:
                if block.users == 0:
                    collection.remove(block)
            except Exception:
                pass


def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')


def safe_active(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def create_controller_empty(name, location=(0, 0, 0), parent=None, display_size=0.25, hide_view=True):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.empty_display_size = display_size
    obj.hide_render = True
    obj.hide_select = True
    obj.hide_viewport = hide_view

    if parent is not None:
        obj.parent = parent

    return obj


def iter_action_fcurves(action):
    if action is None:
        return

    if hasattr(action, "fcurves"):
        try:
            for fc in action.fcurves:
                yield fc
            return
        except Exception:
            pass

    layers = getattr(action, "layers", None)
    if layers:
        for layer in layers:
            strips = getattr(layer, "strips", None)
            if not strips:
                continue
            for strip in strips:
                channelbags = getattr(strip, "channelbags", None)
                if not channelbags:
                    continue
                for channelbag in channelbags:
                    fcurves = getattr(channelbag, "fcurves", None)
                    if not fcurves:
                        continue
                    for fc in fcurves:
                        yield fc


def set_linear_interpolation_idblock(idblock):
    if idblock is None:
        return

    anim = getattr(idblock, "animation_data", None)
    if not anim:
        return

    action = getattr(anim, "action", None)
    if not action:
        return

    for fcurve in iter_action_fcurves(action):
        for kp in getattr(fcurve, "keyframe_points", []):
            kp.interpolation = "LINEAR"
