"""Bundled-app entry point — imports the package so relative imports work."""

from photopick.ui.app import main

if __name__ == "__main__":
    raise SystemExit(main())
