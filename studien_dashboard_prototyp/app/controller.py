from __future__ import annotations

from app.cli_view import CLIView
from app.factory import DomainFactory
from app.models import Studiengang
from app.repository import JsonRepository
from app.sample_data import create_sample_studiengang
from app.services import ApplicationService, DashboardService
from app.validation import validate_positive_int, validate_non_empty


class CLIController:
    def __init__(self, view: CLIView, repository: JsonRepository, studiengang: Studiengang) -> None:
        self.view = view
        self.repository = repository
        self.studiengang = studiengang
        self.app_service = ApplicationService(studiengang)
        self.dashboard_service = DashboardService()

    def _set_studiengang(self, studiengang: Studiengang) -> None:
        self.studiengang = studiengang
        self.app_service = ApplicationService(studiengang)

    def run(self) -> None:
        self.view.show_title()
        while True:
            self.view.show_menu()
            choice = self.view.ask("Auswahl: ")
            try:
                if choice == "1":
                    self.add_modul_flow()
                elif choice == "2":
                    self.add_pruefungsleistung_flow()
                elif choice == "3":
                    self.show_dashboard_flow()
                elif choice == "4":
                    self.save_flow()
                elif choice == "5":
                    self.load_flow()
                elif choice == "6":
                    self.load_sample_data_flow()
                elif choice == "0":
                    self.view.show_message("Programm beendet.")
                    break
                else:
                    self.view.show_error("Ungültige Auswahl.")
            except Exception as exc:  # bewusst breit im CLI, damit das Programm nicht abbricht
                self.view.show_error(str(exc))

    def add_modul_flow(self) -> None:
        semester_nummer = validate_positive_int(self.view.ask("Semester-Nummer: "), "Semester-Nummer")
        modulname = self.view.ask("Modulname: ")
        ects = self.view.ask("ECTS: ")
        modul = DomainFactory.create_modul(modulname, ects)
        self.app_service.modul_anlegen(semester_nummer, modul)
        self.view.show_message(f"Modul '{modul.name}' wurde angelegt.")

    def add_pruefungsleistung_flow(self) -> None:
        semester_nummer = validate_positive_int(self.view.ask("Semester-Nummer: "), "Semester-Nummer")
        modulname = validate_non_empty(self.view.ask("Modulname: "), "Modulname")
        datum = self.view.ask("Datum (TT.MM.JJJJ): ")
        note = self.view.ask("Note (1.0 - 5.0): ")
        self.view.show_pruefungsarten()
        art = self.view.ask("Prüfungsart (z. B. KLAUSUR): ")
        leistung = DomainFactory.create_pruefungsleistung(datum, note, art)
        self.app_service.pruefungsleistung_hinzufuegen(semester_nummer, modulname, leistung)
        self.view.show_message("Prüfungsleistung wurde gespeichert.")

    def show_dashboard_flow(self) -> None:
        dashboard = self.dashboard_service.build_dashboard(self.studiengang)
        self.view.render_dashboard(dashboard)

    def save_flow(self) -> None:
        path = self.repository.save(self.studiengang)
        self.view.show_message(f"Daten wurden gespeichert: {path}")

    def load_flow(self) -> None:
        studiengang = self.repository.load()
        self._set_studiengang(studiengang)
        self.view.show_message("Daten wurden erfolgreich geladen.")

    def load_sample_data_flow(self) -> None:
        self._set_studiengang(create_sample_studiengang())
        self.view.show_message("Beispieldaten wurden geladen.")
