from dataclasses import dataclass, field
from typing import List


@dataclass
class PruefungEintragViewModel:
    datum: str
    modul: str


@dataclass
class ModulStatusViewModel:
    semester: int
    modul: str
    status: str
    note: str


@dataclass
class DashboardViewModel:
    studiengang_name: str
    fortschritt_prozent: float
    ects_belegt: int
    ects_gesamt: int
    aktueller_schnitt: str
    beste_note: str
    schlechteste_note: str
    regelstudienzeit_semester: int
    verbleibende_semester: int
    pruefungen: List[PruefungEintragViewModel] = field(default_factory=list)
    modulstatus: List[ModulStatusViewModel] = field(default_factory=list)
    noten_pro_semester: List[tuple[int, float]] = field(default_factory=list)
