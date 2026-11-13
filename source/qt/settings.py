from jinja2 import Template

from source.paths import resource_path
from source.qt_imports import *


class Settings:
    DEFAULT_FONT_SIZE = 12

    def __init__(self):
        self._settings = QSettings("Koncentr", "DemoApp")

    @property
    def font_size(self):
        return self._settings.value("font_size", Settings.DEFAULT_FONT_SIZE)

    @font_size.setter
    def font_size(self, value):
        self._settings.setValue("font_size", value)

    def get_style_settings(self) -> dict:
        return {
            "font_size": self.font_size
        }



