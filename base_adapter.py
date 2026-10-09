from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class GameAdapter(ABC):
    """Base interface for all game-specific adapters."""

    game_id: str = ""
    name: str = ""
    version: str = "custom"
    supported_extensions: List[str] = ["zip", "json", "cfg", "ini", "txt"]

    def __init__(self, install_root: str | Path, mod_root: str | Path = "./mods"):
        self.install_root = Path(install_root)
        self.mod_root = Path(mod_root)
        self.install_root.mkdir(parents=True, exist_ok=True)
        self.mod_root.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def validate_install(self) -> bool:
        """Check whether the game installation exists and is supported."""

    @abstractmethod
    def install_mod(self, mod_dir: Path, target_root: Path | None = None) -> None:
        """Install a mod pack into the game installation."""

    @abstractmethod
    def uninstall_mod(self, mod_dir: Path, target_root: Path | None = None) -> None:
        """Remove a previously installed mod pack."""

    def list_supported_files(self) -> List[str]:
        return [f"*.{ext}" for ext in self.supported_extensions]
