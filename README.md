# Studien-Dashboard-Prototyp

Ein lauffähiger CLI-Prototyp für ein Studien-Dashboard in Python.

## Funktionen
- Module anlegen
- Prüfungsleistungen erfassen
- Dashboard mit Kennzahlen anzeigen
- Daten in JSON speichern und wieder laden
- Beispieldaten laden

## Architektur
- `app/models.py`: Domänenmodell
- `app/services.py`: Anwendungs- und Dashboard-Logik
- `app/cli_view.py`: Ein- und Ausgabe
- `app/controller.py`: Steuerung des Ablaufs
- `app/repository.py`: JSON-Persistenz
- `app/factory.py`: Objekterzeugung und Validierung

## Start
Siehe `INSTALLATION.txt`.
