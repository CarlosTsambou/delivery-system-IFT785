from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.colis_repository import ColisRepository
from app.schemas import ColisCreer, ColisReponse, ColisChangerStatut
from app.services.colis_service import ColisService

router = APIRouter(prefix="/colis", tags=["Colis"])

@router.post("/", response_model=ColisReponse, status_code=201)
def creer_colis(colis: ColisCreer, db: Session = Depends(get_db)):
    repo = ColisRepository(db)
    return repo.creer(
        description=colis.description,
        adresse_destination=colis.adresse_destination,
        adresse_expediteur=colis.adresse_expediteur
    )

@router.get("/", response_model=list[ColisReponse])
def obtenir_tous_les_colis(db: Session = Depends(get_db)):
    repo = ColisRepository(db)
    return repo.obtenir_tous()

@router.get("/{colis_id}", response_model=ColisReponse)
def obtenir_colis(colis_id: str, db: Session = Depends(get_db)):
    repo = ColisRepository(db)
    colis = repo.obtenir_par_id(colis_id)
    if colis is None:
        raise HTTPException(status_code=404, detail="Colis non trouvé")
    return colis

@router.patch("/{colis_id}/statut", response_model=ColisReponse)
def changer_statut(colis_id: str, data: ColisChangerStatut, db: Session = Depends(get_db)):
    repo = ColisRepository(db)
    colis = repo.obtenir_par_id(colis_id)
    if colis is None:
        raise HTTPException(status_code=404, detail="Colis non trouvé")
    if not ColisService.transition_valide(colis.statut, data.nouveau_statut):
        raise HTTPException(
            status_code=400,
            detail=ColisService.message_erreur_transition(colis.statut, data.nouveau_statut)
        )
    return repo.changer_statut(colis_id, data.nouveau_statut)

@router.delete("/{colis_id}", status_code=204)
def supprimer_colis(colis_id: str, db: Session = Depends(get_db)):
    repo = ColisRepository(db)
    succes = repo.supprimer(colis_id)
    if not succes:
        raise HTTPException(status_code=404, detail="Colis non trouvé")