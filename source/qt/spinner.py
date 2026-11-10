import sys
import time

from PySide6.QtCore import Qt, QTimer, QRectF, Property, QSize
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QStyleOption, QStyle, QHBoxLayout, \
    QLabel, QLineEdit, QSizePolicy


class Spinner(QWidget):
    def __init__(self, arc_length: int = 90 * 16, rotation_speed: int = 4 * 16, parent=None):
        super().__init__(parent)

        if not (-360*16 <= arc_length <= 360*16):
            raise ValueError("Arc length must be between -360*16 and 360*16")

        # Угол в Qt измеряется в 1/16 градуса
        self._angle = 0
        self._arc_length = arc_length
        self._rotation_speed = rotation_speed

        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._rotate)

        self._circle_color = QColor("gray")
        self._arc_color = QColor("white")
        self._circle_pen_width = 10
        self._arc_pen_width = 8

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )

        self._size_hint = QSize(30, 30)

    def start(self):
        self.show()
        self._timer.start()

    def stop(self):
        self._timer.stop()
        self.hide()

    def _rotate(self):
        self._angle = (self._angle - self._rotation_speed) % (360 * 16)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        circle_pen = QPen(self._circle_color)
        circle_pen.setWidth(self._circle_pen_width)

        arc_pen = QPen(self._arc_color)
        arc_pen.setWidth(self._arc_pen_width)
        arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Background circle
        painter.setPen(circle_pen)

        size = min(self.width(), self.height())

        x = (self.width() - size) / 2
        y = (self.height() - size) / 2

        margin = max(self._circle_pen_width, self._arc_pen_width) / 2 + 1

        rect = QRectF(
            x + margin,
            y + margin,
            size - 2 * margin,
            size - 2 * margin,
        )

        painter.drawEllipse(rect)

        # Animated arc
        painter.setPen(arc_pen)

        painter.drawArc(
            rect,
            int(self._angle),
            int(self._arc_length),
        )

    def minimumSizeHint(self):
        return QSize(20, 20)

    def sizeHint(self):
        return self._size_hint

    def setSizeHint(self, size_hint):
        self._size_hint = size_hint
        self.updateGeometry()

    # Далее определены QSS свойства для управления стилем (смотри пример в самом низу)
    def getCircleColor(self):
        return self._circle_color

    def setCircleColor(self, color):
        self._circle_color = color
        self.update()

    circleColor = Property(
        QColor,
        getCircleColor,
        setCircleColor,
    )

    def getArcColor(self):
        return self._arc_color

    def setArcColor(self, color):
        self._arc_color = color
        self.update()

    arcColor = Property(
        QColor,
        getArcColor,
        setArcColor,
    )

    def getCirclePenWidth(self):
        return self._circle_pen_width

    def setCirclePenWidth(self, width):
        self._circle_pen_width = width
        self.update()

    circlePenWidth = Property(
        int,
        getCirclePenWidth,
        setCirclePenWidth,
    )

    def getArcPenWidth(self):
        return self._arc_pen_width

    def setArcPenWidth(self, width):
        self._arc_pen_width = width
        self.update()

    arcPenWidth = Property(
        int,
        getArcPenWidth,
        setArcPenWidth,
    )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        Spinner {
            qproperty-circleColor: white;
            qproperty-arcColor: purple;
            qproperty-circlePenWidth: 5;
            qproperty-arcPenWidth: 4;
        }
    """)

    w = QWidget()
    hbox = QHBoxLayout(w)
    label = QLabel("Test label")
    edit = QLineEdit()
    btn = QPushButton("Button")

    print(f"{btn.sizeHint()=}")
    print(f"{label.sizeHint()=}")
    print(f"{edit.sizeHint()=}")

    spinner = Spinner(arc_length=135 * 16, rotation_speed=4 * 16)
    spinner.setSizePolicy(
        QSizePolicy.Fixed,
        QSizePolicy.Fixed,
    )
    h = btn.sizeHint().height()
    spinner.setSizeHint(QSize(h, h))

    hbox.addWidget(label)
    hbox.addWidget(edit)
    hbox.addWidget(spinner)
    hbox.addWidget(btn)

    w.show()

    spinner.start()

    sys.exit(app.exec())
