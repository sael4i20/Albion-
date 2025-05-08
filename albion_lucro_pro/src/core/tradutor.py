import json
from fuzzywuzzy import fuzz
from typing import Dict, List
from core.database import ItemDatabase
from core.api import AlbionAPI

class Tradutor:
    def __init__(self, db: ItemDatabase, api: AlbionAPI):
        self.db = db
        self.api = api
        self.itens = self.db.load_items()
        self.categorias = self.db.load_categories()

        if self.db.needs_initial_load():
            self._carregar_dados_iniciais()

    def _carregar_dados_iniciais(self):
        """Popula os arquivos de cache na primeira execução"""
        print("⏳ Carregando metadados dos itens pela primeira vez...")
        
        try:
            # Busca todos os itens do repositório oficial
            itens_api = self.api.get_all_items_metadata()
            
            # Processa os dados
            itens_cache = {}
            categorias_cache = {}
            
            for item in itens_api:
                item_id = item.get('UniqueName')
                if item_id:
                    itens_cache[item_id] = {
                        "nome": item.get('LocalizedNames', {}).get('PT-BR', item_id),
                        "tier": f"T{item.get('Tier', '?')}",
                        "categoria": item.get('ItemType'),
                        "subcategoria": item.get('ItemGroup'),
                        "encantamento": item.get('EnchantmentLevel', 0)
                    }
                    
                    # Mapeia categoria
                    if item_id not in categorias_cache:
                        categorias_cache[item_id] = item.get('ItemType', 'Desconhecida')
            
            # Salva no cache
            self.db.save_all_data(itens_cache, categorias_cache)
            self.itens = itens_cache
            self.categorias = categorias_cache
            
            print("✅ Metadados carregados com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao carregar metadados: {str(e)}")

    def buscar_por_nome(self, nome: str) -> List[dict]:
        """Busca itens por nome (com fuzzy matching)"""
        resultados = []
        for item_id, dados in self.itens.items():
            similaridade = fuzz.ratio(nome.lower(), dados["nome"].lower())
            if similaridade > 70:  # Threshold ajustável
                resultados.append({
                    "id": item_id,
                    **dados,
                    "similaridade": similaridade
                })
        
        return sorted(resultados, key=lambda x: x["similaridade"], reverse=True)[:10]  # Top 10