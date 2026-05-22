"""Compatibility entrypoint delegating to IA-Carmine Core Runtime."""

from __future__ import annotations

from ia_carmine.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
