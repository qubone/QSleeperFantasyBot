#!/usr/bin/env python3
"""Bump the patch version of the project and create a git tag.
This script reads the base version from a specified file, determines the latest patch version from git tags,
increments it, and creates a new tag in the format 'vX.Y.Z'. It can also perform a dry run where it only
logs the new tag without creating it.
"""

import argparse
import logging
import re
import subprocess

from pathlib import Path

logging.basicConfig(level=logging.INFO)


def get_base_version(version_file: Path) -> str:
    """Read the base version from the specified file.
    Args:
        version_file (Path): Path to the version file.
        Returns:
        str: The base version in the format 'X.Y'.
    Raises:
        FileNotFoundError: If the version file does not exist.
        ValueError: If the version format is invalid.
    """
    if not version_file.exists():
        raise FileNotFoundError(f"Version file {version_file} does not exist.")
    base = version_file.read_text().strip()
    if not re.match(r"^\d+\.\d+$", base):
        raise ValueError(f"Invalid base version in {version_file}: {base}")
    return base


def get_latest_patch(base_version: str) -> int:
    """Get the latest patch version from git tags.
    Args:
        base_version (str): The base version in the format 'X.Y'.
    Returns:
        int: The latest patch version number.
    """
    subprocess.run(["git", "fetch", "--tags"], check=True)
    pattern = re.compile(rf"^v{re.escape(base_version)}\.(\d+)$")
    tags = subprocess.check_output(["git", "tag"], text=True).splitlines()
    patches = [int(m.group(1)) for t in tags if (m := pattern.match(t))]
    return max(patches, default=-1)


def bump_patch_tag(version_file: Path) -> str:
    """Bump the patch version and return the new tag.
    Args:
        version_file (Path): Path to the version file.
    Returns:
        str: The new tag in the format 'vX.Y.Z'.
    """
    base = get_base_version(version_file)
    latest_patch = get_latest_patch(base)
    new_patch = latest_patch + 1
    return f"v{base}.{new_patch}"


def create_and_push_tag(tag: str) -> None:
    """Create a new git tag and push it to the remote repository.
    Args:
        tag (str): The tag to create and push.
    """
    existing_tags = subprocess.check_output(["git", "tag"], text=True).splitlines()
    if tag in existing_tags:
        logging.info(f"Tag {tag} already exists. Skipping creation.")
        return
    subprocess.run(["git", "tag", tag], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)


def main(version_file: Path, dry_run: bool) -> None:
    """Main function to bump the patch version and create a tag.
    Args:
        version_file (Path): Path to the version file.
        dry_run (bool): If True, do not create the tag.
    """
    new_tag = bump_patch_tag(version_file)
    logging.info("Creating patch version: %s", new_tag)
    if dry_run:
        logging.info("Dry run enabled, not creating tag.")
        return
    create_and_push_tag(new_tag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version-file",
        type=Path,
        default=Path("VERSION"),
        help="Path to the version file (default: VERSION)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not write changes")
    args = parser.parse_args()
    main(args.version_file, args.dry_run)
