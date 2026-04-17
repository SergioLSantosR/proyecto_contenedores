from pydantic import BaseModel
from typing import Optional

class PuntoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    latitud: float
    longitud: float
    categoria: str

class PuntoCreate(PuntoBase):
    pass

class PuntoResponse(PuntoBase):
    id: int

    class Config:
        from_attributes = True
