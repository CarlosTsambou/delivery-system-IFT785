from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_statistiques_globales():
    client.post("/colis/", json={
        "description": "Colis test",
        "adresse_destination": "123 rue Test",
        "adresse_expediteur": "456 rue Source"
    })
    reponse = client.get("/dashboard/global")
    assert reponse.status_code == 200
    data = reponse.json()
    assert "total_colis" in data
    assert "taux_confirmation" in data
    assert data["total_colis"] >= 1

def test_statistiques_par_statut():
    reponse = client.get("/dashboard/par-statut")
    assert reponse.status_code == 200
    data = reponse.json()
    assert "créé" in data
    assert "en_transit" in data
    assert "livré" in data
    assert "confirmé" in data

def test_resume_complet():
    reponse = client.get("/dashboard/resume")
    assert reponse.status_code == 200
    data = reponse.json()
    assert "global" in data
    assert "par_statut" in data

def test_statistiques_par_periode():
    reponse = client.get(
        "/dashboard/par-periode",
        params={
            "date_debut": "2020-01-01T00:00:00",
            "date_fin": "2030-01-01T00:00:00"
        }
    )
    assert reponse.status_code == 200
    data = reponse.json()
    assert "total_colis" in data
    assert "colis" in data

def test_strategie_interchangeable():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.database import Base
    from app.services.dashboard_service import (
        DashboardService, StatistiqueGlobale, StatistiqueParStatut
    )
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    service = DashboardService(db)
    service.definir_strategie(StatistiqueGlobale())
    result1 = service.executer()
    assert "total_colis" in result1
    service.definir_strategie(StatistiqueParStatut())
    result2 = service.executer()
    assert "créé" in result2
    db.close()