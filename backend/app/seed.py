from sqlalchemy.orm import Session
import models, crud, schemas

def cargar_datos_iniciales(db: Session):
    if db.query(models.PuntoInteres).count() > 0:
        return
    puntos_ejemplo = [
        {"nombre": "Catedral Metropolitana", "descripcion": "Principal iglesia de la ciudad", "latitud": -34.6037, "longitud": -58.3816, "categoria": "cultural"},
        {"nombre": "Parque Lezama", "descripcion": "Parque histórico con museos", "latitud": -34.6266, "longitud": -58.3700, "categoria": "natural"},
        {"nombre": "Estación de Servicio ACA", "descripcion": "Combustibles y servicios", "latitud": -34.5911, "longitud": -58.3926, "categoria": "servicio"},
        {"nombre": "Teatro Colón", "descripcion": "Famoso teatro lírico", "latitud": -34.5997, "longitud": -58.3836, "categoria": "cultural"},
        {"nombre": "Restaurante Puerto Madero", "descripcion": "Comida gourmet junto al río", "latitud": -34.6105, "longitud": -58.3657, "categoria": "gastronomico"}
    ]
    for p in puntos_ejemplo:
        punto = schemas.PuntoCreate(**p)
        crud.crear_punto(db, punto)
