from jinja2 import Template

from source.paths import resource_path
from source.qt.settings import Settings
from source.qt_imports import QApplication


class StyleManager:
    def __init__(self, settings: Settings):
        self._settings = settings

    def apply_style(self):
        with resource_path("style_template.qss").open(encoding="utf-8") as f:
            template = Template(f.read())
            style = template.render(**self._settings.get_style_settings())
            app = QApplication.instance()
            app.setStyleSheet(style)
