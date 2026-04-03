from app.cli_view import CLIView
from app.controller import CLIController
from app.models import Studiengang
from app.repository import JsonRepository


def create_empty_project() -> Studiengang:
    return Studiengang(
        name="Mein Studien-Dashboard",
        regelstudienzeit_semester=6,
        ects_gesamt=180,
    )


if __name__ == "__main__":
    view = CLIView()
    repository = JsonRepository()
    controller = CLIController(view=view, repository=repository, studiengang=create_empty_project())
    controller.run()
