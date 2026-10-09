"""
Game Registry Module
Manages registration and discovery of supported games and their adapters.
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class GameConfig:
    """Configuration for a registered game."""
    game_id: str
    name: str
    version: str
    install_path: Path
    mod_folder: Path
    adapter_class: str
    supports_backup: bool = True
    max_mod_size_mb: int = 2048
    supported_formats: List[str] = None
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ["zip", "rar", "7z"]


class GameRegistry:
    """Central registry for all supported games and their configurations."""
    
    def __init__(self, registry_file: Path = None):
        """
        Initialize the game registry.
        
        Args:
            registry_file: Path to JSON file storing game configurations.
                          Defaults to ~/.universal_mod_manager/games.json
        """
        if registry_file is None:
            registry_file = Path.home() / ".universal_mod_manager" / "games.json"
        
        self.registry_file = registry_file
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.games: Dict[str, GameConfig] = {}
        self._adapters: Dict[str, type] = {}
        self.load_registry()
    
    def register_game(self, config: GameConfig) -> bool:
        """
        Register a new game in the registry.
        
        Args:
            config: GameConfig instance for the game
            
        Returns:
            True if successful, False if game already exists
        """
        if config.game_id in self.games:
            print(f"⚠️  Game '{config.game_id}' is already registered.")
            return False
        
        # Validate paths exist
        if not config.install_path.exists():
            print(f"❌ Install path does not exist: {config.install_path}")
            return False
        
        # Create mod folder if it doesn't exist
        config.mod_folder.mkdir(parents=True, exist_ok=True)
        
        self.games[config.game_id] = config
        self.save_registry()
        print(f"✅ Game '{config.name}' registered successfully.")
        return True
    
    def unregister_game(self, game_id: str) -> bool:
        """
        Unregister a game from the registry.
        
        Args:
            game_id: ID of the game to unregister
            
        Returns:
            True if successful, False if game not found
        """
        if game_id not in self.games:
            print(f"❌ Game '{game_id}' not found in registry.")
            return False
        
        del self.games[game_id]
        self.save_registry()
        print(f"✅ Game '{game_id}' unregistered.")
        return True
    
    def get_game(self, game_id: str) -> Optional[GameConfig]:
        """
        Retrieve a game configuration by ID.
        
        Args:
            game_id: ID of the game
            
        Returns:
            GameConfig if found, None otherwise
        """
        return self.games.get(game_id)
    
    def list_games(self) -> List[str]:
        """
        Get list of all registered game IDs.
        
        Returns:
            List of game IDs
        """
        return list(self.games.keys())
    
    def list_games_detailed(self) -> List[Dict]:
        """
        Get detailed information about all registered games.
        
        Returns:
            List of game information dictionaries
        """
        return [
            {
                "id": game_id,
                "name": config.name,
                "version": config.version,
                "install_path": str(config.install_path),
                "mod_folder": str(config.mod_folder),
                "supported_formats": config.supported_formats
            }
            for game_id, config in self.games.items()
        ]
    
    def register_adapter(self, game_id: str, adapter_class: type) -> bool:
        """
        Register an adapter class for a game.
        
        Args:
            game_id: ID of the game
            adapter_class: The adapter class to register
            
        Returns:
            True if successful
        """
        if game_id not in self.games:
            print(f"❌ Game '{game_id}' not found in registry.")
            return False
        
        self._adapters[game_id] = adapter_class
        print(f"✅ Adapter registered for game '{game_id}'.")
        return True
    
    def get_adapter(self, game_id: str) -> Optional[type]:
        """
        Retrieve the adapter class for a game.
        
        Args:
            game_id: ID of the game
            
        Returns:
            Adapter class if found, None otherwise
        """
        return self._adapters.get(game_id)
    
    def save_registry(self) -> None:
        """Save the current registry to disk."""
        registry_data = {
            game_id: {
                "name": config.name,
                "version": config.version,
                "install_path": str(config.install_path),
                "mod_folder": str(config.mod_folder),
                "adapter_class": config.adapter_class,
                "supports_backup": config.supports_backup,
                "max_mod_size_mb": config.max_mod_size_mb,
                "supported_formats": config.supported_formats
            }
            for game_id, config in self.games.items()
        }
        
        with open(self.registry_file, "w") as f:
            json.dump(registry_data, f, indent=2)
        print(f"📁 Registry saved to {self.registry_file}")
    
    def load_registry(self) -> None:
        """Load the registry from disk."""
        if not self.registry_file.exists():
            print("ℹ️  No existing registry found. Starting fresh.")
            return
        
        try:
            with open(self.registry_file, "r") as f:
                registry_data = json.load(f)
            
            for game_id, data in registry_data.items():
                config = GameConfig(
                    game_id=game_id,
                    name=data["name"],
                    version=data["version"],
                    install_path=Path(data["install_path"]),
                    mod_folder=Path(data["mod_folder"]),
                    adapter_class=data["adapter_class"],
                    supports_backup=data.get("supports_backup", True),
                    max_mod_size_mb=data.get("max_mod_size_mb", 2048),
                    supported_formats=data.get("supported_formats", ["zip", "rar", "7z"])
                )
                self.games[game_id] = config
            
            print(f"✅ Registry loaded. Found {len(self.games)} game(s).")
        
        except json.JSONDecodeError:
            print("❌ Error loading registry: Invalid JSON format.")
        except Exception as e:
            print(f"❌ Error loading registry: {e}")
    
    def validate_game_paths(self, game_id: str) -> bool:
        """
        Validate that all required paths for a game exist and are accessible.
        
        Args:
            game_id: ID of the game to validate
            
        Returns:
            True if all paths are valid
        """
        config = self.get_game(game_id)
        if not config:
            print(f"❌ Game '{game_id}' not found.")
            return False
        
        if not config.install_path.exists():
            print(f"❌ Install path missing: {config.install_path}")
            return False
        
        if not config.mod_folder.exists():
            print(f"⚠️  Mod folder missing, attempting to create: {config.mod_folder}")
            try:
                config.mod_folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"❌ Failed to create mod folder: {e}")
                return False
        
        print(f"✅ All paths valid for '{config.name}'")
        return True


# Example usage
if __name__ == "__main__":
    # Create registry
    registry = GameRegistry()
    
    # Example: Register GTA V
    gta_config = GameConfig(
        game_id="gta_v",
        name="Grand Theft Auto V",
        version="1.58",
        install_path=Path("C:/Program Files/Rockstar Games/Grand Theft Auto V"),
        mod_folder=Path("C:/Program Files/Rockstar Games/Grand Theft Auto V/mods"),
        adapter_class="GTAVAdapter",
        supported_formats=["zip", "rar"]
    )
    registry.register_game(gta_config)
    
    # List games
    print("\nRegistered games:")
    for game in registry.list_games_detailed():
        print(f"  - {game['name']} ({game['id']})")
