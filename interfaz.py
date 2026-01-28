import customtkinter as ctk

# Configuración inicial de apariencia
ctk.set_appearance_mode("dark")  

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Examen diagnostico")
        self.geometry("1100x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Componentes
        self.crear_menu_lateral()
        self.crear_panel_contenido()

    def crear_menu_lateral(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Título
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Tipos de reportes", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botoines
        self.btn_reportes = ctk.CTkButton(self.sidebar_frame, text="Reportes", command=self.mostrar_vista_reportes)
        self.btn_reportes.grid(row=1, column=0, padx=20, pady=10)

        self.btn_graficos = ctk.CTkButton(self.sidebar_frame, text="Gráficos",command=self.mostrar_vista_graficos)
        self.btn_graficos.grid(row=2, column=0, padx=20, pady=10)

    def crear_panel_contenido(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.titulo_vista = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=24))
        self.titulo_vista.pack(pady=20)

        # Frame contenedor dinámico (aquí pondremos las tablas o gráficas)
        self.contenido_dinamico = ctk.CTkFrame(self.main_frame)
        self.contenido_dinamico.pack(fill="both", expand=True, padx=10, pady=10)

    def limpiar_panel(self):
        for widget in self.contenido_dinamico.winfo_children():
            widget.destroy()

    def mostrar_vista_reportes(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Reportes de Empleados")
        #grid_reportes = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        #grid_reportes.pack(pady=20, padx=20, fill="both")
        ctk.CTkLabel(self.contenido_dinamico, text="Seleccione un reporte a generar:").pack(pady=10)
        
        btn_lista = ctk.CTkButton(self.contenido_dinamico, text="Listado general y filtrado", command=lambda: print("Reporte 1"))
        btn_lista.pack(pady=5)
        
        btn_managers = ctk.CTkButton(self.contenido_dinamico, text="Managers por Depto", command=lambda: print("Reporte 2"))
        btn_managers.pack(pady=5)

        btn_mjrPagado = ctk.CTkButton(self.contenido_dinamico, text="Empleado mejor pagado por Depto", command=lambda: print("Reporte 3"))
        btn_mjrPagado.pack(pady=5)

        btn_contratados = ctk.CTkButton(self.contenido_dinamico, text="Listado total de empleados por año", command=lambda: print("Reporte 4"))
        btn_contratados.pack(pady=5)

        btn_managers = ctk.CTkButton(self.contenido_dinamico, text="Listado descipcion de Depto", command=lambda: print("Reporte 5"))
        btn_managers.pack(pady=5)
        

    def mostrar_vista_graficos(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Análisis Gráfico")
        #grid_graficos = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        #grid_graficos.pack(pady=20, padx=20, fill="both")
        ctk.CTkLabel(self.contenido_dinamico, text="Seleccione un tipo de gráfica a generar:").pack(pady=10)

        btn_grafico1 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 1", command=lambda: print("Gráfico 1"))
        btn_grafico1.pack(pady=5)

        btn_grafico2 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 2", command=lambda: print("Gráfico 2"))
        btn_grafico2.pack(pady=5)

        btn_grafico3 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 3", command=lambda: print("Gráfico 3"))
        btn_grafico3.pack(pady=5)

        btn_grafico4 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 4", command=lambda: print("Gráfico 4"))
        btn_grafico4.pack(pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()