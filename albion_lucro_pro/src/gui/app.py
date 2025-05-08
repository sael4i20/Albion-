import customtkinter as ctk
from tkinter import messagebox
from core.api import AlbionPriceAPI
from core.database import AlbionDatabase
from core.tradutor import Tradutor
from gui.components import FiltrosFrame

class AlbionLucroApp(ctk.CTk):
    def __init__(self, api: AlbionPriceAPI, db: AlbionDatabase, tradutor: Tradutor):
        super().__init__()
        self.api = api
        self.db = db
        self.tradutor = tradutor
        
        self.title("Albion Lucro Pro")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        
        self._setup_ui()

    def _setup_ui(self):
        # Configuração do grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Painel de Filtros (esquerda)
        self.filtros = FiltrosFrame(self, self._aplicar_filtros)
        self.filtros.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        
        # Painel Principal (direita)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Barra de Busca
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Digite o nome do item (ex: Espada Longa)",
            width=400
        )
        self.entry.pack(side="left", padx=5, pady=5, expand=True)
        
        self.btn_buscar = ctk.CTkButton(
            self.search_frame,
            text="Buscar",
            command=self._buscar_item
        )
        self.btn_buscar.pack(side="left", padx=5, pady=5)
        
        # Área de Resultados
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(0, weight=1)
        
        self.text = ctk.CTkTextbox(self.result_frame, state="disabled")
        self.text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def _buscar_item(self):
        termo = self.entry.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um nome para buscar!")
            return
        
        try:
            resultados = self.tradutor.buscar_por_nome(termo)
            
            if not resultados:
                messagebox.showinfo("Info", "Nenhum item encontrado com esse nome")
                return
                
            self._exibir_resultados(resultados)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na busca:\n{str(e)}")

    def _exibir_resultados(self, resultados: list):
        """Exibe os resultados na interface"""
        cidades = self.filtros.get_cidades_selecionadas()
        if not cidades:
            cidades = ["Caerleon"]  # Default
        
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        
        for item in resultados[:5]:  # Limita a 5 resultados
            try:
                precos = self.api.get_prices(item['id'], ",".join(cidades))
                
                self.text.insert("end", f"📦 {item['nome']} (T{item['tier']})\n")
                self.text.insert("end", f"🔹 Categoria: {item['categoria']}\n")
                self.text.insert("end", f"📍 Preços em {', '.join(cidades)}:\n")
                self.text.insert("end", f"{precos.to_string()}\n\n")
                
            except Exception as e:
                self.text.insert("end", f"⚠️ Erro ao buscar preços para {item['nome']}: {str(e)}\n\n")
        
        self.text.configure(state="disabled")

    def _aplicar_filtros(self, filtros: dict):
        """Aplica os filtros selecionados"""
        print("Filtros aplicados:", filtros)
        # Aqui você pode implementar a lógica de filtragem
        # Exemplo: self.db.get_items_by_category(filtros['categoria'])