import argparse
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from dunamai import Style, Version
from tomlkit import dump as toml_dump
from tomlkit import parse as toml_parse

__VERSION__ = "0.3.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _bump_version(current_version: Version, bump_element: Literal["major", "minor", "patch", "prerelease"]) -> str:
    if bump_element == "prerelease":
        return current_version.serialize(style=Style.SemVer, format="{base}-post.{distance}")

    bump_index = ["major", "minor", "patch"].index(bump_element)
    return current_version.bump(index=bump_index).serialize(style=Style.SemVer, format="{base}")


def _bump_pyproject_version(bumped_version: str) -> None:
    path = PROJECT_ROOT / "pyproject.toml"

    with path.open(mode="r") as f:
        data = toml_parse(f.read())

    data["project"]["version"] = bumped_version

    with path.open(mode="w") as f:
        toml_dump(data, f)


def _bump_change_log_version(bumped_version: str) -> None:
    path = PROJECT_ROOT / "CHANGELOG.md"

    with path.open(mode="r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("## [Unreleased]"):
            lines[i] = f"## [Unreleased]\n\n## [{bumped_version}] - {datetime.now(tz=UTC).date().isoformat()}\n"

    with path.open(mode="w") as f:
        f.writelines(lines)


def _run_uv_lock() -> None:
    try:
        subprocess.run(["uv", "lock"], check=True, capture_output=True, text=True)  # noqa: S607
    except subprocess.CalledProcessError as e:
        print(f"Error running 'uv lock': {e.stderr}")
        raise


def main() -> None:
    """Script entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("version_element", choices=["major", "minor", "patch", "prerelease"])
    args = parser.parse_args()

    current_version = Version.from_git()
    bumped_version = _bump_version(current_version=current_version, bump_element=args.version_element)
    current_version_fmt = current_version.serialize(style=Style.SemVer, format="{base}")
    print(f"Bumping version: {current_version_fmt} -> {bumped_version}")

    _bump_pyproject_version(bumped_version)
    print("- updated pyproject.toml")
    _run_uv_lock()
    print("- updated lock file")
    if args.version_element != "prerelease":
        _bump_change_log_version(bumped_version)
        print("- updated CHANGELOG.md")


if __name__ == "__main__":
    main()
