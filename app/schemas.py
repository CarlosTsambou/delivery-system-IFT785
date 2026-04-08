from pydantic import BaseModel
from app.models.colis import StatutColis
from datetime import datetime

model_config = {"from_attributes": True}

class ColisCreer(BaseModel):
    description: str
    adresse_destination: str
    adresse_expediteur: str

class ColisReponse(BaseModel):
    id: str
    description: str
    adresse_destination: str
    adresse_expediteur: str
    statut: StatutColis
    date_creation: datetime
    date_modification: datetime

class ColisChangerStatut(BaseModel):
    nouveau_statut: StatutColis