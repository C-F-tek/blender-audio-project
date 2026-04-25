"""Feature catalog facade.

Keep feature-level decisions here so adding a new block, for example water,
does not require hunting through unrelated scene scripts.
"""

from spaziotempo.core.registry import FEATURE_CATALOG, LAYER_SPECS


def get_feature(name):
    return FEATURE_CATALOG.get(name)


def feature_layer(name):
    feature = get_feature(name)
    if feature is None:
        return None
    layer_key = feature["layer"]
    return LAYER_SPECS[layer_key]
