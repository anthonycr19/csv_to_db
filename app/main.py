from fastapi import FastAPI, UploadFile, Depends, HTTPException, File
from sqlalchemy.orm import Session, mapper
from . import models
from datetime import datetime
from sqlalchemy.sql import text

from app.database import Base, engine, get_db
import pandas as pd

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/post-csv/")
async def send_csv(
        jobs_file: UploadFile = File(...),
        departments_file: UploadFile = File(...),
        employees_file: UploadFile = File(...),
        db: Session = Depends(get_db)):

    if not jobs_file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="La extesión del archivo debe ser CSV obligatoriamente")
    if not departments_file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="La extesión del archivo debe ser CSV obligatoriamente")
    if not employees_file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="La extesión del archivo debe ser CSV oblogatoriamente")

    # Leer el archivo CSV en un DataFrame de pandas
    # Leer los archivos CSV
    jobs_df = pd.read_csv(jobs_file.file, header=None, names=["id", "job_title"])
    departments_df = pd.read_csv(departments_file.file, header=None, names=["id", "name"])
    employees_df = pd.read_csv(employees_file.file, header=None,
                               names=["id", "name", "datetime", "department_id", "job_id"])

    # Validar y limpiar datos
    employees_df["id"] = pd.to_numeric(employees_df["id"], errors="coerce", downcast="integer")
    employees_df["job_id"] = pd.to_numeric(employees_df["job_id"], errors="coerce", downcast="integer")
    employees_df["department_id"] = pd.to_numeric(employees_df["department_id"], errors="coerce", downcast="integer")
    employees_df["datetime"] = pd.to_datetime(employees_df["datetime"], errors="coerce", utc=True)

    # Eliminar filas con valores nulos en columnas obligatorias
    employees_df = employees_df.dropna(subset=["id", "name", "datetime", "job_id", "department_id"])

    # Convertir los DataFrames a listas de diccionarios
    jobs_data = jobs_df.to_dict(orient="records")
    departments_data = departments_df.to_dict(orient="records")
    employees_data = employees_df.to_dict(orient="records")

    # Insertar los datos en la base de datos
    try:
        db.bulk_insert_mappings(models.Job, jobs_data)
        db.bulk_insert_mappings(models.Department, departments_data)
        db.bulk_insert_mappings(models.HiredEmployee, employees_data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar los datos en la base de datos: {e}")

    return {"message": "Los datos han sido guardados correctamente en la BD"}


@app.get("/employees/hired-per-quarter")
def hired_employees_by_quarter(db: Session = Depends(get_db)):
    query = text("""
    SELECT 
        d.name AS department_name,
        j.job_title,
        EXTRACT(QUARTER FROM he.datetime) AS quarter,
        COUNT(he.id) AS hired_count
    FROM 
        hired_employees he
    JOIN 
        jobs j ON he.job_id = j.id
    JOIN 
        departments d ON he.department_id = d.id
    WHERE 
        EXTRACT(YEAR FROM he.datetime) = 2021
    GROUP BY 
        d.name, j.job_title, EXTRACT(QUARTER FROM he.datetime)
    ORDER BY 
        d.name, j.job_title, quarter;
    """)
    result = db.execute(query).fetchall()

    # Convertir el resultado en una lista de diccionarios
    data = [
        {
            "department_name": row[0],
            "job_title": row[1],
            "quarter": int(row[2]),
            "hired_count": row[3],
        }
        for row in result
    ]

    return {"Results data": data}


@app.get("/departments/above-average")
def departments_above_average(db: Session = Depends(get_db)):
    query = text("""
    WITH department_hires AS (
        SELECT 
            d.id AS department_id,
            d.name AS department_name,
            COUNT(he.id) AS hired_count
        FROM 
            hired_employees he
        JOIN 
            departments d ON he.department_id = d.id
        WHERE 
            EXTRACT(YEAR FROM he.datetime) = 2021
        GROUP BY 
            d.id, d.name
    ),
    average_hires AS (
        SELECT 
            AVG(hired_count) AS avg_hires
        FROM 
            department_hires
    )
    SELECT 
        dh.department_id,
        dh.department_name,
        dh.hired_count
    FROM 
        department_hires dh
    CROSS JOIN 
        average_hires ah
    WHERE 
        dh.hired_count > ah.avg_hires
    ORDER BY 
        dh.hired_count DESC;
    """)

    result = db.execute(query).fetchall()

    # Convertir ahora el resultado en una lista de diccionarios
    data = [
        {
            "department_id": row[0],
            "department_name": row[1],
            "hired_count": row[2],
        }
        for row in result
    ]

    return {"Results data": data}
