from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

def crear_punto(db: Session, punto: schemas.PuntoCreate):
    point = Point(punto.longitud, punto.latitud)
    ubicacion_geometrica = from_shape(point, srid=4326)
    db_punto = models.PuntoInteres(
        nombre=punto.nombre,
        descripcion=punto.descripcion,
        categoria=punto.categoria,
        latitud=punto.latitud,
        longitud=punto.longitud,
        ubicacion=ubicacion_geometrica
    )
    db.add(db_punto)
    db.commit()
    db.refresh(db_punto)
    return db_punto

def listar_puntos(db: Session, categoria: str = None, lat: float = None, lng: float = None, radio_km: float = None):
    query = db.query(models.PuntoInteres)
    if categoria:
        query = query.filter(models.PuntoInteres.categoria == categoria)
    if lat is not None and lng is not None and radio_km is not None:
        radio_metros = radio_km * 1000
        query = query.filter(
            func.ST_DWithin(
                models.PuntoInteres.ubicacion,
                func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326),
                radio_metros
            )
        )
    return query.all()
