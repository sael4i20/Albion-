from dotenv import load_dotenv
from core.api import AlbionPriceAPI
from core.database import AlbionDatabase
from core.tradutor import Tradutor
from gui.app import AlbionLucroApp

def setup_environment():
    """Configura o ambiente e verifica dependências"""
    load_dotenv()
    # Verifica/cria pasta de dados se necessário
    import os
    os.makedirs("./data", exist_ok=True)

def main():
    try:
        # Configuração inicial
        setup_environment()
        
        # Inicializa serviços
        db = AlbionDatabase()
        api = AlbionPriceAPI()
        tradutor = Tradutor(db)
        
        # Inicia a aplicação
        app = AlbionLucroApp(api, db, tradutor)
        app.mainloop()
        
    except Exception as e:
        print(f"⛔ Erro crítico durante inicialização: {str(e)}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()