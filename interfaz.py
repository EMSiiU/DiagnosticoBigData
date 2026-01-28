import customtkinter as ctk
from database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        # Botones
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
        ctk.CTkLabel(self.contenido_dinamico, text="Seleccione un reporte a generar:").pack(pady=15)
        # Botones de reportes
        #1
        ctk.CTkLabel(self.contenido_dinamico, text="1.- Listado general y filtrado por departamento").pack(pady=2)
        btn_lista = ctk.CTkButton(
            self.contenido_dinamico,
            text = "Reporte 1",
            command = self.reporte_1
            )
        btn_lista.pack(pady=5)
        #2
        ctk.CTkLabel(self.contenido_dinamico, text="2.- Managers por departamento").pack(pady=2)
        btn_managers = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Reporte 2", 
            command = self.reporte_2
            )
        btn_managers.pack(pady=5)
        #3
        ctk.CTkLabel(self.contenido_dinamico, text="3.- Empleado mejor pagado por departamento").pack(pady=2)
        btn_mjrPagado = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Reporte 3", 
            command = self.reporte_3
            )
        btn_mjrPagado.pack(pady=5)
        #4
        ctk.CTkLabel(self.contenido_dinamico, text="4.- Listado total de empleados por año").pack(pady=2)
        btn_contratados = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Reporte 4", 
            command = self.reporte_4
            )
        btn_contratados.pack(pady=5)
        #5
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
        db = Database()
        departamentos = db.departamentos()
        db.cerrar()
        # --- FILTRO ---
        filtro_frame = ctk.CTkFrame(self.contenido_dinamico)
        filtro_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(filtro_frame, text="Departamento:").pack(side="left", padx=5)
        self.dept_map = {d["dept_name"]: d["dept_no"] for d in departamentos}
        # ComboBox de departamentos
        self.combo_dept = ctk.CTkComboBox(
            filtro_frame,
            values=list(self.dept_map.keys()),
            width=250
        )
        self.combo_dept.pack(side="left", padx=5)
        # Botones de aplicar y quitar filtro
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
        ).pack(side="left", padx=10)
        # Contenedor de tabla
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        self.mostrar_tabla_empleados()

    def aplicar_filtro_departamento(self):
        dept_name = self.combo_dept.get()
        dept_no = self.dept_map.get(dept_name)
        # Mostrar tabla con filtro
        self.mostrar_tabla_empleados(dept_no)

    def quitar_filtro_departamento(self):
        # Mostrar tabla sin filtro
        self.mostrar_tabla_empleados()

    def mostrar_tabla_empleados(self, dept_no=None):
        # Limpiar tabla anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()
        # Obtener datos
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
        # Fila de encabezados
        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")
        # Filas de datos
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
            # Coloca los valores en cada celda
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
        # Contenedor de tabla
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        # Obtener datos
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
        # Fila de encabezados
        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")
        # Filas de datos
        for fila, man in enumerate(managers, start=1):
            valores = [
                man["departamento"],
                man["manager"],
                man["fecha_inicio"]
            ]
            # Coloca los valores en cada celda
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
        # Contenedor de tabla
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        # Obtener datos
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
        # Fila de encabezados
        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")
        # Filas de datos
        for fila, mp in enumerate(mejores_pagados, start=1):
            valores = [
                mp["departamento"],
                mp["no_empleado"],
                mp["empleado"],
                f"${mp['salario']}"
            ]
            # Coloca los valores en cada celda
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
        # Contenedor de tabla
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        # Obtener datos
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
        # Fila de encabezados
        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")
        # Filas de datos
        for fila, data in enumerate(empa, start=1):
            valores = [
                data["anio"],
                data["total_empleados"]
            ]
            # Coloca los valores en cada celda
            for col, valor in enumerate(valores):
                ctk.CTkLabel(tabla, text=str(valor)).grid(
                    row=fila,
                    column=col,
                    padx=8,
                    pady=4,
                    sticky="ew"
                    
                )

    def reporte_5(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Descripción de departamentos")
        # Contenedor de tabla
        self.frame_tabla = ctk.CTkFrame(self.contenido_dinamico)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        # Obtener datos
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
        # Fila de encabezados
        for col, texto in enumerate(encabezados):
            lbl = ctk.CTkLabel(
                tabla,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=8, pady=6, sticky="w")
        # Filas de datos
        for fila, data in enumerate(desc, start=1):
            valores = [
                data["departamento"],
                data["total_empleados"],
                f"${data['salario_prom']}"
            ]
            # Coloca los valores en cada celda
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
        ctk.CTkLabel(self.contenido_dinamico, text="Seleccione un tipo de gráfica a generar:").pack(pady=10)
        # Botones de gráficos
        # 1
        ctk.CTkLabel(self.contenido_dinamico, text="1.- Comparación del total de empleados por género").pack(pady=2)
        btn_grafico1 = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Gráfico 1", 
            command = self.grafico_1
            )
        btn_grafico1.pack(pady=5)
        # 2
        ctk.CTkLabel(self.contenido_dinamico, text="2.- Los 10 empleaados mejores pagados").pack(pady=2)
        btn_grafico2 = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Gráfico 2", 
            command = self.grafico_2
            )
        btn_grafico2.pack(pady=5)
        # 3
        ctk.CTkLabel(self.contenido_dinamico, text="3.- Promedio de salario por departamento").pack(pady=2)
        btn_grafico3 = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Gráfico 3", 
            command = self.grafico_3
            )
        btn_grafico3.pack(pady=5)
        # 4
        ctk.CTkLabel(self.contenido_dinamico, text="4.- Brecha salarial por cada departamento").pack(pady=2)
        btn_grafico4 = ctk.CTkButton(
            self.contenido_dinamico, 
            text = "Gráfico 4", 
            command = self.grafico_4
            )
        btn_grafico4.pack(pady=5)

    def grafico_1(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Empleados por género")
        db = Database()
        data = db.empleados_genero()
        db.cerrar()
        # Datos para la gráfica
        etiqueta = [f"{d['total_empleados']:,} {d['genero']}" for d in data]
        cifra = [d["total_empleados"] for d in data]
        # Crear figura
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")
        ax.pie(
            cifra,
            labels=etiqueta,
            autopct="%1.1f%%",
            startangle=90,
            textprops={
                "color": "white",
                "fontsize": 14
                }
        )
        ax.set_title(
            "Distribución de empleados por género", 
            color="white", 
            fontsize=16)
        ax.axis("equal")  # círculo perfecto
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.contenido_dinamico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def grafico_2(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Top 10 mejores pagados")
        db = Database()
        data = db.mejores_salarios()
        db.cerrar()
        # Datos para la gráfica
        empleados = [d["empleado"] for d in data]
        salarios = [d["salary"] for d in data]
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")
        barras = ax.barh(empleados, salarios, color="#1f77b4")
        ax.set_xlabel("Salario", color="white", fontsize=14)
        ax.set_title("Top 10 empleados mejor pagados", color="white", fontsize=14)
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")
        ax.invert_yaxis()
        # Etiquetas de salario en las barras
        for barra, salario in zip(barras, salarios):
            ax.text(
                salario + max(salarios) * 0.01,
                barra.get_y() + barra.get_height() / 2,
                f"${salario:,.0f}",
                va="center",
                color="white",
                fontsize=10
            )
        fig.tight_layout()
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.contenido_dinamico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def grafico_3(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Salario promedio por departamento")
        db = Database()
        data = db.promedio_salario_departamento()
        db.cerrar()
        # Datos para la gráfica
        departamentos = [d["departamento"] for d in data]
        salarios = [d["salario_prom"] for d in data]
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")
        barras = ax.bar(departamentos, salarios, color="#4e79a7")
        ax.set_title("Salario promedio por departamento", color="white", pad=15)
        ax.set_ylabel("Salario promedio", color="white")
        ax.tick_params(axis="x", colors="white", rotation=30)
        ax.tick_params(axis="y", colors="white")
        # Etiquetas de salario en las barras
        for barra, salario in zip(barras, salarios):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height(),
                f"${salario:,.0f}",
                ha="center",
                va="bottom",
                color="white",
                fontsize=9
            )
        fig.tight_layout()
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.contenido_dinamico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def grafico_4(self):
        self.limpiar_panel()
        self.titulo_vista.configure(text="Brecha salarial por departamento")
        db = Database()
        data = db.brecha_salarial()
        db.cerrar()
        # Datos para la gráfica
        departamentos = [d["departamento"] for d in data]
        salario_min = [d["salario_min"] for d in data]
        salario_max = [d["salario_max"] for d in data]
        diferencia = [d["diferencia"] for d in data]
        x = range(len(departamentos))
        ancho = 0.35
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")
        # Barras de salario mínimo y máximo
        ax.bar(
            [i - ancho / 2 for i in x],
            salario_min,
            width=ancho,
            label="Salario mínimo",
            color="#328827"
        )
        ax.bar(
            [i + ancho / 2 for i in x],
            salario_max,
            width=ancho,
            label="Salario máximo",
            color="#eb3134"
        )
        ax.set_title("Brecha salarial por departamento", color="white", pad=15)
        ax.set_ylabel("Salario", color="white")
        ax.set_xticks(x)
        ax.set_xticklabels(departamentos, rotation=30, ha="right", color="white")

        ax.tick_params(axis="y", colors="white")
        ax.legend(facecolor="#2b2b2b", edgecolor="white", labelcolor="white")
        # Etiquetas de salario en las barras
        for i in range(len(departamentos)):
            ax.text(
                i,
                salario_max[i] + (salario_max[i] * 0.02),
                f"Δ ${diferencia[i]:,.0f}",
                ha="center",
                va="bottom",
                color="white",
                fontsize=9,
                fontweight="bold"
            )
        fig.tight_layout()
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.contenido_dinamico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()