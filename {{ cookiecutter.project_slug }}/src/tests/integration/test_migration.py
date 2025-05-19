import pytest
from alembic.command import downgrade, upgrade
from alembic.script import Script, ScriptDirectory


def get_revisions(alembic_config) -> list[Script]:
    revisions_dir = ScriptDirectory(alembic_config.get_main_option("script_location"))

    revisions: list[Script] = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.fixture(scope="module", autouse=True)
def _drop_db(alembic_config) -> None:
    downgrade(alembic_config, "base")


@pytest.mark.order("first")
def test_migrations_stairway(alembic_config) -> None:
    for revision in get_revisions(alembic_config):
        upgrade(alembic_config, revision.revision)
        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)
