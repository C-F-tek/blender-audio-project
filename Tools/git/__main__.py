"""Module entrypoint for ``python -m Tools.git``."""

from __future__ import annotations

from Tools.git.dispatch import main


if __name__ == "__main__":
    raise SystemExit(main())
