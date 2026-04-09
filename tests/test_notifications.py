from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.notifications.observer import SujetColis, ObservateurColis
from app.models.colis import Colis, StatutColis
from app.services.colis_service import ColisService

client = TestClient(app)

class ObservateurTest(ObservateurColis):
    def __init__(self):
        self.notifications = []

    def notifier(self, colis: Colis, ancien_statut: str) -> None:
        self.notifications.append({
            "colis_id": colis.id,
            "ancien_statut": ancien_statut,
            "nouveau_statut": colis.statut.value
        })

def test_observer_notifie_lors_changement_statut():
    observateur = ObservateurTest()
    sujet = SujetColis()
    sujet.abonner(observateur)
    colis_mock = MagicMock()
    colis_mock.id = "test-id-123"
    colis_mock.statut.value = "en_transit"
    sujet.notifier_tous(colis_mock, "créé")
    assert len(observateur.notifications) == 1
    assert observateur.notifications[0]["ancien_statut"] == "créé"
    assert observateur.notifications[0]["nouveau_statut"] == "en_transit"

def test_observer_desabonnement():
    observateur = ObservateurTest()
    sujet = SujetColis()
    sujet.abonner(observateur)
    sujet.desabonner(observateur)
    colis_mock = MagicMock()
    colis_mock.statut.value = "en_transit"
    sujet.notifier_tous(colis_mock, "créé")
    assert len(observateur.notifications) == 0

def test_transition_valide():
    assert ColisService.transition_valide(StatutColis.CREE, StatutColis.EN_TRANSIT) is True
    assert ColisService.transition_valide(StatutColis.EN_TRANSIT, StatutColis.LIVRE) is True
    assert ColisService.transition_valide(StatutColis.LIVRE, StatutColis.CONFIRME) is True

def test_transition_invalide():
    assert ColisService.transition_valide(StatutColis.CREE, StatutColis.CONFIRME) is False
    assert ColisService.transition_valide(StatutColis.CONFIRME, StatutColis.CREE) is False

def test_api_refuse_transition_invalide():
    reponse = client.post("/colis/", json={
        "description": "Montre",
        "adresse_destination": "123 rue Test",
        "adresse_expediteur": "456 rue Source"
    })
    colis_id = reponse.json()["id"]
    reponse = client.patch(f"/colis/{colis_id}/statut", json={
        "nouveau_statut": "confirmé"
    })
    assert reponse.status_code == 400
    assert "Transition impossible" in reponse.json()["detail"]

def test_api_accepte_transition_valide():
    reponse = client.post("/colis/", json={
        "description": "Clavier",
        "adresse_destination": "789 avenue Test",
        "adresse_expediteur": "101 rue Source"
    })
    colis_id = reponse.json()["id"]
    reponse = client.patch(f"/colis/{colis_id}/statut", json={
        "nouveau_statut": "en_transit"
    })
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "en_transit"