#!/usr/bin/env python3

import sys
import re
import argparse


def update_pyproject_version(file_path, new_version):
    """
    Update version in pyproject.toml file

        Args:
            file_path (str): Path to pyproject.toml file
            new_version (str): New version to set (e.g., 'v1.0.1' or '1.0.1')
        Returns:
            bool: True if update was successful, False otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove 'v' prefix if present
        clean_version = new_version.lstrip("v")

        # Pattern to match version line in pyproject.toml
        pattern = r'^version\s*=\s*["\'][^"\']*["\']'
        replacement = f'version = "{clean_version}"'

        # Update the version
        updated_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

        # Check if version was found and updated
        if updated_content == content:
            print(f"Warning: Version pattern not found in {file_path}")
            return False

        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f">>Updated version to {clean_version} in {file_path}")
        return True

    except FileNotFoundError:
        print(f">>Error: File {file_path} not found")
        return False
    except Exception as e:
        print(f">>Error updating {file_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Update version in pyproject.toml")
    parser.add_argument("version", help="New version (e.g., v1.0.1 or 1.0.1)")
    parser.add_argument(
        "--file", default="pyproject.toml", help="Path to pyproject.toml file"
    )

    args = parser.parse_args()

    success = update_pyproject_version(args.file, args.version)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
