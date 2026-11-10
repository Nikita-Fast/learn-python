import socket
import sys
import time
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QApplication, QLabel, QCheckBox, QGridLayout, \
    QSizePolicy, QPushButton

from source.qt.ipv4_validator import IPv4Validator
from source.qt.switch_widget import SwitchWidget


class Device:
    def __init__(self, name: str):
        self._name = name

    def connect(*args, **kwargs):
        pass

    def disconnect(self):
        pass

    def is_connected(self) -> bool:
        pass

    @property
    def name(self) -> str:
        return self._name

class TcpDevice(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self._is_connected = False
        self._sock = None

    def connect(self, ip: str, port: int):
        if self._is_connected:
            raise RuntimeError(f"TcpDevice '{self._name}' already connected")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
        except Exception:
            self._sock = None
            raise
        else:
            self._is_connected = True
            self._sock = sock

    def disconnect(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None
        else:
            raise RuntimeError(f"TcpDevice '{self._name}' is not connected")

    def send(self, data: bytes):
        self._sock.send(data)

    def receive(self, n: int) -> bytes:
        return self._sock.recv(n)


class DevicesManager:
    def __init__(self):
        self._devices = {}

    def devices_id(self) -> list:
        return list(self._devices.keys())

    def get_device(self, device_id: str) -> Device:
        if device_id not in self._devices:
            raise RuntimeError(f"Unknown {device_id=}")
        return self._devices[device_id]

    def add_device(self, device: Device, device_id: str):
        if device_id in self._devices:
            raise ValueError(f"Device '{device_id}' already exists (device_id must be unique)")
        self._devices[device_id] = device


class ConnectionWidget(QWidget):
    def __init__(self, devices_manager: DevicesManager):
        super().__init__()

        self._devices_manager = devices_manager

        ip_validator = IPv4Validator()

        self._checkbox = QCheckBox()
        self._name_label = QLabel("Векторный анализатор цепей ZNA26")
        self._ip_edit = QLineEdit()
        self._check_widget = SwitchWidget(parent=self)
        self._connect_btn = QPushButton("Подключиться")

        self._ip_edit.setValidator(ip_validator)
        self._ip_edit.setText("127.0.0.1")

        header1 = QLabel("Checkbox")
        header2 = QLabel("Устройство")
        header3 = QLabel("IP-адрес")
        header4 = QLabel("Переключатель")

        for label in [header1, header2, header3, header4]:
            label.setProperty("role", "header")
            label.setAlignment(Qt.AlignCenter)
            label.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Fixed,
            )

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.addWidget(header1, 0, 0)
        grid.addWidget(header2, 0, 1)
        grid.addWidget(header3, 0, 2)
        grid.addWidget(header4, 0, 3)

        grid.addWidget(self._checkbox, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self._name_label, 1, 1)
        grid.addWidget(self._ip_edit, 1, 2)
        grid.addWidget(self._check_widget, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self._connect_btn, 1, 4)

        self.setLayout(grid)

        self._connect_btn.clicked.connect(self._handle_connect)

    def _handle_connect(self):

        device = self._devices_manager.get_device("test-tcp-device-1")
        device.connect(ip=self._ip_edit.text(), port=5025)
        time.sleep(1)
        device.send(b"*IDN?\n")
        time.sleep(1)
        print(device.receive(1024))
        device.disconnect()


if __name__ == '__main__':
    style = Path(__file__).parent.parent.parent / "Resource" / "style.qss"

    app = QApplication(sys.argv)
    app.setStyleSheet(style.read_text(encoding="utf-8"))

    devices_manager = DevicesManager()
    tcp_dev = TcpDevice(name="tcp scpi device")
    devices_manager.add_device(tcp_dev, "test-tcp-device-1")

    # devices_manager.get_device("test-tcp-device-1")

    window = ConnectionWidget(devices_manager)
    window.show()
    sys.exit(app.exec())
