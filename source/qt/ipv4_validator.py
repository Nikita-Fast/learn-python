from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QLineEdit


class IPv4Validator(QValidator):
    def validate(self, text: str, pos: int):
        if not text:
            return QValidator.State.Intermediate, text, pos

        parts = text.split(".")

        if len(parts) > 4:
            return QValidator.State.Invalid, text, pos

        for part in parts:
            if part == "":
                continue

            if not part.isdigit():
                return QValidator.State.Invalid, text, pos

            if len(part) > 3:
                return QValidator.State.Invalid, text, pos

            if int(part) > 255:
                return QValidator.State.Invalid, text, pos

        if len(parts) == 4 and all(
            part != "" and 0 <= int(part) <= 255
            for part in parts
        ):
            return QValidator.State.Acceptable, text, pos

        return QValidator.State.Intermediate, text, pos


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    line_edit = QLineEdit()
    line_edit.setPlaceholderText("192.168.1.1")
    line_edit.setValidator(IPv4Validator(line_edit))
    line_edit.show()

    sys.exit(app.exec())