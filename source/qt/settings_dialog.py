from pathlib import Path

from PySide6.QtWidgets import QMessageBox

from source.paths import resource_path
from source.qt.logging_setup import (
    configure_logging,
    default_log_directory,
    effective_log_directory,
    paths_equal,
)
from source.qt.path_selector_widget import FolderSelectorWidget
from source.qt.settings import Settings
from source.qt.style_manager import StyleManager
from source.qt_imports import *


class SettingsDialog(QDialog):
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self._settings = settings
        self._style_manager = StyleManager(settings)

        self._button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
        )
        self._button_box.clicked.connect(self.on_button_clicked)

        # Виджеты для ввода настроек
        self._font_size_spin = QSpinBox()
        self._font_size_spin.setValue(self._settings.font_size)

        self._pending_color = QColor(self._settings.main_menu_background_color)
        if not self._pending_color.isValid():
            self._pending_color = QColor(
                self._settings.default("style/main_menu_background_color")
            )

        self._color_button = QPushButton()
        self._color_button.clicked.connect(self._choose_color)
        self._update_color_button()

        icon = QIcon(str(resource_path("icons/folder.png")))
        self._default_log_dir = default_log_directory()
        self._log_folder_selector = FolderSelectorWidget(
            icon,
            "Выбрать папку",
            dialog_caption="Папка для сохранения логов",
            parent=self,
        )
        self._log_folder_selector.setText(
            str(effective_log_directory(self._settings))
        )

        form = QFormLayout()
        form.addRow("Размер шрифта:", self._font_size_spin)
        form.addRow("Цвет фона меню:", self._color_button)
        form.addRow("Расположение Log-файлов:", self._log_folder_selector)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self._button_box)
        self.setLayout(vbox)

    def on_button_clicked(self, btn):
        match self._button_box.buttonRole(btn):
            case QDialogButtonBox.ButtonRole.ApplyRole | QDialogButtonBox.ButtonRole.AcceptRole:
                if not self._save_settings():
                    return

                self._apply_settings()

                if self._button_box.buttonRole(btn) == QDialogButtonBox.ButtonRole.AcceptRole:
                    self.accept()
            case QDialogButtonBox.ButtonRole.RejectRole:
                self.reject()
            case unknown_role:
                raise ValueError(f"Неизвестная роль: {unknown_role}")

    def _choose_color(self):
        color = QColorDialog.getColor(
            self._pending_color,
            self,
            "Цвет фона главного меню",
        )
        if color.isValid():
            self._pending_color = color
            self._update_color_button()

    def _update_color_button(self):
        color = self._pending_color

        pixmap = QPixmap(25, 25)
        pixmap.fill(color)

        self._color_button.setIcon(QIcon(pixmap))
        self._color_button.setText(color.name().upper())

    def _save_settings(self) -> bool:
        raw_path = self._log_folder_selector.text().strip()
        selected_dir = (
            Path(raw_path).expanduser().resolve(strict=False)
            if raw_path
            else self._default_log_dir
        )

        try:
            configure_logging(selected_dir)
        except OSError as exc:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось использовать папку для логов:\n"
                f"{selected_dir}\n\n{exc}",
            )
            return False

        if paths_equal(selected_dir, self._default_log_dir):
            self._settings.log_folder = ""
        else:
            self._settings.log_folder = str(selected_dir)

        self._settings.font_size = self._font_size_spin.value()
        self._settings.main_menu_background_color = self._pending_color.name().upper()
        self._settings.sync()
        return True

    def _apply_settings(self):
        # применение настроек, относящихся к стилю
        self._style_manager.apply_style()


