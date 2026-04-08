import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Base de données séparée pour les tests
DATABASE_TEST_URL = "sqlite:///./test.db"

engine_test = create_engine(
    DATABASE_TEST_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

client = TestClient(app)

def test_creer_colis():
    reponse = client.post("/colis/", json={
        "description": "Téléphone",
        "adresse_destination": "123 rue Principale, Montréal",
        "adresse_expediteur": "456 rue du Commerce, Québec"
    })
    assert reponse.status_code == 201
    data = reponse.json()
    assert data["description"] == "Téléphone"
    assert data["statut"] == "créé"
    assert "id" in data

def test_obtenir_colis_par_id():
    reponse = client.post("/colis/", json={
        "description": "Livre",
        "adresse_destination": "789 avenue des Arts, Montréal",
        "adresse_expediteur": "101 rue du Port, Québec"
    })
    colis_id = reponse.json()["id"]
    reponse = client.get(f"/colis/{colis_id}")
    assert reponse.status_code == 200
    assert reponse.json()["id"] == colis_id

def test_colis_non_trouve():
    reponse = client.get("/colis/id-qui-nexiste-pas")
    assert reponse.status_code == 404

def test_changer_statut():
    reponse = client.post("/colis/", json={
        "description": "Tablette",
        "adresse_destination": "222 rue Sherbrooke, Montréal",
        "adresse_expediteur": "333 rue King, Sherbrooke"
    })
    colis_id = reponse.json()["id"]
    reponse = client.patch(f"/colis/{colis_id}/statut", json={
        "nouveau_statut": "en_transit"
    })
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "en_transit"

def test_supprimer_colis():
    reponse = client.post("/colis/", json={
        "description": "Casque audio",
        "adresse_destination": "555 boulevard Laurier, Québec",
        "adresse_expediteur": "666 rue Sainte-Catherine, Montréal"
    })
    colis_id = reponse.json()["id"]
    reponse = client.delete(f"/colis/{colis_id}")
    assert reponse.status_code == 204
    reponse = client.get(f"/colis/{colis_id}")
    assert reponse.status_code == 404