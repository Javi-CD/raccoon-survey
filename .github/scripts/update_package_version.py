#!/usr/bin/env python3

import sys
import json
import argparse


def update_package_version(file_path, new_version):
    """
    Update version in package.json file

        Args:
            file_path (str): Path to package.json file
            new_version (str): New version to set (e.g., 'v1.0.1' or '1.0.1')
        Returns:
            bool: True if update was successful, False otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Remove 'v' prefix if present
        clean_version = new_version.lstrip("v")

        # Update the version
        old_version = data.get("version", "unknown")
        data["version"] = clean_version

        # Write back to file with proper formatting
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")  # Add newline at end

        print(
            f">>Updated version from {old_version} to {clean_version} in {file_path}"
        )
        return True

    except FileNotFoundError:
        print(f">>Error: File {file_path} not found")
        return False
    except json.JSONDecodeError as e:
        print(f">>Error: Invalid JSON in {file_path}: {e}")
        return False
    except Exception as e:
        print(f">>Error updating {file_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Update version in package.json")
    parser.add_argument("version", help="New version (e.g., v1.0.1 or 1.0.1)")
    parser.add_argument(
        "--file", default="package.json", help="Path to package.json file"
    )

    args = parser.parse_args()

    success = update_package_version(args.file, args.version)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
