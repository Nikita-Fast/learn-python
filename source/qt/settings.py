import json
from typing import Any

from source.paths import resource_path
from source.qt_imports import QSettings


def _flatten(prefix: str, value: Any, result: dict[str, Any]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            _flatten(f"{prefix}/{key}" if prefix else key, child, result)
    else:
        result[prefix] = value


class Settings:
    _defaults: dict[str, Any] | None = None

    def __init__(self, qsettings: QSettings | None = None):
        self._qsettings = qsettings or QSettings("Koncentr", "DemoApp")

        if Settings._defaults is None:
            Settings._defaults = self._load_defaults()

        self._defaults = Settings._defaults

    @staticmethod
    def _load_defaults() -> dict[str, Any]:
        with resource_path("default_settings.json").open(encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("default_settings.json должен содержать объект JSON")

        result: dict[str, Any] = {}
        _flatten("", data, result)
        return result

    def get(self, key: str) -> Any:
        default = self._default(key)
        value = self._qsettings.value(key, default)
        return self._coerce(value, default)

    def set(self, key: str, value: Any) -> None:
        default = self._default(key)
        self._qsettings.setValue(key, self._coerce(value, default))

    def reset(self, key: str | None = None) -> None:
        if key is None:
            self._qsettings.clear()
        else:
            self._default(key)
            self._qsettings.remove(key)

    def sync(self) -> None:
        self._qsettings.sync()

    def all_keys(self) -> list[str]:
        return self._qsettings.allKeys()

    def get_style_settings(self) -> dict[str, Any]:
        prefix = "style/"
        return {
            key[len(prefix):]: self.get(key)
            for key in self._defaults
            if key.startswith(prefix)
        }

    @property
    def font_size(self) -> int:
        return int(self.get("style/font_size"))

    @font_size.setter
    def font_size(self, value: int) -> None:
        self.set("style/font_size", value)

    def _default(self, key: str) -> Any:
        try:
            return self._defaults[key]
        except KeyError:
            raise KeyError(f"Неизвестная настройка: {key!r}") from None

    @staticmethod
    def _coerce(value: Any, default: Any) -> Any:
        if value is None:
            return default

        if isinstance(default, bool):
            if isinstance(value, str):
                return value.strip().lower() in {"1", "true", "yes", "on"}
            return bool(value)

        if isinstance(default, int):
            try:
                return int(value)
            except (TypeError, ValueError):
                return default

        if isinstance(default, float):
            try:
                return float(value)
            except (TypeError, ValueError):
                return default

        if isinstance(default, str):
            return str(value)

        return value
