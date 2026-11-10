from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget


class SwitchWidget(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._checked = False

        self.setFixedSize(50, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool) -> None:
        checked = bool(checked)

        if self._checked == checked:
            return

        self._checked = checked
        self.update()
        self.toggled.emit(checked)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self._checked)
            event.accept()
            return

        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = 2

        track_rect = self.rect().adjusted(
            margin,
            margin,
            -margin,
            -margin,
        )

        radius = track_rect.height() / 2

        # Цвет трека
        if self._checked:
            track_color = QColor("#4CAF50")
        else:
            track_color = QColor("#BDBDBD")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, radius, radius)

        # Круглый ползунок
        knob_margin = 1
        knob_size = track_rect.height() - 2 * knob_margin

        if self._checked:
            knob_x = (
                track_rect.right()
                - knob_margin
                - knob_size
                + 1
            )
        else:
            knob_x = track_rect.left() + knob_margin

        knob_y = track_rect.top() + knob_margin

        painter.setBrush(QColor("white"))

        painter.drawEllipse(
            knob_x,
            knob_y,
            knob_size,
            knob_size,
        )