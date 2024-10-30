import nox
import os

nox.options.sessions = ["lint"]

# Define the minimal nox version required to run
nox.options.needs_version = ">= 2024.3.2"


@nox.session
def lint(session):
    session.install("flake8")
    session.run(
        "flake8", "--exclude", ".nox,*.egg,build,data",
        "--select", "E,W,F", "."
    )


@nox.session
def build_and_check_dists(session):
    session.install("build", "check-manifest >= 0.42", "twine")
    # If your project uses README.rst, uncomment the following:
    # session.install("readme_renderer")

    session.run("check-manifest", "--ignore", "noxfile.py,tests/**")
    session.run("python", "-m", "build")
    session.run("python", "-m", "twine", "check", "dist/*")


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def tests(session):
    session.install("pytest")
    build_and_check_dists(session)

    generated_files = os.listdir("dist/")
    generated_sdist = os.path.join("dist/", generated_files[1])

    session.install(generated_sdist)

    session.run("py.test", "tests/", *session.posargs)
