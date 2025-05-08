import os
import json
from pathlib import Path

def criar_estrutura_completa():
    """Cria toda a estrutura de pastas e arquivos do projeto"""
    # Lista de pastas a serem criadas
    pastas = [
        'data',
        'src/core',
        'src/gui'
    ]
    
    # Criando pastas
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        print(f'Pasta criada: {pasta}')

    # Criando arquivos essenciais
    arquivos = {
        'data/itens.json': '{}',
        '.env': 'ALBION_API_URL=https://west.albion-online-data.com/api/v2/stats',
        'requirements.txt': """customtkinter==5.2.1
requests==2.31.0
pandas==2.0.3
python-dotenv==1.0.0""",
        'src/main.py': """from dotenv import load_dotenv
from core.api import AlbionAPI
from core.database import ItemDatabase
from gui.app import AlbionLucroApp

def main():
    load_dotenv()
    api = AlbionAPI()
    db = ItemDatabase('./data/itens.json')
    app = AlbionLucroApp(api, db)
    app.mainloop()

if __name__ == "__main__":
    main()""",
        'src/core/api.py': """import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

class AlbionAPI:
    def __init__(self):
        self.base_url = os.getenv("ALBION_API_URL")

    def get_item_data(self, item_id: str) -> dict:
        url = f"{self.base_url}/items/{item_id}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()[0]

    def get_prices(self, item_id: str, cities: str = "Caerleon,Martlock") -> pd.DataFrame:
        url = f"{self.base_url}/prices/{item_id}?locations={cities}"
        response = requests.get(url)
        response.raise_for_status()
        return pd.DataFrame(response.json())""",
        'src/core/database.py': """import json
import os
from typing import Dict

class ItemDatabase:
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def load_items(self) -> Dict[str, dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_item(self, item_id: str, item_data: dict):
        items = self.load_items()
        items[item_id] = item_data
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=4, ensure_ascii=False)""",
        'src/gui/app.py': """import customtkinter as ctk
from tkinter import messagebox
from core.api import AlbionAPI
from core.database import ItemDatabase

class AlbionLucroApp(ctk.CTk):
    def __init__(self, api: AlbionAPI, db: ItemDatabase):
        super().__init__()
        self.api = api
        self.db = db
        self.title("Albion Lucro Pro")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        self._setup_ui()

    def _setup_ui(self):
        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o ID do item (ex: T4_BAG)")
        self.entry.pack(pady=20, padx=20, fill="x")

        self.btn = ctk.CTkButton(self, text="Buscar Dados", command=self._fetch_data)
        self.btn.pack(pady=10)

        self.text = ctk.CTkTextbox(self, state="disabled")
        self.text.pack(pady=20, padx=20, fill="both", expand=True)

    def _fetch_data(self):
        item_id = self.entry.get().strip()
        if not item_id:
            messagebox.showerror("Erro", "Digite um ID de item!")
            return

        try:
            item_data = self.api.get_item_data(item_id)
            prices = self.api.get_prices(item_id)
            
            self.db.save_item(item_id, {
                "nome": item_data["name"],
                "tier": item_data["tier"],
                "tipo": item_data["type"]
            })
            
            self.text.configure(state="normal")
            self.text.delete("1.0", "end")
            self.text.insert("end", f"📦 {item_data['name']} (T{item_data['tier']})\n\n")
            self.text.insert("end", f"📍 Preços:\n{prices.to_string()}")
            self.text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar dados:\n{str(e)}")"""
    }

    # Criando arquivos
    for caminho, conteudo in arquivos.items():
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f'Arquivo criado: {caminho}')

    print("\n✅ Estrutura do projeto criada com sucesso!")
    print("Instale as dependências com: pip install -r requirements.txt")
    print("Execute o projeto com: python src/main.py")

if __name__ == "__main__":
    criar_estrutura_completa()