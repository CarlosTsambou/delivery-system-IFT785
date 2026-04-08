from fastapi import FastAPI
from app.database import engine, Base
from app.routers import colis

app = FastAPI(
    title="Système de gestion de livraison de colis",
    description="API de suivi et d'optimisation des livraisons",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(colis.router)

@app.get("/")
def root():
    return {"message": "Bienvenue dans le système de livraison de colis"}

@app.get("/health")
def health_check():
    return {"status": "ok"}