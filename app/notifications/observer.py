from abc import ABC, abstractmethod
from app.models.colis import Colis

class ObservateurColis(ABC):
    @abstractmethod
    def notifier(self, colis: Colis, ancien_statut: str) -> None:
        pass

class SujetColis:
    def __init__(self):
        self._observateurs: list[ObservateurColis] = []

    def abonner(self, observateur: ObservateurColis) -> None:
        self._observateurs.append(observateur)

    def desabonner(self, observateur: ObservateurColis) -> None:
        self._observateurs.remove(observateur)

    def notifier_tous(self, colis: Colis, ancien_statut: str) -> None:
        for observateur in self._observateurs:
            observateur.notifier(colis, ancien_statut)