class ST_OT_select_group(bpy.types.Operator):
    bl_idname = "spaziotempo.select_group"
    bl_label = "Select Scene Group"

    group: bpy.props.StringProperty(default="hero")

    def execute(self, context):
        bpy.ops.object.select_all(action="DESELECT")

        names = []
        if self.group == "hero":
            names = ["HeroRoot", "HeroDeformController", "AuraAudioSampler"]
        elif self.group == "particles":
            names = [obj.name for obj in particle_emitters()]
        elif self.group == "fog":
            names = [
                "AtmosphereCube",
                "FogPulseController",
                "FogFilamentsRoot",
                "SoftRhythmBackdrop",
                "BackdropPulseController",
            ]
            names.extend(obj.name for obj in objects_with_prefix("FogFilament_"))
        elif self.group == "letters":
            names = ["AlbumLetterParticleSources"]
            names.extend(obj.name for obj in objects_with_prefix("AlbumLetterParticle_"))

        selected = []
        for name in names:
            obj = find_obj(name)
            if obj is None:
                continue
            obj.hide_viewport = False
            obj.select_set(True)
            selected.append(obj)

        if selected:
            context.view_layer.objects.active = selected[0]
        self.report({"INFO"}, f"Selected {len(selected)} objects.")
        return {"FINISHED"}


class ST_PT_tuning_panel(bpy.types.Panel):
    bl_label = "Scene Tuner"
    bl_idname = "ST_PT_tuning_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Spaziotempo"

    def draw(self, context):
        layout = self.layout
        tune = context.scene.spaziotempo_tuning

        row = layout.row(align=True)
        row.operator("spaziotempo.apply_tuning", icon="CHECKMARK")
        row.operator("spaziotempo.keyframe_tuning", icon="KEY_HLT")

        box = layout.box()
        box.label(text="Hot Update")
        row = box.row(align=True)
        op = row.operator("spaziotempo.hot_update_scene", text="Render Only", icon="OUTPUT")
        op.mode = "RENDER"
        op = row.operator("spaziotempo.hot_update_scene", text="Materials", icon="MATERIAL")
        op.mode = "MATERIALS"
        row = box.row(align=True)
        op = row.operator("spaziotempo.hot_update_scene", text="Fog", icon="MOD_FLUIDSIM")
        op.mode = "FOG"
        op = row.operator("spaziotempo.hot_update_scene", text="Physics", icon="PHYSICS")
        op.mode = "PHYSICS"
        op = box.operator(
            "spaziotempo.hot_update_scene", text="Hot Update All", icon="FILE_REFRESH"
        )
        op.mode = "ALL"

        row = box.row(align=True)
        row.operator("spaziotempo.rebuild_restart_check", icon="VIEWZOOM")
        row.operator("spaziotempo.optimizer_check", icon="SETTINGS")

        row = layout.row(align=True)
        row.operator("spaziotempo.save_tuning_preset", icon="FILE_TICK")
        row.operator("spaziotempo.load_tuning_preset", icon="FILE_REFRESH")

        layout.operator("spaziotempo.open_tuning_guide", icon="TEXT")

        box = layout.box()
        box.label(text="Hero / Aura")
        box.prop(tune, "hero_scale")
        box.prop(tune, "hero_deform")
        box.prop(tune, "hero_fine_deform")
        box.prop(tune, "hero_wave")
        box.prop(tune, "hero_twist")
        box.prop(tune, "hero_mat_emission")
        box.prop(tune, "hero_mat_bump")
        box.prop(tune, "hero_mat_roughness")
        box.prop(tune, "hero_mat_noise")
        box.prop(tune, "aura_deform")
        box.prop(tune, "aura_detail")
        box.prop(tune, "aura_pulse")

        box = layout.box()
        box.label(text="Fog")
        box.prop(tune, "fog_density")
        box.prop(tune, "fog_emission")
        box.prop(tune, "fog_noise_scale")
        box.prop(tune, "fog_scale_xy")
        box.prop(tune, "fog_scale_z")
        box.prop(tune, "show_fog_cube")

        box = layout.box()
        box.label(text="Backdrop / Floor")
        box.prop(tune, "backdrop_emission")
        box.prop(tune, "backdrop_noise_scale")
        box.prop(tune, "backdrop_scale")
        box.prop(tune, "floor_scale")
        box.prop(tune, "show_backdrop")
        box.prop(tune, "render_backdrop")
        box.prop(tune, "show_floor")
        box.prop(tune, "render_floor")

        box = layout.box()
        box.label(text="Camera / Render")
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="Preview")
        op.profile = "PREVIEW"
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1080p")
        op.profile = "YOUTUBE_FAST_1080P"
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1440p")
        op.profile = "YOUTUBE_FAST_1440P"
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 4K")
        op.profile = "YOUTUBE_FAST_4K"
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1080p")
        op.profile = "YOUTUBE_1080P"
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1440p")
        op.profile = "YOUTUBE_1440P"
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 4K")
        op.profile = "YOUTUBE_4K"
        box.prop(tune, "runtime_profile")
        box.prop(tune, "youtube_final")
        box.prop(tune, "camera_fstop")
        box.prop(tune, "motion_blur")
        box.prop(tune, "rhythm_light_power")
        box.prop(tune, "compositor_glow")
        box.prop(tune, "compositor_lens")
        box.operator(
            "spaziotempo.load_image_sequence", text="Load Frames + Audio", icon="FILE_MOVIE"
        )
        box.operator("spaziotempo.encode_ffmpeg", text="Encode MP4 FFmpeg", icon="FILE_MOVIE")
        box.operator("spaziotempo.encode_ffmpeg_shell", text="Encode FFmpeg Shell", icon="CONSOLE")

        box = layout.box()
        box.label(text="Scale Existing Animation")
        box.prop(tune, "anim_hero_deform_factor")
        box.prop(tune, "anim_aura_factor")
        box.operator("spaziotempo.scale_animation", icon="GRAPH")

        box = layout.box()
        box.label(text="Select")
        row = box.row(align=True)
        op = row.operator("spaziotempo.select_group", text="Hero")
        op.group = "hero"
        op = row.operator("spaziotempo.select_group", text="Fog")
        op.group = "fog"


classes = (
    ST_TuningSettings,
    ST_OT_apply_tuning,
    ST_OT_keyframe_tuning,
    ST_OT_scale_animation,
    ST_OT_apply_runtime_profile,
    ST_OT_hot_update_scene,
    ST_OT_rebuild_restart_check,
    ST_OT_optimizer_check,
    ST_OT_load_image_sequence,
    ST_OT_encode_ffmpeg,
    ST_OT_encode_ffmpeg_shell,
    ST_OT_save_preset,
    ST_OT_load_preset,
    ST_OT_open_guide_text,
    ST_OT_select_group,
    ST_PT_tuning_panel,
)


def register():
    if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
        del bpy.types.Scene.spaziotempo_tuning

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.spaziotempo_tuning = PointerProperty(type=ST_TuningSettings)


def unregister():
    if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
        del bpy.types.Scene.spaziotempo_tuning
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
