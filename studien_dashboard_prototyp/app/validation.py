from __future__ import annotations

from datetime import datetime


def validate_non_empty(value: str, feldname: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{feldname} darf nicht leer sein.")
    return value


def validate_note(value: str) -> float:
    try:
        note = float(value.replace(",", "."))
    except ValueError as exc:
        raise ValueError("Ungültige Note.") from exc
    if not (1.0 <= note <= 5.0):
        raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")
    return round(note, 1)



def validate_positive_int(value: str, feldname: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{feldname} muss eine ganze Zahl sein.") from exc
    if number <= 0:
        raise ValueError(f"{feldname} muss größer als 0 sein.")
    return number



def validate_date(value: str) -> str:
    value = value.strip()
    try:
        datetime.strptime(value, "%d.%m.%Y")
    except ValueError as exc:
        raise ValueError("Datum muss im Format TT.MM.JJJJ angegeben werden.") from exc
    return value
