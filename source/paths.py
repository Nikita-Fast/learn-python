import sys
from pathlib import Path


def app_root() -> Path:
    """Корень приложения: папка проекта в dev, папка бандла в exe."""
    if getattr(sys, "frozen", False):
        # PyInstaller: onefile -> Temp/_MEIxxxx, onedir -> <app>/_internal
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    # source/paths.py -> source -> корень проекта
    return Path(__file__).resolve().parents[1]


def resource_path(*parts: str) -> Path:
    """Путь к файлу внутри resource/."""
    return app_root().joinpath("resource", *parts)


if __name__ == '__main__':
    print(app_root())
    print(resource_path("style_template.qss"))