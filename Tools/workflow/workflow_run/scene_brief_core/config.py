"""Configuration for scene director brief/chat."""

from __future__ import annotations

MEMORY_VERSION = 4
MAX_SCENE_CHAT_PROMPT_CHARS = 14000

QUESTION_FIELDS = [
    (
        "creative_intent",
        "Idea generale / mood",
        "Che sensazione deve dare la scena?",
        "cinematica, audio-reactive, materia luminosa, spazio profondo non troppo nero",
    ),
    (
        "hero_object",
        "Oggetto centrale",
        "Come deve comportarsi l'oggetto centrale?",
        "sfera/aura viva con deformazione mesh completa su tutti i keyframe audio",
    ),
    (
        "background",
        "Sfondo",
        "Che sfondo vuoi?",
        "azzurro/verde sfumato coerente con cover, niente nero piatto, niente linee/pannelli visibili",
    ),
    (
        "fog",
        "Nebbia",
        "Come deve muoversi la nebbia?",
        "filamenti o banchi morbidi tipo fumo, visibili ma leggeri, compressi/decompressi dal suono",
    ),
    (
        "particles_orbits",
        "Particelle/orbite",
        "Che comportamento vuoi per satelliti/particelle?",
        "orbite attorno al centro come atomo musicale, mini-satelliti, emissione sugli oggetti fisici esistenti",
    ),
    (
        "materials_lights",
        "Materiali/luci",
        "Come devono reagire materiali e luci?",
        "materia + emissione fusi, luce generale stabile, no strobo forte, accenti su oggetti secondari",
    ),
    (
        "camera_motion",
        "Camera",
        "Che tipo di camera vuoi?",
        "movimento lento e musicale, micro pressione sui beat, niente scatti aggressivi",
    ),
    (
        "avoid",
        "Da evitare",
        "Cosa non vuoi vedere?",
        "placeholder, scena vuota, oggetti importati brutti, nero dominante, nebbia squadrettata, perdita di keyframe",
    ),
    (
        "render_target",
        "Target render",
        "A cosa deve stare attento il generatore per i tempi render?",
        "test veloce con NPU spenta, qualita alta ma evitando volumi pesanti e luci globali variabili",
    ),
    ("free_notes", "Note libere", "Aggiungi istruzioni extra per la scena.", ""),
]
