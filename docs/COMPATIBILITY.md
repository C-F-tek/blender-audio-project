# Compatibility

## Blender

Exact supported Blender versions are not specified yet.

The project should document compatibility per script, especially when Blender API changes affect node types, render settings, or EEVEE and Cycles options.

## Python

Python version is tied to the Blender version in most workflows.

External Python interpreter compatibility is not specified yet.

## Operating systems

Known workstation context may include Windows-based Blender usage, but cross-platform support is not specified yet.

## Known compatibility risk areas

- removed or renamed Blender shader nodes;
- render engine enum changes;
- EEVEE and Cycles API differences;
- local absolute paths;
- GPU and CPU render configuration differences;
- audio strip and VSE API changes.

## Documentation rule

Do not mark a Blender version as supported until it has been tested.
