import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor(dictionary = True)

    def cerrar(self):
        self.cursor.close()
        self.conn.close()

    def departamentos(self):
        query = "SELECT * FROM departments ORDER BY dept_name"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def empleados(self, dept_no = None):
        query = """
        SELECT
            e.emp_no AS no_empleado,
            e.first_name AS nombres,
            e.last_name AS apellidos,
            e.birth_date AS nacimiento,
            e.gender AS genero,
            e.hire_date AS contratacion,
            d.dept_name AS departamento,
            t.title AS titulo_actual,
            s.salary AS salario_actual
        FROM employees e
        JOIN dept_emp de ON e.emp_no = de.emp_no
        JOIN departments d ON de.dept_no = d.dept_no
        JOIN titles t ON e.emp_no = t.emp_no
        JOIN salaries s ON e.emp_no = s.emp_no
        WHERE de.to_date = '9999-01-01'
            AND t.to_date = '9999-01-01'
            AND s.to_date = '9999-01-01'
        """
        params = []
        if dept_no:
            query += " AND d.dept_no = %s"
            params.append(dept_no)
        query += "ORDER BY e.emp_no LIMIT 50"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def managers(self):
        query = """
        SELECT
            d.dept_name AS departamento,
            CONCAT(e.first_name, ' ', e.last_name) AS manager,
            dm.from_date AS fecha_inicio
        FROM dept_manager dm
        JOIN departments d
            ON dm.dept_no = d.dept_no
        JOIN employees e
            ON dm.emp_no = e.emp_no
        WHERE dm.to_date = '9999-01-01'
        ORDER BY d.dept_name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def mejores_pagados(self):
        query = """
        SELECT
            d.dept_name AS departamento,
            e.emp_no AS no_empleado,
            CONCAT(e.first_name, ' ', e.last_name) AS empleado,
            s.salary AS salario
        FROM departments d
        JOIN dept_emp de
            ON d.dept_no = de.dept_no
        AND de.to_date = '9999-01-01'
        JOIN employees e
            ON de.emp_no = e.emp_no
        JOIN salaries s
            ON e.emp_no = s.emp_no
        AND s.to_date = '9999-01-01'
        JOIN (
            SELECT de2.dept_no, MAX(s2.salary) AS max_salary
            FROM dept_emp de2
            JOIN salaries s2
                ON de2.emp_no = s2.emp_no
            AND s2.to_date = '9999-01-01'
            WHERE de2.to_date = '9999-01-01'
            GROUP BY de2.dept_no
        ) ms
            ON ms.dept_no = d.dept_no
        AND ms.max_salary = s.salary
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def empleados_por_anio(self):
        query = """
        SELECT
            YEAR(hire_date) AS anio,
            COUNT(*) AS total_empleados
        FROM employees
        GROUP BY YEAR(hire_date)
        ORDER BY anio
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def descripcion_dep(self):
        query = """
        SELECT
            d.dept_name AS departamento,
            COUNT(de.emp_no) AS total_empleados,
            ROUND(AVG(s.salary),2) AS salario_prom
        FROM departments d
            JOIN dept_emp de
                ON d.dept_no = de.dept_no
                AND de.to_date = '9999-01-01'
            JOIN salaries s
                ON s.emp_no = de.emp_no
                AND s.to_date = '9999-01-01'
        GROUP BY d.dept_no, d.dept_name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def empleados_genero(self):
        query = """
        SELECT
            CASE gender
                WHEN 'M' THEN 'Hombres'
                WHEN 'F' THEN 'Mujeres'
            END AS genero,
            COUNT(*) AS total_empleados
        FROM employees
        GROUP BY gender
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def mejores_salarios(self):
        query = """
        SELECT
            CONCAT(e.first_name, ' ', e.last_name) AS empleado,
            s.salary
        FROM employees e
            JOIN salaries s
                ON e.emp_no = s.emp_no
                AND s.to_date = '9999-01-01'
        ORDER BY s.salary desc
        LIMIT 10
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def promedio_salario_departamento(self):
        query = """
        SELECT
            d.dept_name AS departamento,
            ROUND(AVG(s.salary),2) AS salario_prom
        FROM departments d
            JOIN dept_emp de
                ON d.dept_no = de.dept_no
                AND de.to_date = '9999-01-01'
            JOIN salaries s
                ON s.emp_no = de.emp_no
                AND s.to_date = '9999-01-01'
        GROUP BY d.dept_no, d.dept_name
        ORDER BY salario_prom DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def brecha_salarial(self):
        query = """
        SELECT
            d.dept_name AS departamento,
            MAX(s.salary) AS salario_max,
            MIN(s.salary) AS salario_min,
            (MAX(s.salary) - MIN(s.salary)) AS diferencia
        FROM departments d
            JOIN dept_emp de
                ON d.dept_no = de.dept_no
                AND de.to_date = '9999-01-01'
            JOIN salaries s
                ON s.emp_no = de.emp_no
                AND s.to_date = '9999-01-01'
        GROUP BY d.dept_no, d.dept_name
        ORDER BY d.dept_name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

# Ejemplo para probar la clase Database
if __name__ == "__main__":
    db = Database()
    datos = db.empleados(dept_no='d001')
    print(datos[:10])
    db.cerrar()