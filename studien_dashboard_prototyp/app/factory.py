from __future__ import annotations

from app.models import Modul, Pruefungsart, Pruefungsleistung
from app.validation import validate_date, validate_non_empty, validate_note, validate_positive_int


class DomainFactory:
    """Erzeugt Domänenobjekte aus Benutzereingaben.

    Dadurch bleibt der Controller schlank und die Validierung an einer Stelle gebündelt.
    """

    @staticmethod
    def create_modul(name: str, ects: str) -> Modul:
        return Modul(
            name=validate_non_empty(name, "Modulname"),
            ects=validate_positive_int(ects, "ECTS"),
        )

    @staticmethod
    def create_pruefungsleistung(datum: str, note: str, art: str) -> Pruefungsleistung:
        try:
            pruefungsart = Pruefungsart[art.upper()]
        except KeyError as exc:
            erlaubte_werte = ", ".join(a.name for a in Pruefungsart)
            raise ValueError(f"Ungültige Prüfungsart. Erlaubt: {erlaubte_werte}") from exc
        return Pruefungsleistung(
            datum=validate_date(datum),
            note=validate_note(note),
            art=pruefungsart,
        )
