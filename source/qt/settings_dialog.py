from jinja2 import Template

from source.paths import resource_path
from source.qt.settings import Settings
from source.qt.style_manager import StyleManager
from source.qt_imports import *


class SettingsDialog(QDialog):
    def __init__(self, /, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self._settings = Settings()
        self._style_manager = StyleManager()

        self._button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
        )
        self._button_box.clicked.connect(self.on_button_clicked)

        # Виджеты для ввода настроек
        self._font_size_spin = QSpinBox()
        self._font_size_spin.setValue(self._settings.font_size)

        form = QFormLayout()
        form.addRow("Размер шрифта:", self._font_size_spin)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self._button_box)
        self.setLayout(vbox)

    def on_button_clicked(self, btn):
        match self._button_box.buttonRole(btn):
            case QDialogButtonBox.ButtonRole.ApplyRole | QDialogButtonBox.ButtonRole.AcceptRole:
                self._save_settings()
                self._apply_settings()

                if self._button_box.buttonRole(btn) == QDialogButtonBox.ButtonRole.AcceptRole:
                    self.accept()
            case QDialogButtonBox.ButtonRole.RejectRole:
                self.reject()
            case unknown_role:
                raise ValueError(f"Неизвестная роль: {unknown_role}")

    def _save_settings(self):
        self._settings.font_size = self._font_size_spin.value()

    def _apply_settings(self):
        # применение настроек, относящихся к стилю
        self._style_manager.apply_style()


