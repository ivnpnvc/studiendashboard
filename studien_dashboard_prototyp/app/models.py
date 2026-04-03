from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Pruefungsart(str, Enum):
    KLAUSUR = "Klausur"
    MUENDLICH = "Mündlich"
    HAUSARBEIT = "Hausarbeit"
    PROJEKT = "Projekt"
    PRAKTIKUM = "Praktikum"
    SONSTIGES = "Sonstiges"


@dataclass
class Pruefungsleistung:
    datum: str
    note: float
    art: Pruefungsart

    def __post_init__(self) -> None:
        if not (1.0 <= self.note <= 5.0):
            raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")
        # einfache 0.3-Notenschritte erlauben, aber nicht erzwingen
        if not self.datum or not isinstance(self.datum, str):
            raise ValueError("Das Datum darf nicht leer sein.")


@dataclass
class Modul:
    name: str
    ects: int
    pruefungsleistungen: List[Pruefungsleistung] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Der Modulname darf nicht leer sein.")
        if self.ects <= 0:
            raise ValueError("ECTS müssen größer als 0 sein.")

    def add_pruefungsleistung(self, leistung: Pruefungsleistung) -> None:
        self.pruefungsleistungen.append(leistung)

    def aktuelle_note(self) -> Optional[float]:
        """Für den Prototypen zählt die beste vorhandene Note."""
        if not self.pruefungsleistungen:
            return None
        return min(l.note for l in self.pruefungsleistungen)

    @property
    def bestanden(self) -> bool:
        note = self.aktuelle_note()
        return note is not None and note <= 4.0

    @property
    def status_text(self) -> str:
        if not self.pruefungsleistungen:
            return "offen"
        return "bestanden" if self.bestanden else "nicht bestanden"


@dataclass
class Semester:
    nummer: int
    module: List[Modul] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.nummer <= 0:
            raise ValueError("Semester-Nummer muss größer als 0 sein.")

    def add_modul(self, modul: Modul) -> None:
        self.module.append(modul)

    def finde_modul(self, modulname: str) -> Optional[Modul]:
        for modul in self.module:
            if modul.name.lower() == modulname.lower():
                return modul
        return None


@dataclass
class Studiengang:
    name: str
    regelstudienzeit_semester: int
    ects_gesamt: int
    semester: List[Semester] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Der Studiengangname darf nicht leer sein.")
        if self.regelstudienzeit_semester <= 0:
            raise ValueError("Regelstudienzeit muss größer als 0 sein.")
        if self.ects_gesamt <= 0:
            raise ValueError("ECTS gesamt muss größer als 0 sein.")

    def add_semester(self, semester: Semester) -> None:
        if self.finde_semester(semester.nummer) is not None:
            raise ValueError(f"Semester {semester.nummer} existiert bereits.")
        self.semester.append(semester)
        self.semester.sort(key=lambda s: s.nummer)

    def finde_semester(self, nummer: int) -> Optional[Semester]:
        for semester in self.semester:
            if semester.nummer == nummer:
                return semester
        return None

    def finde_oder_erzeuge_semester(self, nummer: int) -> Semester:
        semester = self.finde_semester(nummer)
        if semester is None:
            semester = Semester(nummer=nummer)
            self.add_semester(semester)
        return semester
