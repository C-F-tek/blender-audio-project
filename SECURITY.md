# Security Policy

## Supported versions

Supported versions are not specified yet.

## Reporting

For now, report security-relevant issues through the repository issue tracker or directly to the maintainer when a private channel is available.

## Scope

This project is primarily a Blender/Python workflow repository. Security considerations may include:

- unsafe execution of untrusted Python scripts;
- untrusted external assets;
- local path exposure;
- accidental publication of private render, audio, or analysis files.

## Guidance

Do not run scripts from untrusted sources inside Blender. Review file paths, external dependencies, and asset references before execution.
