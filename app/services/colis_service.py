from app.models.colis import StatutColis

TRANSITIONS_VALIDES = {
    StatutColis.CREE: [StatutColis.EN_TRANSIT],
    StatutColis.EN_TRANSIT: [StatutColis.LIVRE],
    StatutColis.LIVRE: [StatutColis.CONFIRME],
    StatutColis.CONFIRME: []
}

class ColisService:
    @staticmethod
    def transition_valide(statut_actuel: StatutColis, nouveau_statut: StatutColis) -> bool:
        transitions = TRANSITIONS_VALIDES.get(statut_actuel, [])
        return nouveau_statut in transitions

    @staticmethod
    def obtenir_transitions_possibles(statut_actuel: StatutColis) -> list[StatutColis]:
        return TRANSITIONS_VALIDES.get(statut_actuel, [])

    @staticmethod
    def message_erreur_transition(statut_actuel: StatutColis, nouveau_statut: StatutColis) -> str:
        possibles = TRANSITIONS_VALIDES.get(statut_actuel, [])
        if not possibles:
            return f"Le colis est déjà en état final : {statut_actuel.value}"
        noms = [s.value for s in possibles]
        return f"Transition impossible : {statut_actuel.value} → {nouveau_statut.value}. Transitions valides : {noms}"