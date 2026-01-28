import customtkinter as ctk
from database import Database

# Configuración inicial de apariencia
ctk.set_appearance_mode("dark")  

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Examen diagnostico")
        self.geometry("1200x700")

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
        self.titulo_vista.configure(text="Menú de Reportes")
        #grid_reportes = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        #grid_reportes.pack(pady=20, padx=20, fill="both")
        ctk.CTkLabel(self.contenido_dinamico, text="Seleccione un reporte a generar:").pack(pady=15)
        
        ctk.CTkLabel(self.contenido_dinamico, text="1.- Listado general y filtrado por departamento").pack(pady=2)
        btn_lista = ctk.CTkButton(
            self.contenido_dinamico,
            text = "Reporte 1",
            command = self.reporte_1
            )
        btn_lista.pack(pady=5)

        ctk.CTkLabel(self.contenido_dinamico, text="2.- Managers por departamento").pack(pady=2)
        btn_managers = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Reporte 2", 
            command = self.reporte_2
            )
        btn_managers.pack(pady=5)

        ctk.CTkLabel(self.contenido_dinamico, text="3.- Empleado mejor pagado por departamento").pack(pady=2)
        btn_mjrPagado = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Reporte 3", 
            command = self.reporte_3
            )
        btn_mjrPagado.pack(pady=5)

        ctk.CTkLabel(self.contenido_dinamico, text="4.- Listado total de empleados por año").pack(pady=2)
        btn_contratados = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Reporte 4", 
            command = self.reporte_4
            )
        btn_contratados.pack(pady=5)

        ctk.CTkLabel(self.contenido_dinamico, text="5.- Listado descripción de departamento").pack(pady=2)
        btn_descripcion = ctk.CTkButton(
            self.contenido_dinamico, 
            text="Reporte 5", 
            command=self.reporte_5
            )
        btn_descripcion.pack(pady=5)
        
    def reporte_1(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Listado de empleados")

        # --- FILTRO ---
        filtro_frame = ctk.CTkFrame(self.contenido_dinamico)
        filtro_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(filtro_frame, text="Departamento:").pack(side="left", padx=5)

        db = Database()
        departamentos = db.departamentos()
        db.cerrar()

        self.dept_map = {d["dept_name"]: d["dept_no"] for d in departamentos}

        self.combo_dept = ctk.CTkComboBox(
            filtro_frame,
            values=list(self.dept_map.keys()),
            width=250
        )
        self.combo_dept.pack(side="left", padx=5)

        ctk.CTkButton(
            filtro_frame,
            text="Aplicar filtro",
            command=self.aplicar_filtro_departamento
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            filtro_frame,
            text="Quitar filtro",
            fg_color="#B22222",
            hover_color="#8B1A1A",
            command=self.quitar_filtro_departamento
        ).pack(side="left", padx=5)

        # --- CONTENEDOR DE TABLA ---
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.mostrar_tabla_empleados()

    def aplicar_filtro_departamento(self):
        dept_name = self.combo_dept.get()
        dept_no = self.dept_map.get(dept_name)

        self.mostrar_tabla_empleados(dept_no)

    def quitar_filtro_departamento(self):
        self.mostrar_tabla_empleados()

    def mostrar_tabla_empleados(self, dept_no=None):
        # Limpiar tabla anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        db = Database()
        empleados = db.empleados(dept_no)
        db.cerrar()

        # Frame con scroll
        tabla = ctk.CTkScrollableFrame(self.frame_tabla)
        tabla.pack(fill="both", expand=True)

        # Encabezados
        encabezados = [
            "No. Emp",
            "Nombres",
            "Apellidos",
            "Nacimiento",
            "Género",
            "Contratación",
            "Departamento",
            "Título",
            "Salario"
        ]

        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")

        # Filas
        for fila, emp in enumerate(empleados, start=1):
            valores = [
                emp["no_empleado"],
                emp["nombres"],
                emp["apellidos"],
                emp["nacimiento"],
                emp["genero"],
                emp["contratacion"],
                emp["departamento"],
                emp["titulo_actual"],
                f"${emp['salario_actual']}"
            ]

            for col, valor in enumerate(valores):
                ctk.CTkLabel(tabla, text=str(valor)).grid(
                    row=fila,
                    column=col,
                    padx=8,
                    pady=4,
                    sticky="w"
                )

    def reporte_2(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Listado de managers")

        # --- CONTENEDOR DE TABLA ---
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        db = Database()
        managers = db.managers()
        db.cerrar()

        # Frame con scroll
        tabla = ctk.CTkScrollableFrame(self.frame_tabla)
        tabla.pack(fill="both", expand=True)

        # Encabezados
        encabezados = [
            "Departamento",
            "Manager",
            "Fecha Inicio"
        ]

        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")

        # Filas
        for fila, man in enumerate(managers, start=1):
            valores = [
                man["departamento"],
                man["manager"],
                man["fecha_inicio"]
            ]

            for col, valor in enumerate(valores):
                ctk.CTkLabel(tabla, text=str(valor)).grid(
                    row=fila,
                    column=col,
                    padx=8,
                    pady=4,
                    sticky="w"
                )

    def reporte_3(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Mejores pagados por departamento")

        # --- CONTENEDOR DE TABLA ---
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        db = Database()
        mejores_pagados = db.mejores_pagados()
        db.cerrar()

        # Frame con scroll
        tabla = ctk.CTkScrollableFrame(self.frame_tabla)
        tabla.pack(fill="both", expand=True)

        # Encabezados
        encabezados = [
            "Departamento",
            "No. Empleado",
            "Empleado",
            "Salario"
        ]

        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")

        # Filas
        for fila, mp in enumerate(mejores_pagados, start=1):
            valores = [
                mp["departamento"],
                mp["no_empleado"],
                mp["empleado"],
                f"${mp['salario']}"
            ]

            for col, valor in enumerate(valores):
                ctk.CTkLabel(tabla, text=str(valor)).grid(
                    row=fila,
                    column=col,
                    padx=8,
                    pady=4,
                    sticky="w"
                )

    def reporte_4(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Empleados por año")

        # --- CONTENEDOR DE TABLA ---
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        db = Database()
        empa = db.empleados_por_anio()
        db.cerrar()

        # Frame con scroll
        tabla = ctk.CTkScrollableFrame(self.frame_tabla)
        tabla.pack(fill="both", expand=True)

        # Encabezados
        encabezados = [
            "Año",
            "Total Empleados Contratados"
        ]

        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")

        # Filas
        for fila, data in enumerate(empa, start=1):
            valores = [
                data["anio"],
                data["total_empleados"]
            ]

            for col, valor in enumerate(valores):
                ctk.CTkLabel(tabla, text=str(valor)).grid(
                    row=fila,
                    column=col,
                    padx=8,
                    pady=4,
                    sticky="w"
                )

    def reporte_5(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Descripción de departamentos")

        # --- CONTENEDOR DE TABLA ---
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        db = Database()
        desc = db.descripcion_dep()
        db.cerrar()

        # Frame con scroll
        tabla = ctk.CTkScrollableFrame(self.frame_tabla)
        tabla.pack(fill="both", expand=True)

        # Encabezados
        encabezados = [
            "Departamento",
            "Total Empleados",
            "Salario Promedio"
        ]

        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")

        # Filas
        for fila, data in enumerate(desc, start=1):
            valores = [
                data["departamento"],
                data["total_empleados"],
                f"${data['salario_prom']}"
            ]

            for col, valor in enumerate(valores):
                ctk.CTkLabel(tabla, text=str(valor)).grid(
                    row=fila,
                    column=col,
                    padx=8,
                    pady=4,
                    sticky="w"
                )

    def mostrar_vista_graficos(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Menú de Gráficos")
        #grid_graficos = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        #grid_graficos.pack(pady=20, padx=20, fill="both")
        ctk.CTkLabel(self.contenido_dinamico, text="Seleccione un tipo de gráfica a generar:").pack(pady=10)

        ctk.CTkLabel(self.contenido_dinamico, text="1.- Comparación del total de empleados por género").pack(pady=2)
        btn_grafico1 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 1", command=lambda: print("Gráfico 1"))
        btn_grafico1.pack(pady=5)

        ctk.CTkLabel(self.contenido_dinamico, text="2.- Los 10 empleaados mejores pagados").pack(pady=2)
        btn_grafico2 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 2", command=lambda: print("Gráfico 2"))
        btn_grafico2.pack(pady=5)

        ctk.CTkLabel(self.contenido_dinamico, text="3.- Promedio de salario por departamento").pack(pady=2)
        btn_grafico3 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 3", command=lambda: print("Gráfico 3"))
        btn_grafico3.pack(pady=5)

        ctk.CTkLabel(self.contenido_dinamico, text="4.- Brecha salarial por cada departamento").pack(pady=2)
        btn_grafico4 = ctk.CTkButton(self.contenido_dinamico, text="Gráfico 4", command=lambda: print("Gráfico 4"))
        btn_grafico4.pack(pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()