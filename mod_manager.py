from pathlib import Path
from typing import Dict, List, Optional
import shutil

from base_adapter import GameAdapter
from game_registry import GameConfig, GameRegistry


class ModManager:
    """High-level manager for installing and tracking mods across games."""

    def __init__(self, registry: Optional[GameRegistry] = None):
        self.registry = registry or GameRegistry()
        self.adapters: Dict[str, GameAdapter] = {}

    def register_adapter(self, adapter: GameAdapter) -> bool:
        config = GameConfig(
            game_id=adapter.game_id,
            name=adapter.name,
            version=adapter.version,
            install_path=adapter.install_root,
            mod_folder=adapter.mod_root,
            adapter_class=adapter.__class__.__name__,
            supported_formats=adapter.supported_extensions,
        )

        if not self.registry.register_game(config):
            return False

        self.adapters[adapter.game_id] = adapter
        return True

    def install_mod(self, game_id: str, mod_dir: str | Path) -> None:
        adapter = self.adapters.get(game_id)
        if adapter is None:
            raise ValueError(f"No adapter registered for game '{game_id}'.")

        source = Path(mod_dir)
        if not source.exists():
            raise FileNotFoundError(f"Mod directory not found: {source}")

        adapter.install_mod(source, adapter.install_root)
        print(f"✅ Mod installed for {adapter.name}: {source}")

    def uninstall_mod(self, game_id: str, mod_dir: str | Path) -> None:
        adapter = self.adapters.get(game_id)
        if adapter is None:
            raise ValueError(f"No adapter registered for game '{game_id}'.")

        source = Path(mod_dir)
        if not source.exists():
            raise FileNotFoundError(f"Mod directory not found: {source}")

        adapter.uninstall_mod(source, adapter.install_root)
        print(f"✅ Mod uninstalled for {adapter.name}: {source}")

    def list_games(self) -> List[str]:
        return self.registry.list_games()

    def list_mods(self, game_id: str) -> List[str]:
        config = self.registry.get_game(game_id)
        if not config:
            return []
        mod_dir = config.mod_folder
        if not mod_dir.exists():
            return []
        return [str(p.name) for p in mod_dir.iterdir() if p.is_dir() or p.is_file()]


def backup_directory(path: Path) -> Path:
    backup_dir = path.parent / f"{path.name}.backup"
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    shutil.copytree(path, backup_dir)
    return backup_dir
