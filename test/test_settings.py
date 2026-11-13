import pytest
from jinja2 import Environment, meta
from PySide6.QtCore import QSettings

from source.paths import resource_path
from source.qt.settings import Settings


def make_settings(tmp_path):
    qsettings = QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat)
    return Settings(qsettings), qsettings


def test_defaults_are_loaded(tmp_path):
    settings, _ = make_settings(tmp_path)

    assert settings.font_size == 12
    assert settings.get("style/font_size") == 12
    assert settings.get("style/main_menu_background_color") == "#3C3C3C"


def test_setting_persists(tmp_path):
    path = str(tmp_path / "settings.ini")

    first = Settings(QSettings(path, QSettings.Format.IniFormat))
    first.font_size = 18
    first.sync()

    second = Settings(QSettings(path, QSettings.Format.IniFormat))
    assert second.font_size == 18


def test_reset_returns_default(tmp_path):
    settings, _ = make_settings(tmp_path)
    settings.font_size = 18
    settings.sync()
    assert settings.font_size == 18

    settings.reset("style/font_size")
    assert settings.font_size == 12


def test_style_settings(tmp_path):
    settings, _ = make_settings(tmp_path)

    assert settings.get_style_settings() == {
        "font_size": 12,
        "main_menu_background_color": "#3C3C3C",
    }


def test_unknown_key_raises(tmp_path):
    settings, _ = make_settings(tmp_path)

    with pytest.raises(KeyError):
        settings.get("style/unknown")

    with pytest.raises(KeyError):
        settings.set("style/unknown", 1)


def test_invalid_value_falls_back_to_default(tmp_path):
    settings, qsettings = make_settings(tmp_path)
    qsettings.setValue("style/font_size", "not-a-number")

    assert settings.font_size == 12


def test_all_keys(tmp_path):
    settings, _ = make_settings(tmp_path)
    settings.font_size = 18
    settings.sync()

    assert "style/font_size" in settings.all_keys()


def test_qss_placeholders_have_defaults(tmp_path):
    settings, _ = make_settings(tmp_path)
    source = resource_path("style_template.qss").read_text(encoding="utf-8")
    ast = Environment().parse(source)

    placeholders = meta.find_undeclared_variables(ast)

    assert placeholders <= set(settings.get_style_settings())
