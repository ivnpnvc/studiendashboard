from __future__ import annotations

from typing import Iterable

from app.models import Pruefungsart
from app.viewmodels import DashboardViewModel


class CLIView:
    def show_title(self) -> None:
        print("\n" + "=" * 70)
        print("STUDIEN-DASHBOARD-PROTOTYP")
        print("=" * 70)

    def show_menu(self) -> None:
        print("\nBitte eine Option wählen:")
        print("1 - Modul hinzufügen")
        print("2 - Prüfungsleistung erfassen")
        print("3 - Dashboard anzeigen")
        print("4 - Daten speichern")
        print("5 - Daten laden")
        print("6 - Beispieldaten laden")
        print("0 - Beenden")

    def ask(self, prompt: str) -> str:
        return input(prompt).strip()

    def show_message(self, message: str) -> None:
        print(message)

    def show_error(self, message: str) -> None:
        print(f"Fehler: {message}")

    def show_pruefungsarten(self) -> None:
        print("Erlaubte Prüfungsarten:")
        print(", ".join(art.name for art in Pruefungsart))

    def render_dashboard(self, dashboard: DashboardViewModel) -> None:
        print("\n" + "-" * 70)
        print(f"Dashboard für: {dashboard.studiengang_name}")
        print("-" * 70)
        print(f"Fortschritt: {dashboard.fortschritt_prozent}% ({dashboard.ects_belegt}/{dashboard.ects_gesamt} ECTS)")
        print(f"Regelstudienzeit: {dashboard.regelstudienzeit_semester} Semester | Verbleibend: {dashboard.verbleibende_semester}")
        print(f"Aktueller Schnitt: {dashboard.aktueller_schnitt}")
        print(f"Beste Note: {dashboard.beste_note} | Schlechteste Note: {dashboard.schlechteste_note}")

        print("\nNotenentwicklung je Semester:")
        if not dashboard.noten_pro_semester:
            print("  Noch keine Noten vorhanden.")
        else:
            for semester, note in dashboard.noten_pro_semester:
                balken = "#" * max(1, int((6 - note) * 4))
                print(f"  Semester {semester}: {note:.2f} {balken}")

        print("\nPrüfungsübersicht:")
        if not dashboard.pruefungen:
            print("  Keine Prüfungsleistungen erfasst.")
        else:
            for eintrag in dashboard.pruefungen:
                print(f"  - {eintrag.datum}: {eintrag.modul}")

        print("\nModulstatus:")
        if not dashboard.modulstatus:
            print("  Keine Module vorhanden.")
        else:
            for status in dashboard.modulstatus:
                print(f"  Semester {status.semester}: {status.modul} | {status.status} | Note: {status.note}")
