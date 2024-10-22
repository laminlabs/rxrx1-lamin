import nox
from laminci import upload_docs_artifact
from laminci.nox import (
    SYSTEM,
    build_docs,
    install_lamindb,
    login_testuser1,
    run,
    run_pre_commit,
)

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def build(session):
    install_lamindb(session, branch="release", extras="bionty,aws,gcp,jupyter")
    run(
        session,
        f"uv pip install {SYSTEM} wetlab findrefs vitessce starlette s3fs>=2024.10.0",
    )
    run(session, f"uv pip install {SYSTEM} .[dev]")
    login_testuser1(session)
    run(session, "pytest -s tests")
    build_docs(session, strict=True)
    upload_docs_artifact(aws=True)
