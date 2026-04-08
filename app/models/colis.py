from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.sqlite import INTEGER
from app.database import Base
from datetime import datetime, timezone
import enum
import uuid

class StatutColis(enum.Enum):
    CREE = "créé"
    EN_TRANSIT = "en_transit"
    LIVRE = "livré"
    CONFIRME = "confirmé"

class Colis(Base):
    __tablename__ = "colis"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String, nullable=False)
    adresse_destination = Column(String, nullable=False)
    adresse_expediteur = Column(String, nullable=False)
    statut = Column(Enum(StatutColis), default=StatutColis.CREE, nullable=False)
    date_creation = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    date_modification = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Colis {self.id} - {self.statut}>"