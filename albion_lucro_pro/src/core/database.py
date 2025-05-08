import json
import os
from typing import Dict, List
from pathlib import Path

class ItemDatabase:
    def __init__(self, items_path: str = "./data/itens.json", 
                 categories_path: str = "./data/categorias.json"):
        self.items_path = items_path
        self.categories_path = categories_path
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Garante que o diretório data existe"""
        Path("./data").mkdir(exist_ok=True)

    def load_items(self) -> Dict[str, dict]:
        """Carrega itens do cache local"""
        try:
            with open(self.items_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_categories(self) -> Dict[str, str]:
        """Carrega categorias do cache local"""
        try:
            with open(self.categories_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_all_data(self, items: Dict[str, dict], categories: Dict[str, str]):
        """Salva todos os dados no cache"""
        with open(self.items_path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=4, ensure_ascii=False)
        
        with open(self.categories_path, "w", encoding="utf-8") as f:
            json.dump(categories, f, indent=4, ensure_ascii=False)

    def needs_initial_load(self) -> bool:
        """Verifica se precisa carregar dados iniciais"""
        return not (os.path.exists(self.items_path) and os.path.exists(self.categories_path))