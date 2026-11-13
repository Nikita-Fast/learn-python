import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import QStandardPaths

from source.qt.settings import Settings


LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FILE_NAME = "app.log"
MAX_LOG_BYTES = 5_000_000
BACKUP_COUNT = 5


# Права на каталог логов (POSIX, восьмеричная запись):
#
#   0700 — владелец: rwx; группа и остальные: ---.
#          Только владелец может войти в каталог, увидеть файлы
#          и создавать/удалять их.
#
#   0750 — владелец: rwx; группа: r-x; остальные: ---.
#          Читать каталог могут владелец и члены группы.
#
#   0755 — владелец: rwx; группа: r-x; остальные: r-x.
#          Любой пользователь может увидеть имена файлов.
#          Создавать/удалять файлы может только владелец.
#
# Для каталога:
#   r — читать список имён;
#   w — создавать/удалять/переименовывать записи;
#   x — входить в каталог и обращаться к файлам внутри.
#
# Выбрано 0700: логи доступны только пользователю,
# который запустил приложение. Он является владельцем каталога
# и может прочитать или скопировать лог.
LOG_DIR_MODE = 0o700


# Права на файл лога:
#
#   0600 — владелец: rw-; группа и остальные: ---.
#          Только владелец может читать и изменять лог.
#
#   0640 — владелец: rw-; группа: r--; остальные: ---.
#          Лог могут читать владелец и члены группы.
#
#   0644 — владелец: rw-; группа: r--; остальные: r--.
#          Любой пользователь может прочитать лог.
#
# Для файла x (execute) не нужен: лог не является исполняемым файлом.
#
# Выбрано 0600: пользователь-владелец может читать и копировать лог,
# остальные пользователи системы — нет.
LOG_FILE_MODE = 0o600


class SecureRotatingFileHandler(RotatingFileHandler):
    """RotatingFileHandler, который сохраняет права 0600 на POSIX."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_file_mode()

    def doRollover(self) -> None:
        super().doRollover()
        self._apply_file_mode()

    def _apply_file_mode(self) -> None:
        if os.name != "posix":
            return
        try:
            os.chmod(self.baseFilename, LOG_FILE_MODE)
        except OSError:
            # Не мешаем логированию, если права не удалось изменить.
            pass


def default_log_directory() -> Path:
    base = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.StateLocation
    )

    if not base:
        base = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppLocalDataLocation
        )

    if not base:
        base = str(Path.home() / ".local" / "state")

    return Path(base) / "logs"


def effective_log_directory(settings: Settings) -> Path:
    custom = settings.log_folder.strip()
    if custom:
        return Path(custom).expanduser().resolve(strict=False)
    return default_log_directory()


def paths_equal(first: Path, second: Path) -> bool:
    first = Path(first).expanduser().resolve(strict=False)
    second = Path(second).expanduser().resolve(strict=False)
    return os.path.normcase(str(first)) == os.path.normcase(str(second))


def configure_logging(log_dir: Path) -> None:
    log_dir = Path(log_dir).expanduser().resolve(strict=False)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Для стандартного каталога приложения выставляем 0700.
    # Пользовательскую папку не трогаем: у неё могут быть свои правила доступа.
    if os.name == "posix" and paths_equal(log_dir, default_log_directory()):
        log_dir.chmod(LOG_DIR_MODE)

    log_file = log_dir / LOG_FILE_NAME
    _ensure_log_file(log_file)

    root = logging.getLogger()

    # Если лог уже пишется в этот файл, не пересоздаём обработчик.
    for old_handler in root.handlers:
        if getattr(old_handler, "_app_log_handler", False):
            old_path = getattr(old_handler, "baseFilename", None)
            if old_path and paths_equal(Path(old_path), log_file):
                root.setLevel(logging.DEBUG)
                return

    handler = SecureRotatingFileHandler(
        log_file,
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler._app_log_handler = True

    for old_handler in list(root.handlers):
        if getattr(old_handler, "_app_log_handler", False):
            root.removeHandler(old_handler)
            old_handler.close()

    root.addHandler(handler)
    root.setLevel(logging.DEBUG)


def _ensure_log_file(path: Path) -> None:
    # os.open учитывает umask, поэтому после создания
    # явно фиксируем итоговые права через chmod.
    fd = os.open(
        path,
        os.O_CREAT | os.O_APPEND | os.O_WRONLY,
        LOG_FILE_MODE,
    )
    os.close(fd)

    if os.name == "posix":
        path.chmod(LOG_FILE_MODE)
