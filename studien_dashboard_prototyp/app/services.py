from __future__ import annotations

from dataclasses import asdict
from typing import List

from app.models import Studiengang, Modul
from app.viewmodels import DashboardViewModel, ModulStatusViewModel, PruefungEintragViewModel


class DashboardService:
    """Liest nur aus dem Domänenmodell und erstellt ein ViewModel für die Darstellung."""

    @staticmethod
    def build_dashboard(studiengang: Studiengang) -> DashboardViewModel:
        alle_module = [modul for semester in studiengang.semester for modul in semester.module]
        benotete_module = [modul for modul in alle_module if modul.aktuelle_note() is not None]
        alle_noten = [modul.aktuelle_note() for modul in benotete_module if modul.aktuelle_note() is not None]
        ects_belegt = sum(modul.ects for modul in alle_module if modul.bestanden)
        fortschritt = (ects_belegt / studiengang.ects_gesamt * 100) if studiengang.ects_gesamt else 0
        aktueller_schnitt = f"{sum(alle_noten)/len(alle_noten):.2f}" if alle_noten else "-"
        beste_note = f"{min(alle_noten):.1f}" if alle_noten else "-"
        schlechteste_note = f"{max(alle_noten):.1f}" if alle_noten else "-"

        naechste_pruefungen: List[PruefungEintragViewModel] = []
        modulstatus: List[ModulStatusViewModel] = []
        noten_pro_semester: List[tuple[int, float]] = []

        for semester in studiengang.semester:
            semester_noten = []
            for modul in semester.module:
                note = modul.aktuelle_note()
                if note is not None:
                    semester_noten.append(note)
                    for leistung in modul.pruefungsleistungen:
                        naechste_pruefungen.append(PruefungEintragViewModel(datum=leistung.datum, modul=modul.name))
                modulstatus.append(
                    ModulStatusViewModel(
                        semester=semester.nummer,
                        modul=modul.name,
                        status=modul.status_text,
                        note="-" if note is None else f"{note:.1f}",
                    )
                )
            if semester_noten:
                noten_pro_semester.append((semester.nummer, round(sum(semester_noten) / len(semester_noten), 2)))

        return DashboardViewModel(
            studiengang_name=studiengang.name,
            fortschritt_prozent=round(fortschritt, 1),
            ects_belegt=ects_belegt,
            ects_gesamt=studiengang.ects_gesamt,
            aktueller_schnitt=aktueller_schnitt,
            beste_note=beste_note,
            schlechteste_note=schlechteste_note,
            regelstudienzeit_semester=studiengang.regelstudienzeit_semester,
            verbleibende_semester=max(studiengang.regelstudienzeit_semester - len(studiengang.semester), 0),
            pruefungen=sorted(naechste_pruefungen, key=lambda p: p.datum),
            modulstatus=modulstatus,
            noten_pro_semester=noten_pro_semester,
        )


class ApplicationService:
    """Koordiniert Anwendungsfälle und hält den Controller schlank."""

    def __init__(self, studiengang: Studiengang) -> None:
        self.studiengang = studiengang

    def modul_anlegen(self, semester_nummer: int, modul: Modul) -> None:
        semester = self.studiengang.finde_oder_erzeuge_semester(semester_nummer)
        if semester.finde_modul(modul.name):
            raise ValueError(f"Das Modul '{modul.name}' existiert in Semester {semester_nummer} bereits.")
        semester.add_modul(modul)

    def pruefungsleistung_hinzufuegen(self, semester_nummer: int, modulname: str, leistung) -> None:
        semester = self.studiengang.finde_semester(semester_nummer)
        if semester is None:
            raise ValueError(f"Semester {semester_nummer} wurde nicht gefunden.")
        modul = semester.finde_modul(modulname)
        if modul is None:
            raise ValueError(f"Modul '{modulname}' wurde nicht gefunden.")
        modul.add_pruefungsleistung(leistung)
