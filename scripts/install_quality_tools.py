#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import stat
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def platform_key() -> str:
    systems = {"darwin": "darwin", "linux": "linux"}
    machines = {"aarch64": "arm64", "arm64": "arm64", "amd64": "x64", "x86_64": "x64"}
    system = systems.get(platform.system().lower())
    machine = machines.get(platform.machine().lower())
    if not system or not machine:
        raise SystemExit(
            f"unsupported quality tools platform: {platform.system()} {platform.machine()}"
        )
    return f"{system}-{machine}"


def download(url: str, digest: str, destination: Path) -> None:
    with (
        urllib.request.urlopen(url, timeout=60) as response,
        destination.open("wb") as stream,
    ):
        shutil.copyfileobj(response, stream)
    actual = hashlib.sha256(destination.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f"download checksum mismatch for {url}: {actual}")


def install_actionlint(config: dict[str, object], key: str, bin_dir: Path) -> None:
    version = str(config["version"])
    platform_name = key.replace("x64", "amd64").replace("-", "_")
    filename = f"actionlint_{version}_{platform_name}.tar.gz"
    url = f"https://github.com/rhysd/actionlint/releases/download/v{version}/{filename}"
    digest = str(config["platforms"][key])
    with tempfile.TemporaryDirectory(prefix="foundation-actionlint-") as name:
        archive = Path(name) / filename
        download(url, digest, archive)
        with tarfile.open(archive, "r:gz") as stream:
            member = next(
                (
                    item
                    for item in stream.getmembers()
                    if Path(item.name).name == "actionlint"
                ),
                None,
            )
            if (
                member is None
                or not member.isfile()
                or Path(member.name).is_absolute()
                or ".." in Path(member.name).parts
            ):
                raise SystemExit("actionlint archive has no safe executable")
            source = stream.extractfile(member)
            if source is None:
                raise SystemExit("actionlint executable could not be extracted")
            destination = bin_dir / "actionlint"
            with destination.open("wb") as output:
                shutil.copyfileobj(source, output)
            destination.chmod(destination.stat().st_mode | stat.S_IXUSR)


def install_hadolint(config: dict[str, object], key: str, bin_dir: Path) -> None:
    version = str(config["version"])
    system, machine = key.split("-", maxsplit=1)
    system_name = "macos" if system == "darwin" else system
    machine_name = "x86_64" if machine == "x64" else machine
    filename = f"hadolint-{system_name}-{machine_name}"
    url = (
        f"https://github.com/hadolint/hadolint/releases/download/v{version}/{filename}"
    )
    destination = bin_dir / "hadolint"
    download(url, str(config["platforms"][key]), destination)
    destination.chmod(destination.stat().st_mode | stat.S_IXUSR)


def install_shellcheck(config: dict[str, object], key: str, bin_dir: Path) -> None:
    version = str(config["version"])
    platforms = {
        "darwin-arm64": "darwin.aarch64",
        "darwin-x64": "darwin.x86_64",
        "linux-arm64": "linux.aarch64",
        "linux-x64": "linux.x86_64",
    }
    filename = f"shellcheck-v{version}.{platforms[key]}.tar.gz"
    url = f"https://github.com/koalaman/shellcheck/releases/download/v{version}/{filename}"
    with tempfile.TemporaryDirectory(prefix="foundation-shellcheck-") as name:
        archive = Path(name) / filename
        download(url, str(config["platforms"][key]), archive)
        with tarfile.open(archive, "r:gz") as stream:
            member = next(
                (
                    item
                    for item in stream.getmembers()
                    if Path(item.name).name == "shellcheck"
                ),
                None,
            )
            if (
                member is None
                or not member.isfile()
                or Path(member.name).is_absolute()
                or ".." in Path(member.name).parts
            ):
                raise SystemExit("shellcheck archive has no executable")
            source = stream.extractfile(member)
            if source is None:
                raise SystemExit("shellcheck executable could not be extracted")
            destination = bin_dir / "shellcheck"
            with destination.open("wb") as output:
                shutil.copyfileobj(source, output)
            destination.chmod(destination.stat().st_mode | stat.S_IXUSR)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install pinned foundation quality tools."
    )
    parser.add_argument("--venv", type=Path, required=True)
    parser.add_argument("--tools-dir", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads((ROOT / "quality/tools.json").read_text(encoding="utf-8"))
    args.tools_dir.mkdir(parents=True, exist_ok=True)
    bin_dir = args.tools_dir / "bin"
    bin_dir.mkdir(exist_ok=True)
    if not (args.venv / "bin/python").is_file():
        subprocess.run(["python3", "-m", "venv", str(args.venv)], check=True)
    subprocess.run(
        [
            str(args.venv / "bin/pip"),
            "install",
            "--disable-pip-version-check",
            "-r",
            str(ROOT / "requirements/quality.txt"),
        ],
        check=True,
    )
    key = platform_key()
    install_actionlint(config["actionlint"], key, bin_dir)
    install_hadolint(config["hadolint"], key, bin_dir)
    install_shellcheck(config["shellcheck"], key, bin_dir)
    npm = shutil.which("npm")
    if npm is None:
        raise SystemExit("npm is required to install markdownlint-cli2")
    npm_dir = args.tools_dir / "npm"
    npm_dir.mkdir(parents=True, exist_ok=True)
    for filename in ("package.json", "package-lock.json"):
        shutil.copy2(ROOT / "quality/npm" / filename, npm_dir / filename)
    subprocess.run(
        [
            npm,
            "ci",
            "--ignore-scripts",
            "--no-audit",
            "--no-fund",
            "--prefix",
            str(npm_dir),
        ],
        env={**os.environ, "npm_config_update_notifier": "false"},
        check=True,
    )
    print(args.venv / "bin")
    print(bin_dir)
    print(npm_dir / "node_modules/.bin")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
