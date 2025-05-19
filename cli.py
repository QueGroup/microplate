import json
import tempfile

import typer
from cookiecutter.main import cookiecutter

app = typer.Typer()


@app.command()
def create(
    template: str = typer.Option(
        ".", help="Путь к шаблону: локальный путь или ссылка на GitHub"
    )
):
    typer.echo("🚀 Backend Template Generator")

    project_name = typer.prompt("Project title")
    description = typer.prompt(
        "Project description", default="My awesome FastAPI project"
    )
    version = typer.prompt("Version", default="0.1.0")
    modules_input = typer.prompt(
        "Your subject area"
    )
    author = typer.prompt("Author (First name and last name)")
    modules = [m.strip() for m in modules_input.split(",") if m.strip()]

    project_slug = project_name.lower().replace(" ", "_")

    include_sync_api = typer.confirm("Include sync API?", default=True)
    include_async_api = typer.confirm("Include async API?", default=False)

    context = {
        "project_name": project_name,
        "description": description,
        "project_slug": project_slug,
        "version": version,
        "modules": modules,
        "author": author,
        "include_sync_api": "yes" if include_sync_api else "no",
        "include_async_api": "yes" if include_async_api else "no",
    }

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump(context, f)
        f.flush()

        cookiecutter(
            template=template,
            extra_context=context,
            no_input=True,
        )

    typer.echo(f"\n✅ Project '{project_name}' has been successfully created!")


if __name__ == "__main__":
    app()
