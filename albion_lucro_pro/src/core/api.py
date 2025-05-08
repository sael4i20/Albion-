import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

class AlbionPriceAPI:
    def __init__(self):
        self.base_url = os.getenv("ALBION_API_URL")
        
    def get_prices(self, item_id: str, locations: str = "Caerleon,Martlock") -> pd.DataFrame:
        """Busca preços atuais nas cidades especificadas"""
        url = f"{self.base_url}/prices/{item_id}?locations={locations}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    
    def get_historical_prices(self, item_id: str, time_scale: int = 7) -> pd.DataFrame:
        """Busca histórico de preços"""
        url = f"{self.base_url}/history/{item_id}?time-scale={time_scale}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())