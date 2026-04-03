from app.models import Modul, Pruefungsart, Pruefungsleistung, Semester, Studiengang


def create_sample_studiengang() -> Studiengang:
    studiengang = Studiengang(
        name="Softwareentwicklung B.Sc.",
        regelstudienzeit_semester=6,
        ects_gesamt=180,
    )

    semester1 = Semester(nummer=1)
    mathe = Modul(name="Mathe 1", ects=5)
    mathe.add_pruefungsleistung(Pruefungsleistung(datum="15.02.2024", note=1.3, art=Pruefungsart.KLAUSUR))
    prog = Modul(name="Programmierung", ects=5)
    prog.add_pruefungsleistung(Pruefungsleistung(datum="20.02.2024", note=2.0, art=Pruefungsart.PROJEKT))
    semester1.add_modul(mathe)
    semester1.add_modul(prog)

    semester2 = Semester(nummer=2)
    db = Modul(name="Datenbanken", ects=5)
    db.add_pruefungsleistung(Pruefungsleistung(datum="20.04.2024", note=1.7, art=Pruefungsart.KLAUSUR))
    bwl = Modul(name="BWL", ects=5)
    semester2.add_modul(db)
    semester2.add_modul(bwl)

    studiengang.add_semester(semester1)
    studiengang.add_semester(semester2)
    return studiengang
