from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import crud, schemas, models, database, seed

app = FastAPI(title="API de Puntos de Interés", description="Sistema geoespacial", version="1.0")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=database.engine)
    db = next(get_db())
    seed.cargar_datos_iniciales(db)

@app.post("/api/puntos", response_model=schemas.PuntoResponse, status_code=201)
def crear_punto(punto: schemas.PuntoCreate, db: Session = Depends(get_db)):
    return crud.crear_punto(db, punto)

@app.get("/api/puntos", response_model=list[schemas.PuntoResponse])
def listar_puntos(
    categoria: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    radio_km: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    if (lat is None) != (lng is None):
        raise HTTPException(status_code=400, detail="Debe proporcionar latitud y longitud juntas")
    if radio_km is not None and (lat is None or lng is None):
        raise HTTPException(status_code=400, detail="Para filtrar por radio necesita latitud y longitud")
    puntos = crud.listar_puntos(db, categoria, lat, lng, radio_km)
    return puntos
