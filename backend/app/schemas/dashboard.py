from datetime import date
from typing import List

from pydantic import BaseModel


class MonatsZahl(BaseModel):
    monat: date
    anzahl: int


class GemeindeZahl(BaseModel):
    gemeinde: str
    anzahl: int


class DashboardStats(BaseModel):
    anzahl_user: int
    anzahl_gemeinden: int
    anzahl_magistratsvorlagen: int
    anzahl_mobilitaetschecks: int
    anzahl_klimarelevanzpruefungen: int
    magistratsvorlagen_veroeffentlicht: int
    neue_user_pro_monat: List[MonatsZahl]
    neue_magistratsvorlagen_pro_monat: List[MonatsZahl]
    neue_mobilitaetschecks_pro_monat: List[MonatsZahl]
    neue_klimarelevanzpruefungen_pro_monat: List[MonatsZahl]
    magistratsvorlagen_pro_gemeinde: List[GemeindeZahl]
