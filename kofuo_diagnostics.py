#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Non-destructive local diagnostics for each KOFUO game launch.

The launcher calls DiagnosticRun before and after the game process. Full logs stay
on this computer; only the bounded, redacted JSON report is copied to an optional
shared-folder outbox for Supa.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_ARCHIVED_LOG_BYTES = 20 * 1024 * 1024
MAX_EXCERPT_LINES = 15
MAX_EXCERPT_LINE_CHARS = 240
ERROR_MARKER = re.compile(
    r"(error detected|failed to load|fatal error|unhandled exception|"
    r"access violation|crash|assertion failed)",
    re.IGNORECASE,
)
SECRET_VALUE = re.compile(
    r"(?i)\b(password|passwd|token|secret|api[_-]?key)\b\s*[:=]\s*\S+"
)
WINDOWS_PATH = re.compile(r"(?i)\b[A-Z]:\\(?:[^\\\r\n\t]+\\)*[^\\\r\n\t]*")
UNC_PATH = re.compile(r"\\\\[^\\\r\n\t]+\\[^\\\r\n\t]+")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def default_diagnostics_dir() -> Path:
    """Return a per-user local path, outside the game and Git directories."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "KOFUO" / "diagnostics"
    return Path.home() / ".local" / "share" / "kofuo" / "diagnostics"


def sha256_file(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()
    except OSError:
        return None


def redact_line(line: str, game_dir: Path | None = None) -> str:
    """Remove likely private paths and identifiers from an upload excerpt."""
    line = line.replace("\x00", "")
    if game_dir is not None:
        for candidate in (str(game_dir), str(game_dir).replace("/", "\\"), str(game_dir).replace("\\", "/")):
            if candidate:
                line = re.sub(re.escape(candidate), "[GAME_DIR]", line, flags=re.IGNORECASE)
    line = SECRET_VALUE.sub(lambda m: f"{m.group(1)}=[REDACTED]", line)
    line = WINDOWS_PATH.sub("[PATH]", line)
    line = UNC_PATH.sub("[NETWORK_PATH]", line)
    line = EMAIL.sub("[EMAIL]", line)
    line = IPV4.sub("[IP]", line)
    return line.strip()[:MAX_EXCERPT_LINE_CHARS]


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


class DiagnosticRun:
    """Collect one game process result without editing game files or injecting input."""

    def __init__(self, game_dir: Path, exe_path: Path, log_path: Path | None = None):
        self.game_dir = Path(game_dir).expanduser().resolve()
        self.exe_path = Path(exe_path)
        if not self.exe_path.is_absolute():
            self.exe_path = self.game_dir / self.exe_path
        self.exe_path = self.exe_path.resolve()
        self.log_path = Path(log_path) if log_path else self.game_dir / "mugen.log"
        if not self.log_path.is_absolute():
            self.log_path = self.game_dir / self.log_path
        self.report_id = str(uuid.uuid4())
        self.started_monotonic = time.monotonic()
        self.created_utc = datetime.now(timezone.utc).isoformat()
        self.before_log_signature = self._log_signature()
        self.finished = False

    def _log_signature(self) -> tuple[int, int] | None:
        try:
            stat = self.log_path.stat()
            return stat.st_size, stat.st_mtime_ns
        except OSError:
            return None

    def _current_log(self) -> tuple[bool, str | None, list[str]]:
        signature = self._log_signature()
        fresh = signature is not None and signature != self.before_log_signature
        if not fresh:
            return False, None, []
        digest = sha256_file(self.log_path)
        try:
            with self.log_path.open("rb") as stream:
                stream.seek(0, os.SEEK_END)
                size = stream.tell()
                stream.seek(max(0, size - MAX_ARCHIVED_LOG_BYTES), os.SEEK_SET)
                raw = stream.read(MAX_ARCHIVED_LOG_BYTES)
            text = raw.decode("utf-8", errors="replace")
        except OSError:
            return True, digest, []
        excerpt = []
        for line in text.splitlines():
            if ERROR_MARKER.search(line):
                excerpt.append(redact_line(line, self.game_dir))
        return True, digest, excerpt[-MAX_EXCERPT_LINES:]

    def _archive_raw_log(self, destination: Path) -> bool:
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            size = self.log_path.stat().st_size
            with self.log_path.open("rb") as source:
                if size > MAX_ARCHIVED_LOG_BYTES:
                    source.seek(size - MAX_ARCHIVED_LOG_BYTES, os.SEEK_SET)
                with destination.open("wb") as target:
                    shutil.copyfileobj(source, target)
            return True
        except OSError:
            return False

    def finish(self, exit_code: int | None, launch_error: str | None = None) -> dict[str, Any]:
        if self.finished:
            return {}
        self.finished = True
        runtime = round(max(0.0, time.monotonic() - self.started_monotonic), 3)
        fresh_log, log_hash, excerpts = self._current_log()
        signals: list[str] = []
        if launch_error:
            signals.append("launch_failed")
        if exit_code is not None and exit_code != 0:
            signals.append("nonzero_exit")
        if excerpts:
            signals.append("engine_error_marker")
        if runtime < 15:
            signals.append("short_runtime")  # A clue only; it does not prove a crash.
        if not fresh_log:
            signals.append("log_missing_or_unchanged")

        if launch_error:
            status = "launch_failed"
        elif exit_code is not None and exit_code != 0:
            status = "nonzero_exit"
        elif excerpts:
            status = "engine_log_error"
        else:
            status = "exit_observed"

        report: dict[str, Any] = {
            "schema_version": 1,
            "report_id": self.report_id,
            "created_utc": self.created_utc,
            "project": "KOF-Ultimate-Online",
            "event": "game_process_exit",
            "status": status,
            "engine": os.environ.get("KOFUO_ENGINE", "unknown")[:40],
            "game_version": os.environ.get("KOFUO_VERSION", "unknown")[:40],
            "exit_code": exit_code,
            "runtime_seconds": runtime,
            "binary_sha256": sha256_file(self.exe_path),
            "log_sha256": log_hash,
            "log_fresh": fresh_log,
            "signals": signals,
            "error_excerpt": excerpts,
            "raw_log_uploaded": False,
            "supa_delivery": "not_configured",
        }

        local_root = Path(os.environ.get("KOFUO_DIAGNOSTICS_LOCAL_DIR", default_diagnostics_dir()))
        local_report = local_root / "reports" / f"{self.report_id}.json"
        raw_log = local_root / "raw_logs" / f"{self.report_id}.log"
        if fresh_log:
            report["raw_log_saved_locally"] = self._archive_raw_log(raw_log)
        else:
            report["raw_log_saved_locally"] = False

        try:
            _atomic_json(local_report, report)
        except OSError as exc:
            report["local_report_error"] = type(exc).__name__

        outbox = os.environ.get("KOFUO_DIAGNOSTICS_OUTBOX", "").strip()
        if outbox:
            try:
                report["supa_delivery"] = "shared_folder_outbox"
                _atomic_json(Path(outbox) / f"{self.report_id}.json", report)
                _atomic_json(local_report, report)
            except OSError as exc:
                report["supa_delivery"] = f"outbox_error:{type(exc).__name__}"
                try:
                    _atomic_json(local_report, report)
                except OSError:
                    pass

        print(f"KOFUO diagnostic report: {local_report}")
        return report
