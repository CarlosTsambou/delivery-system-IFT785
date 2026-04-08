from sqlalchemy.orm import Session
from app.models.colis import Colis, StatutColis
from datetime import datetime, timezone

class ColisRepository:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, description: str, adresse_destination: str, adresse_expediteur: str) -> Colis:
        colis = Colis(
            description=description,
            adresse_destination=adresse_destination,
            adresse_expediteur=adresse_expediteur
        )
        self.db.add(colis)
        self.db.commit()
        self.db.refresh(colis)
        return colis

    def obtenir_par_id(self, colis_id: str) -> Colis | None:
        return self.db.query(Colis).filter(Colis.id == colis_id).first()

    def obtenir_tous(self) -> list[Colis]:
        return self.db.query(Colis).all()

    def changer_statut(self, colis_id: str, nouveau_statut: StatutColis) -> Colis | None:
        colis = self.obtenir_par_id(colis_id)
        if colis is None:
            return None
        colis.statut = nouveau_statut
        colis.date_modification = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(colis)
        return colis

    def supprimer(self, colis_id: str) -> bool:
        colis = self.obtenir_par_id(colis_id)
        if colis is None:
            return False
        self.db.delete(colis)
        self.db.commit()
        return True