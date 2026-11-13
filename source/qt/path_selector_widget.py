from pathlib import Path

from source.paths import resource_path
from source.qt_imports import *


class FolderSelectorWidget(QLineEdit):
    def __init__(self,
        icon: QIcon,
        action_tooltip: str | None = None,
        dialog_caption: str | None = None,
        action_position: QLineEdit.ActionPosition = QLineEdit.ActionPosition.TrailingPosition,
        is_readonly: bool = False,
        parent=None
    ):
        super().__init__(parent)
        self._dialog_caption = dialog_caption

        self.setReadOnly(is_readonly)

        action = self.addAction(icon, action_position)
        action.triggered.connect(self._select_folder)
        action.setToolTip(action_tooltip)

        button = self.findChild(QToolButton)
        if button is not None:
            button.setCursor(Qt.CursorShape.PointingHandCursor)

    def _select_folder(self):
        current = self.text().strip()
        start_dir = current if current and Path(current).expanduser().is_dir() else QDir.homePath()

        folder = QFileDialog.getExistingDirectory(
            self.window(),
            self._dialog_caption or "Выбор папки",
            start_dir,
            QFileDialog.ShowDirsOnly
        )
        if folder:
            self.setText(folder)


if __name__ == '__main__':
    app = QApplication()

    icon_path = str(resource_path("icons/folder.png"))
    icon = QIcon(icon_path)
    w = FolderSelectorWidget(icon, "Выбрать папку")
    w.show()

    app.exec()


