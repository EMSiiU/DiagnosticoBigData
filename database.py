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
    
if __name__ == "__main__":
    db = Database()
    datos = db.empleados(dept_no='d001')
    print(datos[:10])
    db.cerrar()