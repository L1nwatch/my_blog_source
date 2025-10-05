"""Expose project constants when importing from repository root."""
from __future__ import annotations

import importlib.util
import pathlib

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
_SOURCE = _PROJECT_ROOT / "my_blog" / "my_constant.py"

if not _SOURCE.exists():
    raise ImportError(f"Unable to locate my_blog/my_constant.py at {_SOURCE}")

_spec = importlib.util.spec_from_file_location("_my_blog_constants", _SOURCE)
if _spec is None or _spec.loader is None:  # pragma: no cover - defensive
    raise ImportError("Failed to load project constants module")

_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

def __getattr__(name: str):
    return getattr(_module, name)

__all__ = [name for name in dir(_module) if not name.startswith("_")]

for _name in __all__:
    globals()[_name] = getattr(_module, _name)
