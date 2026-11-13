import logging
import sys

from PySide6.QtCore import QCoreApplication

from source.qt.logging_setup import (
    LOG_FORMAT,
    configure_logging,
    effective_log_directory,
)
from source.qt.settings import Settings
from source.qt.style_manager import StyleManager
from source.qt.settings_dialog import SettingsDialog
from source.qt_imports import *
from source.paths import resource_path


class AppMainWindow(QMainWindow):
    def __init__(self, settings: Settings, /):
        super().__init__()
        self._settings = settings
        self._was_maximized = False
        self.setWindowTitle("Базовое Qt-приложение")
        self.setCentralWidget(ContainerWidget())

        self._create_menu()

    def _create_menu(self):
        menubar = self.menuBar()

        menu = menubar.addMenu("&Меню")

        # 3. Создаем действие (пункт меню) для переключения полноэкранного режима
        self.fullscreen_action = QAction("Полноэкранный режим", self)
        self.fullscreen_action.setCheckable(True)  # Делаем пункт "галочкой"
        self.fullscreen_action.setShortcut(QKeySequence("F11"))  # Горячая клавиша F11
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)
        menu.addAction(self.fullscreen_action)

        self.settings_action = QAction("Настройки", self)
        self.settings_action.triggered.connect(self.open_settings)
        menu.addAction(self.settings_action)

        # Дополнительно: пункт "Выход"
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        menu.addSeparator()
        menu.addAction(exit_action)

    def open_settings(self):
        dialog = SettingsDialog(self._settings, self)
        ret = dialog.exec()
        print(ret)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self._leave_fullscreen()
        else:
            self._was_maximized = self.isMaximized()
            self.showFullScreen()
        self._sync_fullscreen_action()

    def _leave_fullscreen(self):
        if self._was_maximized:
            self.showMaximized()
        else:
            self.showNormal()
        self._sync_fullscreen_action()

    def _sync_fullscreen_action(self):
        self.fullscreen_action.setChecked(self.isFullScreen())

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self._sync_fullscreen_action()
        super().changeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self._leave_fullscreen()
            event.accept()
        else:
            super().keyPressEvent(event)


class ContainerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._label1 = QLabel("Некий текст в первом поле")
        self._spin = QSpinBox()

        self._spin.setValue(12)

        vbox = QVBoxLayout()
        vbox.addWidget(self._label1)
        vbox.addWidget(self._spin)
        vbox.addStretch()
        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # От этих имён зависит путь QStandardPaths для логов.
    QCoreApplication.setOrganizationName("Koncentr")
    QCoreApplication.setApplicationName("DemoApp")

    settings = Settings()

    try:
        configure_logging(effective_log_directory(settings))
    except OSError as exc:
        logging.basicConfig(
            level=logging.DEBUG,
            format=LOG_FORMAT,
            stream=sys.stderr,
            force=True,
        )
        logging.getLogger(__name__).exception(
            "Не удалось открыть лог-файл: %s", exc
        )

    logger = logging.getLogger(__name__)
    logger.info("Расположение логов: %r", effective_log_directory(settings))

    # Настройка переводчика на русский язык
    translator = QTranslator()
    translation_path = resource_path("qtbase_ru.qm").parent
    logger.debug(f"Расположение файла перевода Qt-виджетов на русский язык: {translation_path!r}")

    # Загружаем файл переводов базовых модулей Qt
    if translator.load(QLocale("ru_RU"), "qtbase", "_", str(translation_path)):
        app.installTranslator(translator)

    StyleManager(settings).apply_style()

    mw = AppMainWindow(settings)
    mw.show()

    sys.exit(app.exec())
