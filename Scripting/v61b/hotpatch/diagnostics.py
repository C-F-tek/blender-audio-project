import bpy

from .common import ANALYSIS_JSON_PATH, cfg_value, load_analysis
from spaziotempo.core.registry import LAYER_ORDER, LAYER_SPECS, PROJECT_ROOT_COLLECTION


STRUCTURAL_OBJECTS = [
    "HeroRoot",
    "MainCamera",
    "CameraTarget",
    "AtmosphereCube",
    "FogPulseController",
    "SoftRhythmBackdrop",
]


def text_report(name, lines):
    text = bpy.data.texts.get(name) or bpy.data.texts.new(name)
    text.clear()
    text.write("\n".join(lines))
    return text


def has_object(name):
    return bpy.data.objects.get(name) is not None


def count_objects(prefix):
    return sum(1 for obj in bpy.data.objects if obj.name.startswith(prefix))


def collection_exists(name):
    return bpy.data.collections.get(name) is not None


def layer_collection_counts():
    counts = {}
    for key in LAYER_ORDER:
        spec = LAYER_SPECS[key]
        collection = bpy.data.collections.get(spec.collection)
        counts[key] = len(collection.objects) if collection is not None else 0
    return counts


def scene_frame_count(scene):
    return max(0, int(scene.frame_end) - int(scene.frame_start) + 1)


def material_node_exists(node_name):
    for mat in bpy.data.materials:
        if mat is not None and mat.use_nodes and mat.node_tree.nodes.get(node_name) is not None:
            return True
    return False


def modifier_exists(mod_name):
    for obj in bpy.data.objects:
        for mod in obj.modifiers:
            if mod.name == mod_name:
                return True
    return False


def point_cache_state(cache):
    if cache is None:
        return "no-cache"
    if getattr(cache, "is_baked", False):
        return "baked"
    return "not-baked"


def particle_cache_state(ps):
    cache = getattr(ps, "point_cache", None)
    if cache is None:
        return "no-cache"
    if getattr(cache, "is_baked", False):
        return "baked"
    if getattr(cache, "use_disk_cache", False):
        return "disk-cache-on"
    return "not-baked"


def analyze_rebuild_need():
    scene = bpy.context.scene
    _, frames = load_analysis()
    expected_frames = len(frames)
    current_frames = scene_frame_count(scene)

    blocking = []
    warnings = []
    ok = []

    for name in STRUCTURAL_OBJECTS:
        if has_object(name):
            ok.append(f"OK object: {name}")
        else:
            blocking.append(f"Missing structural object `{name}`: run `main_v61b.py`.")

    if count_objects("PhysicsAccent_") == 0:
        warnings.append("No `PhysicsAccent_*` objects found: Physics hotpatch has nothing to update.")
    else:
        ok.append(f"OK PhysicsAccent objects: {count_objects('PhysicsAccent_')}")

    if not modifier_exists("HeroAudioMeshDisplace"):
        warnings.append("Hero mesh deform modifier missing: run full rebuild if you expect mesh deformation.")
    else:
        ok.append("OK hero mesh deform modifier")

    if not material_node_exists("HeroMatEmissionValue"):
        warnings.append("Hero audio material nodes missing: use Hot Update Materials or full rebuild.")
    else:
        ok.append("OK hero material nodes")

    if expected_frames and current_frames != expected_frames:
        blocking.append(
            f"Frame count mismatch: scene has {current_frames}, analysis has {expected_frames}. Run `main_v61b.py`."
        )
    elif expected_frames:
        ok.append(f"OK frame count: {current_frames}")
    else:
        warnings.append(f"Analysis file not loaded/found: {ANALYSIS_JSON_PATH}")

    if not has_object("HeroGravityField") and has_object("PulseForceField"):
        warnings.append("Old `PulseForceField` found: Hot Update Physics can rename/update it.")
    elif not has_object("HeroGravityField"):
        warnings.append("No `HeroGravityField`: Hot Update Physics can create it, full rebuild creates it cleanly.")
    else:
        ok.append("OK HeroGravityField")

    if collection_exists(PROJECT_ROOT_COLLECTION):
        ok.append(f"OK layer root collection: {PROJECT_ROOT_COLLECTION}")
    else:
        warnings.append("Layer collections missing: use Hot Update All or rebuild with updated `main_v61b.py`.")

    restart = []
    if not hasattr(bpy.types.Scene, "spaziotempo_tuning"):
        restart.append("Panel properties not registered: run `scene_tuning_panel.py` or rebuild with updated `main_v61b.py`.")

    lines = [
        "SPAZIOTEMPO REBUILD / RESTART CHECK",
        "=" * 52,
        f"Result: {'FULL REBUILD NEEDED' if blocking else 'HOTPATCH SHOULD BE ENOUGH'}",
        "",
    ]
    if blocking:
        lines.append("Full rebuild triggers:")
        lines.extend(f"- {item}" for item in blocking)
        lines.append("")
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"- {item}" for item in warnings)
        lines.append("")
    if restart:
        lines.append("Registration/restart notes:")
        lines.extend(f"- {item}" for item in restart)
        lines.append("")
    lines.append("Checked OK:")
    lines.extend(f"- {item}" for item in ok)

    text_report("SPAZIOTEMPO_REBUILD_CHECK", lines)
    return {
        "blocking": blocking,
        "warnings": warnings,
        "restart": restart,
        "report": "\n".join(lines),
    }


def analyze_optimizer():
    scene = bpy.context.scene
    warnings = []
    suggestions = []
    ok = []

    particle_systems = []
    for obj in bpy.data.objects:
        for mod in obj.modifiers:
            if mod.type == 'PARTICLE_SYSTEM':
                ps = getattr(mod, "particle_system", None)
                if ps is not None:
                    particle_systems.append((obj, ps, mod))

    if particle_systems:
        unbaked = []
        for obj, ps, _ in particle_systems:
            state = particle_cache_state(ps)
            settings = getattr(ps, "settings", None)
            physics_type = getattr(settings, "physics_type", "")
            if state != "baked" and physics_type not in {"NO", "NONE", ""}:
                unbaked.append(f"{obj.name} / {ps.name}: {state}, physics={physics_type}")
        if unbaked:
            warnings.append("Particle systems with simulation are not baked/cache-confirmed.")
            suggestions.extend(f"Bake or disk-cache particle system: {item}" for item in unbaked)
        else:
            ok.append(f"Particle systems checked: {len(particle_systems)}")
    else:
        ok.append("No particle systems active")

    rb_world = getattr(scene, "rigidbody_world", None)
    active_rigid = [
        obj for obj in bpy.data.objects
        if getattr(obj, "rigid_body", None) is not None
        and obj.rigid_body.type == 'ACTIVE'
        and not getattr(obj.rigid_body, "kinematic", False)
    ]
    if active_rigid:
        state = point_cache_state(getattr(rb_world, "point_cache", None) if rb_world else None)
        if state != "baked":
            warnings.append(f"{len(active_rigid)} active rigid bodies are dynamic and rigid body cache is {state}.")
            suggestions.append("Bake rigid body cache before final render or make those bodies kinematic/keyframed.")
        else:
            ok.append("Rigid body cache baked")
    else:
        ok.append("No unbaked dynamic rigid bodies detected")

    sim_mods = []
    for obj in bpy.data.objects:
        for mod in obj.modifiers:
            if mod.type in {"CLOTH", "FLUID", "SOFT_BODY", "DYNAMIC_PAINT"}:
                sim_mods.append(f"{obj.name} / {mod.name} ({mod.type})")
    if sim_mods:
        warnings.append("Simulation modifiers found.")
        suggestions.extend(f"Check/bake cache: {item}" for item in sim_mods)
    else:
        ok.append("No cloth/fluid/soft-body simulation modifiers")

    output_mode = str(cfg_value("RENDER_OUTPUT_MODE", "")).upper()
    if output_mode == "IMAGE_SEQUENCE":
        ok.append("Image sequence output active: good for long renders and resume workflow")
    else:
        suggestions.append("For long final renders, IMAGE_SEQUENCE is safer than direct MP4.")

    if bool(cfg_value("FOG_VOLUME_ENABLED", False)):
        suggestions.append("Volumetric fog is enabled: use fog filaments for faster renders and fewer square artifacts.")
    else:
        ok.append("Volumetric fog disabled: fog filaments should avoid Eevee grid artifacts")

    if bool(cfg_value("ENCODE_USE_EXTERNAL_FFMPEG", False)):
        ok.append("External ffmpeg encode enabled: better MP4 quality for fog/gradients")

    counts = layer_collection_counts()
    if any(counts.values()):
        visible_counts = [
            f"{LAYER_SPECS[key].collection}={count}"
            for key, count in counts.items()
            if count
        ]
        ok.append("Layer classification: " + ", ".join(visible_counts))
    else:
        suggestions.append("Run Hot Update All once to populate ST_* layer collections and object metadata.")

    render = scene.render
    if getattr(render, "use_motion_blur", False):
        suggestions.append("Motion blur is on: highest visual cost after volumetrics. Use YT Fast profiles for tests.")

    eevee = getattr(scene, "eevee", None)
    if eevee is not None and hasattr(eevee, "volumetric_samples"):
        samples = int(eevee.volumetric_samples)
        if samples > 48:
            suggestions.append(f"Volumetric samples are {samples}: consider 48 final / 24 fast.")
        else:
            ok.append(f"Volumetric samples: {samples}")

    lines = [
        "SPAZIOTEMPO OPTIMIZER CHECK",
        "=" * 52,
        f"Result: {'CHECK CACHE / BAKE' if warnings else 'NO REQUIRED BAKE FOUND'}",
        "",
    ]
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"- {item}" for item in warnings)
        lines.append("")
    if suggestions:
        lines.append("Suggestions:")
        lines.extend(f"- {item}" for item in suggestions)
        lines.append("")
    lines.append("Checked OK:")
    lines.extend(f"- {item}" for item in ok)

    text_report("SPAZIOTEMPO_OPTIMIZER_REPORT", lines)
    return {
        "warnings": warnings,
        "suggestions": suggestions,
        "report": "\n".join(lines),
    }
