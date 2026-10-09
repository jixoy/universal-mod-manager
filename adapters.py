from pathlib import Path
import shutil

from base_adapter import GameAdapter


class Manhunt1Adapter(GameAdapter):
    """Example adapter for a stealth/horror game project.

    This is a generic architecture example only. It does not include or redistribute
    copyrighted game files. You can define your own folder layout and install logic.
    """

    game_id = "manhunt_1"
    name = "Manhunt 1"
    version = "1.0.0"
    supported_extensions = ["zip", "json", "cfg", "ini", "txt", "dds"]

    def validate_install(self) -> bool:
        required = [
            self.install_root / "game",
            self.install_root / "mods",
        ]
        return all(path.exists() for path in required)

    def install_mod(self, mod_dir: Path, target_root: Path | None = None) -> None:
        target_root = target_root or self.install_root
        install_target = target_root / "mods" / mod_dir.name
        if install_target.exists():
            shutil.rmtree(install_target)
        shutil.copytree(mod_dir, install_target)

    def uninstall_mod(self, mod_dir: Path, target_root: Path | None = None) -> None:
        target_root = target_root or self.install_root
        install_target = target_root / "mods" / mod_dir.name
        if install_target.exists():
            shutil.rmtree(install_target)


class GTAVAdapter(GameAdapter):
    """Example adapter for an open-world game project.

    This is a template for managing a custom mod structure. Replace the paths with
    the actual install location you own and control.
    """

    game_id = "gta_v"
    name = "GTA V"
    version = "1.0.0"
    supported_extensions = ["zip", "json", "cfg", "ini", "txt", "ytd", "ydr"]

    def validate_install(self) -> bool:
        required = [
            self.install_root / "common",
            self.install_root / "mods",
            self.install_root / "update",
        ]
        return all(path.exists() for path in required)

    def install_mod(self, mod_dir: Path, target_root: Path | None = None) -> None:
        target_root = target_root or self.install_root
        install_target = target_root / "mods" / mod_dir.name
        if install_target.exists():
            shutil.rmtree(install_target)
        shutil.copytree(mod_dir, install_target)

    def uninstall_mod(self, mod_dir: Path, target_root: Path | None = None) -> None:
        target_root = target_root or self.install_root
        install_target = target_root / "mods" / mod_dir.name
        if install_target.exists():
            shutil.rmtree(install_target)
