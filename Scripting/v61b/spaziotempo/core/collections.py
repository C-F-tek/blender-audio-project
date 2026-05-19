"""Scene collection and object classification helpers."""

import bpy

from .registry import (
    EXACT_OBJECT_LAYERS,
    LAYER_ORDER,
    LAYER_SPECS,
    PARENT_LAYER_HINTS,
    PREFIX_OBJECT_LAYERS,
    PROJECT_ROOT_COLLECTION,
    STRUCTURE_VERSION,
    TYPE_FALLBACK_LAYERS,
)


def _children_by_name(collection):
    return {child.name: child for child in collection.children}


def _objects_by_name(collection):
    return {obj.name: obj for obj in collection.objects}


def ensure_child_collection(parent, name):
    existing = bpy.data.collections.get(name)
    collection = existing or bpy.data.collections.new(name)
    if name not in _children_by_name(parent):
        parent.children.link(collection)
    return collection


def ensure_project_collections(scene=None, include_reserved=True):
    scene = scene or bpy.context.scene
    project = ensure_child_collection(scene.collection, PROJECT_ROOT_COLLECTION)
    project["st_structure_version"] = STRUCTURE_VERSION

    collections = {}
    for key in LAYER_ORDER:
        spec = LAYER_SPECS[key]
        if spec.reserved and not include_reserved:
            continue
        collection = ensure_child_collection(project, spec.collection)
        collection["st_key"] = spec.key
        collection["st_family"] = spec.family
        collection["st_layer"] = spec.layer
        collection["st_feature"] = spec.feature
        collection["st_reserved"] = bool(spec.reserved)
        collections[key] = collection

    return collections


def _parent_hint(obj):
    parent = getattr(obj, "parent", None)
    while parent is not None:
        hint = PARENT_LAYER_HINTS.get(parent.name)
        if hint is not None:
            return hint
        parent = getattr(parent, "parent", None)
    return None


def classify_object(obj):
    name = obj.name

    exact = EXACT_OBJECT_LAYERS.get(name)
    if exact is not None:
        return exact

    for prefix, layer_key in PREFIX_OBJECT_LAYERS:
        if name.startswith(prefix):
            return layer_key

    hint = _parent_hint(obj)
    if hint is not None:
        return hint

    type_hint = TYPE_FALLBACK_LAYERS.get(getattr(obj, "type", ""))
    if type_hint is not None:
        return type_hint

    return "technical"


def link_object_to_layer(obj, collection):
    if obj.name not in _objects_by_name(collection):
        collection.objects.link(obj)


def apply_object_metadata(obj, spec):
    obj["st_family"] = spec.family
    obj["st_layer"] = spec.layer
    obj["st_feature"] = spec.feature
    obj["st_collection"] = spec.collection
    obj["st_structure_version"] = STRUCTURE_VERSION


def classify_scene_objects(scene=None, include_reserved=True):
    scene = scene or bpy.context.scene
    collections = ensure_project_collections(scene, include_reserved=include_reserved)
    counts = {key: 0 for key in LAYER_ORDER if key in collections}
    objects_classified = 0

    for obj in scene.objects:
        layer_key = classify_object(obj)
        if layer_key not in collections:
            collections[layer_key] = ensure_project_collections(scene, include_reserved=True)[
                layer_key
            ]
            counts.setdefault(layer_key, 0)

        spec = LAYER_SPECS[layer_key]
        link_object_to_layer(obj, collections[layer_key])
        apply_object_metadata(obj, spec)
        counts[layer_key] = counts.get(layer_key, 0) + 1
        objects_classified += 1

    return {
        "root_collection": PROJECT_ROOT_COLLECTION,
        "structure_version": STRUCTURE_VERSION,
        "objects_classified": objects_classified,
        "counts": counts,
        "collections": {key: coll.name for key, coll in collections.items()},
    }


def compact_structure_summary(report):
    parts = []
    for key in LAYER_ORDER:
        count = report.get("counts", {}).get(key, 0)
        if count:
            parts.append(f"{LAYER_SPECS[key].collection}={count}")
    return ", ".join(parts) if parts else "no classified objects"
