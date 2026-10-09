# Universal Mod Manager

A starter project for a universal modding tool that can manage multiple game-specific mod systems through a shared interface.

This repository is intentionally designed as a safe, generic framework:
- it helps you organize mods by game
- it supports a plugin-like adapter architecture
- it keeps legal and ethical boundaries clear
- it avoids bundling or redistributing copyrighted game assets

## Purpose

This project is meant to manage custom mod packs and game-specific logic in a modular way. It is not a cracked game loader or a tool for extracting protected game data.

For a crossover concept like "Manhunt 1 + GTA V", the safe approach is:
- create your own original mod pack or project
- use your own custom assets and config
- keep game integration separate per title
- merge gameplay ideas only in an original, legal project

## Project structure

- `game_registry.py` : tracks supported games and their install directories
- `base_adapter.py` : abstract adapter interface every game plugin must follow
- `mod_manager.py` : installs, uninstalls, and tracks current mods
- `adapters.py` : example adapters for `manhunt_1` and `gta_v`
- `main.py` : command-line entry point for registering and installing mods

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python main.py register manhunt_1 --install-root ./games --mod-root ./mods
python main.py register gta_v --install-root ./games --mod-root ./mods
python main.py list
```

## Example usage

```bash
python main.py install manhunt_1 ./modpacks/my_custom_stealth_pack
python main.py install gta_v ./modpacks/my_custom_openworld_pack
```

## Notes

- Update install paths to the games you actually own and control.
- Use original assets or assets you are legally allowed to use.
- This project is a framework starter, not a direct game merge.

## Future improvements

- GUI front-end
- mod manifest support
- dependency validation
- backup/restore system
- version compatibility checks
- per-game metadata and compatibility profiles

## License

MIT
