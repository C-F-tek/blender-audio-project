class ST_TuningSettings(bpy.types.PropertyGroup):
    hero_scale: FloatProperty(name="Hero scale", default=1.0, min=0.20, max=3.0, precision=3)
    hero_deform: FloatProperty(name="Hero deform", default=1.0, min=0.0, max=4.0, precision=3)
    hero_fine_deform: FloatProperty(name="Hero fine", default=1.0, min=0.0, max=4.0, precision=3)
    hero_wave: FloatProperty(name="Hero wave", default=1.0, min=0.0, max=4.0, precision=3)
    hero_twist: FloatProperty(name="Hero twist", default=1.0, min=0.0, max=4.0, precision=3)
    hero_mat_emission: FloatProperty(
        name="Hero material light", default=1.0, min=0.0, max=4.0, precision=3
    )
    hero_mat_bump: FloatProperty(
        name="Hero material bump", default=1.0, min=0.0, max=4.0, precision=3
    )
    hero_mat_roughness: FloatProperty(
        name="Hero material rough", default=1.0, min=0.10, max=2.0, precision=3
    )
    hero_mat_noise: FloatProperty(
        name="Hero material noise", default=1.0, min=0.10, max=4.0, precision=3
    )

    aura_deform: FloatProperty(name="Aura deform", default=0.45, min=0.0, max=1.0, precision=3)
    aura_detail: FloatProperty(name="Aura detail", default=0.35, min=0.0, max=1.0, precision=3)
    aura_pulse: FloatProperty(name="Aura pulse", default=0.35, min=0.0, max=1.0, precision=3)

    fog_density: FloatProperty(name="Fog density", default=0.035, min=0.0, max=0.55, precision=4)
    fog_emission: FloatProperty(name="Fog emission", default=0.004, min=0.0, max=0.12, precision=4)
    fog_noise_scale: FloatProperty(name="Fog noise", default=0.9, min=0.10, max=12.0, precision=3)
    fog_scale_xy: FloatProperty(name="Fog XY", default=1.0, min=0.20, max=2.20, precision=3)
    fog_scale_z: FloatProperty(name="Fog Z", default=1.0, min=0.20, max=2.40, precision=3)

    backdrop_emission: FloatProperty(
        name="Backdrop light", default=0.175, min=0.0, max=0.80, precision=4
    )
    backdrop_noise_scale: FloatProperty(
        name="Backdrop noise", default=2.4, min=0.10, max=12.0, precision=3
    )
    backdrop_scale: FloatProperty(
        name="Backdrop scale", default=1.0, min=0.20, max=2.40, precision=3
    )
    floor_scale: FloatProperty(name="Floor scale", default=1.0, min=0.20, max=3.0, precision=3)

    camera_fstop: FloatProperty(name="Camera f-stop", default=6.5, min=1.0, max=16.0, precision=2)
    rhythm_light_power: FloatProperty(
        name="Accent emission", default=1.0, min=0.0, max=4.0, precision=3
    )
    compositor_glow: FloatProperty(
        name="Compositor glow", default=1.0, min=0.10, max=4.0, precision=3
    )
    compositor_lens: FloatProperty(
        name="Compositor lens", default=1.0, min=0.0, max=4.0, precision=3
    )

    particle_size: FloatProperty(name="Particle size", default=1.0, min=0.05, max=5.0, precision=3)
    particle_force: FloatProperty(name="Particle force", default=1.0, min=0.0, max=5.0, precision=3)
    letter_source_scale: FloatProperty(
        name="Letter source scale", default=1.0, min=0.10, max=3.0, precision=3
    )

    anim_hero_deform_factor: FloatProperty(
        name="Anim hero deform", default=1.0, min=0.0, max=4.0, precision=3
    )
    anim_aura_factor: FloatProperty(name="Anim aura", default=1.0, min=0.0, max=4.0, precision=3)
    anim_particle_size_factor: FloatProperty(
        name="Anim particle size", default=1.0, min=0.05, max=5.0, precision=3
    )
    anim_particle_force_factor: FloatProperty(
        name="Anim particle force", default=1.0, min=0.0, max=5.0, precision=3
    )

    show_fog_cube: BoolProperty(name="Show fog cube", default=False)
    show_backdrop: BoolProperty(name="Show backdrop", default=True)
    render_backdrop: BoolProperty(name="Render backdrop", default=True)
    show_floor: BoolProperty(name="Show floor", default=True)
    render_floor: BoolProperty(name="Render floor", default=False)
    show_emitters: BoolProperty(name="Show emitters", default=False)
    show_particle_sources: BoolProperty(name="Show source objects", default=False)
    motion_blur: BoolProperty(name="Motion blur", default=False)
    youtube_final: BoolProperty(name="YouTube final", default=False)
    runtime_profile: StringProperty(name="Runtime profile", default="Preview")


class ST_OT_apply_tuning(bpy.types.Operator):
    bl_idname = "spaziotempo.apply_tuning"
    bl_label = "Apply Live Values"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        apply_tuning(context, insert_keyframes=False)
        self.report({"INFO"}, "Spaziotempo tuning applied to current scene.")
        return {"FINISHED"}


class ST_OT_keyframe_tuning(bpy.types.Operator):
    bl_idname = "spaziotempo.keyframe_tuning"
    bl_label = "Apply + Keyframe"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        apply_tuning(context, insert_keyframes=True)
        self.report(
            {"INFO"}, f"Spaziotempo values keyframed at frame {context.scene.frame_current}."
        )
        return {"FINISHED"}


class ST_OT_scale_animation(bpy.types.Operator):
    bl_idname = "spaziotempo.scale_animation"
    bl_label = "Scale Existing FCurves"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        changed = scale_full_animation(context)
        self.report({"INFO"}, f"Scaled {changed} keyframe values.")
        return {"FINISHED"}


class ST_OT_apply_runtime_profile(bpy.types.Operator):
    bl_idname = "spaziotempo.apply_runtime_profile"
    bl_label = "Apply Runtime Profile"
    bl_options = {"REGISTER", "UNDO"}

    final_for_youtube: bpy.props.BoolProperty(default=False)
    profile: bpy.props.StringProperty(default="")

    def execute(self, context):
        profile = self.profile or ("YOUTUBE_4K" if self.final_for_youtube else "PREVIEW")
        apply_runtime_profile(context, profile)
        label = runtime_profile_label(profile)
        self.report({"INFO"}, f"{label} profile applied to current scene.")
        return {"FINISHED"}


class ST_OT_hot_update_scene(bpy.types.Operator):
    bl_idname = "spaziotempo.hot_update_scene"
    bl_label = "Hot Update Scene"
    bl_options = {"REGISTER", "UNDO"}

    mode: bpy.props.StringProperty(default="ALL")

    def execute(self, context):
        if not HOT_UPDATE_PATH.exists():
            self.report({"WARNING"}, f"Hot update script not found: {HOT_UPDATE_PATH}")
            return {"CANCELLED"}

        try:
            code = compile(
                HOT_UPDATE_PATH.read_text(encoding="utf-8"), str(HOT_UPDATE_PATH), "exec"
            )
            exec(
                code,
                {
                    "__file__": str(HOT_UPDATE_PATH),
                    "__name__": "__main__",
                    "HOTPATCH_MODE": self.mode,
                },
            )
        except Exception as exc:
            traceback.print_exc()
            self.report({"ERROR"}, f"Hot update failed: {exc}")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Hot update {self.mode} complete.")
        return {"FINISHED"}


class ST_OT_rebuild_restart_check(bpy.types.Operator):
    bl_idname = "spaziotempo.rebuild_restart_check"
    bl_label = "Rebuild / Restart Check"
    bl_options = {"REGISTER"}

    def execute(self, context):
        try:
            sys.modules.pop("hotpatch.diagnostics", None)
            from hotpatch.diagnostics import analyze_rebuild_need

            result = analyze_rebuild_need()
        except Exception as exc:
            traceback.print_exc()
            self.report({"ERROR"}, f"Check failed: {exc}")
            return {"CANCELLED"}

        if result["blocking"]:
            self.report({"WARNING"}, "Full rebuild needed. See SPAZIOTEMPO_REBUILD_CHECK.")
        elif result["restart"]:
            self.report({"WARNING"}, "Registration issue found. See SPAZIOTEMPO_REBUILD_CHECK.")
        else:
            self.report({"INFO"}, "Hotpatch should be enough. See SPAZIOTEMPO_REBUILD_CHECK.")
        return {"FINISHED"}


class ST_OT_optimizer_check(bpy.types.Operator):
    bl_idname = "spaziotempo.optimizer_check"
    bl_label = "Optimizer Check"
    bl_options = {"REGISTER"}

    def execute(self, context):
        try:
            sys.modules.pop("hotpatch.diagnostics", None)
            from hotpatch.diagnostics import analyze_optimizer

            result = analyze_optimizer()
        except Exception as exc:
            traceback.print_exc()
            self.report({"ERROR"}, f"Optimizer check failed: {exc}")
            return {"CANCELLED"}

        if result["warnings"]:
            self.report(
                {"WARNING"}, "Cache/bake suggestions found. See SPAZIOTEMPO_OPTIMIZER_REPORT."
            )
        else:
            self.report({"INFO"}, "No required bake found. See SPAZIOTEMPO_OPTIMIZER_REPORT.")
        return {"FINISHED"}


class ST_OT_load_image_sequence(bpy.types.Operator):
    bl_idname = "spaziotempo.load_image_sequence"
    bl_label = "Load Image Sequence"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if not ENCODE_SEQUENCE_PATH.exists():
            self.report({"WARNING"}, f"Image sequence script not found: {ENCODE_SEQUENCE_PATH}")
            return {"CANCELLED"}

        try:
            code = compile(
                ENCODE_SEQUENCE_PATH.read_text(encoding="utf-8"), str(ENCODE_SEQUENCE_PATH), "exec"
            )
            exec(code, {"__file__": str(ENCODE_SEQUENCE_PATH), "__name__": "__main__"})
        except Exception as exc:
            traceback.print_exc()
            self.report({"ERROR"}, f"Image sequence load failed: {exc}")
            return {"CANCELLED"}

        self.report({"INFO"}, "Image sequence + audio loaded in Video Sequencer.")
        return {"FINISHED"}


class ST_OT_encode_ffmpeg(bpy.types.Operator):
    bl_idname = "spaziotempo.encode_ffmpeg"
    bl_label = "Encode MP4 FFmpeg"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if not ENCODE_FFMPEG_PATH.exists():
            self.report({"WARNING"}, f"FFmpeg encode script not found: {ENCODE_FFMPEG_PATH}")
            return {"CANCELLED"}

        try:
            code = compile(
                ENCODE_FFMPEG_PATH.read_text(encoding="utf-8"), str(ENCODE_FFMPEG_PATH), "exec"
            )
            exec(code, {"__file__": str(ENCODE_FFMPEG_PATH), "__name__": "__main__"})
        except Exception as exc:
            traceback.print_exc()
            self.report({"ERROR"}, f"FFmpeg encode failed: {exc}")
            return {"CANCELLED"}

        self.report({"INFO"}, "FFmpeg MP4 encoded from image sequence.")
        return {"FINISHED"}


class ST_OT_encode_ffmpeg_shell(bpy.types.Operator):
    bl_idname = "spaziotempo.encode_ffmpeg_shell"
    bl_label = "Encode MP4 FFmpeg Shell"
    bl_options = {"REGISTER"}

    def execute(self, context):
        if not ENCODE_FFMPEG_PATH.exists():
            self.report({"WARNING"}, f"FFmpeg encode script not found: {ENCODE_FFMPEG_PATH}")
            return {"CANCELLED"}

        try:
            code = compile(
                ENCODE_FFMPEG_PATH.read_text(encoding="utf-8"), str(ENCODE_FFMPEG_PATH), "exec"
            )
            exec(
                code,
                {
                    "__file__": str(ENCODE_FFMPEG_PATH),
                    "__name__": "__main__",
                    "FFMPEG_LAUNCH_VISIBLE_SHELL": True,
                },
            )
        except Exception as exc:
            traceback.print_exc()
            self.report({"ERROR"}, f"FFmpeg shell encode failed: {exc}")
            return {"CANCELLED"}

        self.report({"INFO"}, "FFmpeg encode launched in external shell.")
        return {"FINISHED"}


class ST_OT_save_preset(bpy.types.Operator):
    bl_idname = "spaziotempo.save_tuning_preset"
    bl_label = "Save Preset"

    def execute(self, context):
        data = preset_data(context.scene.spaziotempo_tuning)
        PRESET_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.report({"INFO"}, f"Preset saved: {PRESET_PATH}")
        return {"FINISHED"}


class ST_OT_load_preset(bpy.types.Operator):
    bl_idname = "spaziotempo.load_tuning_preset"
    bl_label = "Load Preset"

    def execute(self, context):
        if not PRESET_PATH.exists():
            self.report({"WARNING"}, f"Preset not found: {PRESET_PATH}")
            return {"CANCELLED"}

        data = json.loads(PRESET_PATH.read_text(encoding="utf-8"))
        load_preset_data(context.scene.spaziotempo_tuning, data)
        apply_tuning(context, insert_keyframes=False)
        self.report({"INFO"}, "Preset loaded and applied.")
        return {"FINISHED"}


class ST_OT_open_guide_text(bpy.types.Operator):
    bl_idname = "spaziotempo.open_tuning_guide"
    bl_label = "Open Editable Guide"

    def execute(self, context):
        text_name = "SPAZIOTEMPO_TUNING_GUIDE"
        guide = bpy.data.texts.get(text_name) or bpy.data.texts.new(text_name)

        if GUIDE_PATH.exists():
            body = GUIDE_PATH.read_text(encoding="utf-8")
        else:
            body = "Spaziotempo tuning guide not found."

        guide.clear()
        guide.write(body)
        self.report({"INFO"}, f"Guide opened as Blender text block: {text_name}")
        return {"FINISHED"}
