# Local Workstation Target

## Hardware

CPU: Intel Core Ultra 9 285K, 24 cores, 24 logical processors.

GPU: NVIDIA GeForce RTX 5080, driver 595.79, CUDA 13.2, 16303 MiB VRAM from nvidia-smi.

Integrated GPU: Intel Graphics, driver 32.0.101.8132.

RAM: 32 GB reported by user.

NPU: expected available on Intel Core Ultra platform.

## Software notes

Python launcher: 3.14.4.

The pipeline dry run used a WindowsApps Python 3.12 executable, so interpreter choice should be kept explicit while debugging.

Blender version reported by user: 5.1.

The `blender` command is not currently available in PATH.

## Pipeline policy

CPU lane: parsing, validation, orchestration, compact JSON generation.

NPU lane: short reviews, scoring, classification, checklist passes. Recommended maximum workers: 4.

GPU lane: heavy generation, optional planner command, Blender rendering when large model inference is not running.

Avoid heavy Blender rendering and large local model inference at the same time on the current 32 GB RAM profile.
