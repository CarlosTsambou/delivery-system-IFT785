from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.colis import Colis, StatutColis
from datetime import datetime, timezone

class StrategieStatistique(ABC):
    @abstractmethod
    def calculer(self, db: Session) -> dict:
        pass

class StatistiqueParStatut(StrategieStatistique):
    def calculer(self, db: Session) -> dict:
        resultats = {}
        for statut in StatutColis:
            count = db.query(Colis).filter(Colis.statut == statut).count()
            resultats[statut.value] = count
        return resultats

class StatistiqueGlobale(StrategieStatistique):
    def calculer(self, db: Session) -> dict:
        total = db.query(Colis).count()
        livres = db.query(Colis).filter(
            Colis.statut == StatutColis.CONFIRME
        ).count()
        taux = round((livres / total * 100), 2) if total > 0 else 0
        return {
            "total_colis": total,
            "total_confirmes": livres,
            "taux_confirmation": taux
        }

class StatistiqueParPeriode(StrategieStatistique):
    def __init__(self, date_debut: datetime, date_fin: datetime):
        self.date_debut = date_debut
        self.date_fin = date_fin

    def calculer(self, db: Session) -> dict:
        colis = db.query(Colis).filter(
            Colis.date_creation >= self.date_debut,
            Colis.date_creation <= self.date_fin
        ).all()
        return {
            "periode_debut": self.date_debut.isoformat(),
            "periode_fin": self.date_fin.isoformat(),
            "total_colis": len(colis),
            "colis": [{"id": c.id, "statut": c.statut.value, "description": c.description} for c in colis]
        }

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self._strategie: StrategieStatistique = StatistiqueGlobale()

    def definir_strategie(self, strategie: StrategieStatistique) -> None:
        self._strategie = strategie

    def executer(self) -> dict:
        return self._strategie.calculer(self.db)