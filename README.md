from pathlib import Path
from typing import List, Optional
import argparse
import sys

from mod_manager import ModManager
from adapters import Manhunt1Adapter, GTAVAdapter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Universal mod manager for multiple games")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_parser = subparsers.add_parser("register", help="Register a game adapter")
    register_parser.add_argument("game", choices=["manhunt_1", "gta_v"])
    register_parser.add_argument("--install-root", type=str, default="./games")
    register_parser.add_argument("--mod-root", type=str, default="./mods")

    list_parser = subparsers.add_parser("list", help="List game IDs")

    install_parser = subparsers.add_parser("install", help="Install a mod for a game")
    install_parser.add_argument("game", choices=["manhunt_1", "gta_v"])
    install_parser.add_argument("mod_dir", type=str)

    uninstall_parser = subparsers.add_parser("uninstall", help="Remove a mod for a game")
    uninstall_parser.add_argument("game", choices=["manhunt_1", "gta_v"])
    uninstall_parser.add_argument("mod_dir", type=str)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    manager = ModManager()

    adapters = {
        "manhunt_1": Manhunt1Adapter,
        "gta_v": GTAVAdapter,
    }

    if args.command == "register":
        game_name = args.game
        install_root = Path(args.install_root) / game_name
        mod_root = Path(args.mod_root) / game_name
        adapter = adapters[game_name](install_root, mod_root)
        manager.register_adapter(adapter)
        print(f"Registered {adapter.name} at {install_root}")
        return 0

    if args.command == "list":
        print(manager.list_games())
        return 0

    if args.command == "install":
        adapter_class = adapters[args.game]
        target_root = Path("./games") / args.game
        mod_dir = Path(args.mod_dir)
        adapter = adapter_class(target_root, Path("./mods") / args.game)
        manager.adapters[args.game] = adapter
        manager.install_mod(args.game, mod_dir)
        return 0

    if args.command == "uninstall":
        adapter_class = adapters[args.game]
        target_root = Path("./games") / args.game
        mod_dir = Path(args.mod_dir)
        adapter = adapter_class(target_root, Path("./mods") / args.game)
        manager.adapters[args.game] = adapter
        manager.uninstall_mod(args.game, mod_dir)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
