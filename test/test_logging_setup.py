import logging
import os
import stat
from pathlib import Path

import pytest
from PySide6.QtCore import QSettings

import source.qt.logging_setup as logging_setup
from source.qt.logging_setup import (
    configure_logging,
    effective_log_directory,
    paths_equal,
)
from source.qt.settings import Settings


def make_settings(tmp_path) -> Settings:
    qsettings = QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat)
    return Settings(qsettings)


def flush_app_handlers() -> None:
    for handler in logging.getLogger().handlers:
        if getattr(handler, "_app_log_handler", False):
            handler.flush()


@pytest.fixture(autouse=True)
def restore_logging_state():
    root = logging.getLogger()
    old_handlers = list(root.handlers)
    old_level = root.level

    yield

    for handler in list(root.handlers):
        if getattr(handler, "_app_log_handler", False):
            root.removeHandler(handler)
            handler.close()

    for handler in old_handlers:
        if handler not in root.handlers:
            root.addHandler(handler)

    root.setLevel(old_level)


def test_log_folder_default_and_custom(tmp_path):
    settings = make_settings(tmp_path)

    assert settings.log_folder == ""

    custom = tmp_path / "custom-logs"
    settings.log_folder = f"  {custom}  "
    assert settings.log_folder == str(custom)


def test_effective_log_directory_uses_custom_path(tmp_path):
    settings = make_settings(tmp_path)
    custom = tmp_path / "custom-logs"
    settings.log_folder = str(custom)

    assert paths_equal(effective_log_directory(settings), custom)


def test_configure_logging_writes_to_file(tmp_path):
    log_dir = tmp_path / "logs"
    configure_logging(log_dir)

    logging.getLogger("test").info("hello from test")
    flush_app_handlers()

    log_file = log_dir / "app.log"
    assert log_file.exists()
    assert "hello from test" in log_file.read_text(encoding="utf-8")

    if os.name == "posix":
        assert stat.S_IMODE(log_file.stat().st_mode) == logging_setup.LOG_FILE_MODE


def test_default_log_directory_permissions(tmp_path, monkeypatch):
    default_dir = tmp_path / "default-logs"
    monkeypatch.setattr(logging_setup, "default_log_directory", lambda: default_dir)

    configure_logging(default_dir)

    if os.name == "posix":
        assert stat.S_IMODE(default_dir.stat().st_mode) == logging_setup.LOG_DIR_MODE


def test_reconfigure_logging(tmp_path):
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    configure_logging(first_dir)
    logging.getLogger("test").info("first message")
    flush_app_handlers()

    configure_logging(second_dir)
    logging.getLogger("test").info("second message")
    flush_app_handlers()

    assert "first message" in (first_dir / "app.log").read_text(encoding="utf-8")
    assert "second message" in (second_dir / "app.log").read_text(encoding="utf-8")
