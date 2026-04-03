from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from app.models import Modul, Pruefungsart, Pruefungsleistung, Semester, Studiengang


class JsonStudySerializer:
    """Kapselt das Mapping zwischen Domänenobjekten und JSON-Struktur."""

    @staticmethod
    def to_dict(studiengang: Studiengang) -> Dict[str, Any]:
        return {
            "studiengang": {
                "name": studiengang.name,
                "regelstudienzeit_semester": studiengang.regelstudienzeit_semester,
                "ects_gesamt": studiengang.ects_gesamt,
                "semester": [
                    {
                        "nummer": semester.nummer,
                        "module": [
                            {
                                "name": modul.name,
                                "ects": modul.ects,
                                "pruefungsleistungen": [
                                    {
                                        "datum": leistung.datum,
                                        "note": leistung.note,
                                        "art": leistung.art.name,
                                    }
                                    for leistung in modul.pruefungsleistungen
                                ],
                            }
                            for modul in semester.module
                        ],
                    }
                    for semester in studiengang.semester
                ],
            }
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Studiengang:
        root = data["studiengang"]
        studiengang = Studiengang(
            name=root["name"],
            regelstudienzeit_semester=root["regelstudienzeit_semester"],
            ects_gesamt=root["ects_gesamt"],
        )
        for semester_data in root.get("semester", []):
            semester = Semester(nummer=semester_data["nummer"])
            for modul_data in semester_data.get("module", []):
                modul = Modul(name=modul_data["name"], ects=modul_data["ects"])
                for leistung_data in modul_data.get("pruefungsleistungen", []):
                    modul.add_pruefungsleistung(
                        Pruefungsleistung(
                            datum=leistung_data["datum"],
                            note=leistung_data["note"],
                            art=Pruefungsart[leistung_data["art"]],
                        )
                    )
                semester.add_modul(modul)
            studiengang.add_semester(semester)
        return studiengang


class JsonRepository:
    """Speichert das Projekt an einem festen, gekapselten Speicherort."""

    def __init__(self, storage_dir: Path | None = None, filename: str = "studien_dashboard.json") -> None:
        self.storage_dir = storage_dir or Path(__file__).resolve().parent.parent / "data"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.storage_dir / filename
        self.serializer = JsonStudySerializer()

    def save(self, studiengang: Studiengang) -> Path:
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(self.serializer.to_dict(studiengang), f, indent=2, ensure_ascii=False)
        return self.filepath

    def load(self) -> Studiengang:
        if not self.filepath.exists():
            raise FileNotFoundError("Es wurde noch keine gespeicherte Datei gefunden.")
        with self.filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.serializer.from_dict(data)
