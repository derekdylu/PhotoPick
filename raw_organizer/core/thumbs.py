"""Lazy thumbnail extraction with an on-disk cache.

Thumbnails are decoded only on demand. RAW files use the embedded JPEG preview
(via rawpy) so we never decode the full sensor data.
"""

from __future__ import annotations

import hashlib
import io
import shutil
from pathlib import Path

from .matcher import is_jpg, is_raw

THUMB_SIZE = 512  # max edge in px

_CACHE_ROOT = Path.home() / "Library" / "Caches" / "RawOrganizer" / "thumbs"


def cache_root() -> Path:
    return _CACHE_ROOT


def _cache_key(path: Path) -> str:
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        mtime = 0
    h = hashlib.sha1(f"{path}|{mtime}".encode("utf-8")).hexdigest()
    return h


def _cache_path(path: Path) -> Path:
    return _CACHE_ROOT / f"{_cache_key(path)}.jpg"


def get_thumb_bytes(path: Path) -> bytes | None:
    """Return JPEG bytes for a thumbnail of the given file. None on failure."""
    cached = _cache_path(path)
    if cached.exists():
        try:
            return cached.read_bytes()
        except OSError:
            pass

    data = _decode(path)
    if data is None:
        return None

    try:
        _CACHE_ROOT.mkdir(parents=True, exist_ok=True)
        tmp = cached.with_suffix(".jpg.tmp")
        tmp.write_bytes(data)
        tmp.replace(cached)
    except OSError:
        # Cache write failure is non-fatal — still return the bytes.
        pass
    return data


def _decode(path: Path) -> bytes | None:
    if is_jpg(path):
        return _decode_jpg(path)
    if is_raw(path):
        return _decode_raw(path)
    return None


def _decode_jpg(path: Path) -> bytes | None:
    try:
        from PIL import Image
    except ImportError:
        # Fallback: just hand back the file as-is.
        try:
            return path.read_bytes()
        except OSError:
            return None
    try:
        with Image.open(path) as im:
            im.thumbnail((THUMB_SIZE, THUMB_SIZE))
            buf = io.BytesIO()
            im.convert("RGB").save(buf, format="JPEG", quality=85)
            return buf.getvalue()
    except Exception:
        return None


def _decode_raw(path: Path) -> bytes | None:
    try:
        import rawpy
    except ImportError:
        return None
    try:
        with rawpy.imread(str(path)) as raw:
            try:
                thumb = raw.extract_thumb()
            except rawpy.LibRawNoThumbnailError:
                return None
            except rawpy.LibRawUnsupportedThumbnailError:
                return None

        if thumb.format == rawpy.ThumbFormat.JPEG:
            data = thumb.data
        else:
            # Bitmap thumbnail — re-encode as JPEG via PIL if available.
            try:
                from PIL import Image
            except ImportError:
                return None
            im = Image.fromarray(thumb.data)
            im.thumbnail((THUMB_SIZE, THUMB_SIZE))
            buf = io.BytesIO()
            im.convert("RGB").save(buf, format="JPEG", quality=85)
            data = buf.getvalue()

        # Downscale embedded JPEG previews if they're huge.
        try:
            from PIL import Image
            with Image.open(io.BytesIO(data)) as im:
                if max(im.size) > THUMB_SIZE:
                    im.thumbnail((THUMB_SIZE, THUMB_SIZE))
                    buf = io.BytesIO()
                    im.convert("RGB").save(buf, format="JPEG", quality=85)
                    data = buf.getvalue()
        except Exception:
            pass

        return data
    except Exception:
        return None


def clear_cache() -> int:
    """Remove the on-disk thumbnail cache. Returns number of files deleted."""
    if not _CACHE_ROOT.exists():
        return 0
    count = sum(1 for _ in _CACHE_ROOT.iterdir() if _.is_file())
    shutil.rmtree(_CACHE_ROOT, ignore_errors=True)
    _CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    return count


def cache_size_bytes() -> int:
    if not _CACHE_ROOT.exists():
        return 0
    total = 0
    for p in _CACHE_ROOT.iterdir():
        try:
            total += p.stat().st_size
        except OSError:
            pass
    return total
