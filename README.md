# Proyecto: API para Informes de Contrataciones

## Descripción

Esta API permite consultar información sobre las contrataciones realizadas por departamentos en una organización durante el año 2021. Proporciona datos clave como:

1. El número de empleados contratados por cada puesto y departamento dividido por trimestre.
2. Departamentos que contrataron más empleados que el promedio, junto con el número de empleados contratados, ordenados en orden descendente.

---

## Endpoints Disponibles

### 1. **Consultar contrataciones por trimestre**

**URL**: `/hiring/report-by-quarter`

**Método**: `GET`

**Descripción**:
Devuelve el número de empleados contratados por cada puesto y departamento en 2021, dividido por trimestres. Los resultados están ordenados alfabéticamente por departamento y puesto.

**Ejemplo de Respuesta**:
```json
{
  "data": [
    {
      "department_name": "Engineering",
      "job_title": "Software Engineer",
      "quarter": 1,
      "hired_count": 25
    },
    {
      "department_name": "Sales",
      "job_title": "Sales Manager",
      "quarter": 1,
      "hired_count": 15
    }
  ]
}
```

---

### 2. **Departamentos con contrataciones superiores al promedio**

**URL**: `/departments/above-average`

**Método**: `GET`

**Descripción**:
Devuelve una lista de departamentos que contrataron más empleados que la media de empleados contratados en 2021. Los resultados están ordenados por el número de contrataciones en orden descendente.

**Ejemplo de Respuesta**:
```json
{
  "data": [
    {
      "department_id": 5,
      "department_name": "Engineering",
      "hired_count": 120
    },
    {
      "department_id": 2,
      "department_name": "Sales",
      "hired_count": 95
    }
  ]
}
```

---

## Requisitos del Proyecto

### Dependencias Principales

- **Python 3.9+**
- **FastAPI**: Framework para construir la API.
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **PostgreSQL**: Base de datos utilizada para almacenar los datos.

### Instalación

1. Clonar este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-proyecto>
   ```

2. Crear un entorno virtual e instalar las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar las variables de entorno:
   Crear un archivo `.env` en la raíz del proyecto con los siguientes valores:
   ```env
   DATABASE_URL=postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_datos>
   ```

4. Inicializar la base de datos:
   ```bash
   python -m models
   ```

5. Ejecutar el servidor:
   ```bash
   uvicorn main:app --reload
   ```

---

## Uso

1. Accede a la documentación interactiva de la API en:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

2. Realiza las consultas utilizando herramientas como Postman, cURL o directamente desde el navegador.

---

## Estructura del Proyecto

```
.
├── main.py                # Archivo principal de la API
├── models.py              # Definición de los modelos SQLAlchemy
├── database.py            # Configuración de la base de datos
├── requirements.txt       # Lista de dependencias
├── README.md              # Documentación del proyecto
├── .env                   # Variables de entorno
```

---