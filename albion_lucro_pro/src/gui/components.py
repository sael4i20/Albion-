import customtkinter as ctk
from typing import Callable, List

class FiltrosFrame(ctk.CTkFrame):
    def __init__(self, master, on_filter_change: Callable):
        super().__init__(master)
        self.on_filter_change = on_filter_change
        self._setup_ui()

    def _setup_ui(self):
        # Configuração do grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Filtro de Categoria
        ctk.CTkLabel(self, text="Categoria:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.categoria_var = ctk.StringVar(value="Todos")
        categorias = ["Todos", "Armas", "Armaduras", "Consumíveis", "Materiais"]
        ctk.CTkOptionMenu(self, variable=self.categoria_var, values=categorias,
                         command=lambda _: self._notify_change()).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Filtro de Tier
        ctk.CTkLabel(self, text="Tier:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.tier_var = ctk.StringVar(value="Todos")
        tiers = ["Todos"] + [f"T{i}" for i in range(4, 9)]
        ctk.CTkOptionMenu(self, variable=self.tier_var, values=tiers,
                         command=lambda _: self._notify_change()).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Filtro de Cidades
        ctk.CTkLabel(self, text="Cidades:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cidades_frame = ctk.CTkFrame(self)
        self.cidades_frame.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        cidades = ["Caerleon", "Bridgewatch", "Thetford", "Fort Sterling", "Martlock"]
        self.cidade_vars = {}
        
        for i, cidade in enumerate(cidades):
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(self.cidades_frame, text=cidade, variable=var,
                                command=self._notify_change)
            cb.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            self.cidade_vars[cidade] = var

    def _notify_change(self):
        """Notifica sobre mudanças nos filtros"""
        filtros = {
            "categoria": self.categoria_var.get(),
            "tier": self.tier_var.get(),
            "cidades": [cidade for cidade, var in self.cidade_vars.items() if var.get()]
        }
        self.on_filter_change(filtros)

    def get_cidades_selecionadas(self) -> List[str]:
        """Retorna a lista de cidades selecionadas"""
        return [cidade for cidade, var in self.cidade_vars.items() if var.get()]