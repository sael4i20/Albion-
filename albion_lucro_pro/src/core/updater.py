import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests
from typing import Dict, List

class AlbionDataUpdater:
    def __init__(self, db_path: str = "./data"):
        self.db_path = db_path
        self.items_file = Path(db_path) / "itens.json"
        self.categories_file = Path(db_path) / "categorias.json"
        self.last_update_file = Path(db_path) / "last_update.txt"
        self.data_url = "https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.json"
        self.update_interval = timedelta(days=1)  # Verifica atualizações diariamente

    def needs_update(self) -> bool:
        """Verifica se precisa atualizar baseado no último update"""
        if not self.last_update_file.exists():
            return True
            
        with open(self.last_update_file, "r") as f:
            last_update = datetime.fromisoformat(f.read())
        return datetime.now() - last_update > self.update_interval

    def download_all_items(self) -> List[dict]:
        """Baixa todos os itens do repositório oficial"""
        print("⏳ Baixando metadados completos do Albion...")
        response = requests.get(self.data_url)
        response.raise_for_status()
        return response.json()

    def process_items(self, items_data: List[dict]) -> Dict[str, dict]:
        """Processa todos os itens e extrai campos relevantes"""
        processed = {}
        
        for item in items_data:
            try:
                item_id = item['UniqueName']
                processed[item_id] = {
                    "id": item_id,
                    "nome": item.get('LocalizedNames', {}).get('PT-BR', item_id),
                    "nome_en": item.get('LocalizedNames', {}).get('EN-US', ''),
                    "tier": f"T{item.get('Tier', '?')}",
                    "categoria": item.get('ItemType'),
                    "subcategoria": item.get('ItemGroup'),
                    "encantamento": item.get('EnchantmentLevel', 0),
                    "qualidade": item.get('Quality'),
                    "img_url": f"https://render.albiononline.com/v1/item/{item_id}.png",
                    "last_updated": datetime.now().isoformat()
                }
            except Exception as e:
                print(f"⚠️ Erro processando item {item.get('UniqueName')}: {str(e)}")
        
        return processed

    def update_if_needed(self) -> bool:
        """Executa atualização completa se necessário"""
        if not self.needs_update():
            return False

        try:
            # Cria diretório se não existir
            os.makedirs(self.db_path, exist_ok=True)
            
            # Baixa e processa dados
            items_data = self.download_all_items()
            processed_items = self.process_items(items_data)
            
            # Extrai categorias
            categories = {
                item_id: data['categoria'] 
                for item_id, data in processed_items.items()
                if data.get('categoria')
            }
            
            # Salva arquivos
            with open(self.items_file, 'w', encoding='utf-8') as f:
                json.dump(processed_items, f, indent=4, ensure_ascii=False)
            
            with open(self.categories_file, 'w', encoding='utf-8') as f:
                json.dump(categories, f, indent=4, ensure_ascii=False)
            
            # Atualiza timestamp
            with open(self.last_update_file, 'w') as f:
                f.write(datetime.now().isoformat())
            
            print(f"✅ Dados atualizados! {len(processed_items)} itens processados.")
            return True
            
        except Exception as e:
            print(f"❌ Falha na atualização: {str(e)}")
            return False