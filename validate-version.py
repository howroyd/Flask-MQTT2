import subprocess
import sys

import semver


def get_version_from_pyproject() -> semver.VersionInfo:
    with open("pyproject.toml") as f:
        for line in f:
            if "version" in line:
                return semver.VersionInfo.parse(line.split("=")[1].strip().strip('"'))
    raise ValueError("Version not found in pyproject.toml")


def check_exists(version: str) -> int:
    package: str = f"flask_mqtt2=={version}"
    print(f"Checking if {package} exists")
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--dry-run",
            "--no-deps",
            "--no-build-isolation",
            "--ignore-installed",
            "--no-cache-dir",
            package,
        ],
        capture_output=True,
    ).returncode


if __name__ == "__main__":
    version = get_version_from_pyproject()
    if ret := check_exists(str(version)) != 0:
        print(f"Version {version} doesn't exist ({ret=})")
    else:
        print(f"Version {version} already exists ({ret=})")
        sys.exit(1)
