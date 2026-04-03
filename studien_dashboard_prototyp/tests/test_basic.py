from app.models import Modul, Pruefungsart, Pruefungsleistung


def test_modul_bestanden() -> None:
    modul = Modul(name="Mathe", ects=5)
    modul.add_pruefungsleistung(Pruefungsleistung(datum="01.02.2024", note=2.0, art=Pruefungsart.KLAUSUR))
    assert modul.bestanden is True
    assert modul.aktuelle_note() == 2.0
