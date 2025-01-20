from sqlalchemy import Column, Integer, String, Float, ForeignKey, BigInteger, DateTime
#from .database import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, index=True)
    job_title = Column(String, index=True)

    # Relación con hired_employees
    employees = relationship("HiredEmployee", back_populates="job")


class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relación con hired_employees
    employees = relationship("HiredEmployee", back_populates="department")


class HiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    job_id = Column(BigInteger, ForeignKey("jobs.id"))
    department_id = Column(BigInteger, ForeignKey("departments.id"))

    # Relaciones
    job = relationship("Job", back_populates="employees")
    department = relationship("Department", back_populates="employees")


# Para esta siguiente variable se pondrá el usuario, contraseña, hostname, puerto y nombre de la B.D.
SQLACHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/db_csv_file'
engine = create_engine(SQLACHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
