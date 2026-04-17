from sqlalchemy import Column, Integer, String, Text, Float
from geoalchemy2 import Geometry
from database import Base

class PuntoInteres(Base):
    __tablename__ = "puntos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    categoria = Column(String(50), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    ubicacion = Column(Geometry('POINT', srid=4326))
