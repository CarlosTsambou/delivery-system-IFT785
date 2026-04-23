from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dashboard_service import (
    DashboardService,
    StatistiqueParStatut,
    StatistiqueGlobale,
    StatistiqueParPeriode
)
from datetime import datetime, timezone

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/global")
def statistiques_globales(db: Session = Depends(get_db)):
    service = DashboardService(db)
    service.definir_strategie(StatistiqueGlobale())
    return service.executer()

@router.get("/par-statut")
def statistiques_par_statut(db: Session = Depends(get_db)):
    service = DashboardService(db)
    service.definir_strategie(StatistiqueParStatut())
    return service.executer()

@router.get("/par-periode")
def statistiques_par_periode(
    date_debut: datetime = Query(default=None),
    date_fin: datetime = Query(default=None),
    db: Session = Depends(get_db)
):
    if date_debut is None:
        date_debut = datetime(2020, 1, 1, tzinfo=timezone.utc)
    if date_fin is None:
        date_fin = datetime.now(timezone.utc)
    service = DashboardService(db)
    service.definir_strategie(StatistiqueParPeriode(date_debut, date_fin))
    return service.executer()

@router.get("/resume")
def resume_complet(db: Session = Depends(get_db)):
    service = DashboardService(db)
    service.definir_strategie(StatistiqueGlobale())
    global_stats = service.executer()
    service.definir_strategie(StatistiqueParStatut())
    par_statut = service.executer()
    return {
        "global": global_stats,
        "par_statut": par_statut
    }