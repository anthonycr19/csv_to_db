import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_hired_employees_by_quarter():
    """Test para obtener el número de empleados contratados por trimestre."""
    response = client.get("/hired_employees_by_quarter?year=2021")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("department" in item and "job_title" in item for item in data)


def test_get_departments_hiring_above_average():
    """Test para obtener departamentos que contrataron más empleados que la media."""
    response = client.get("/departments_above_average")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("id" in item and "name" in item and "hired_count" in item for item in data)
