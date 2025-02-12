import os
import sys
import json
from pathlib import Path

def get_folder_structure(root_path: Path) -> dict:
    """
    Recursively collects a dictionary describing the folder structure,
    storing both relative and absolute paths to subfolders and files.
    Skips directories named:
      - node_modules
      - .git
      - reports
    """
    folder_structure = {}

    for root, dirs, files in os.walk(root_path):
        # Remove specific directories so they won't be traversed or listed
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.git' in dirs:
            dirs.remove('.git')
        if 'reports' in dirs:
            dirs.remove('reports')
        if 'test-results' in dirs:
            dirs.remove('test-results')

        relative_root = os.path.relpath(root, root_path)
        absolute_root = os.path.abspath(root)

        # Prepare a list to hold file info (with absolute paths)
        file_info = []
        for f in files:
            abs_file_path = os.path.join(absolute_root, f)
            file_info.append({
                "name": f,
                "absolute_path": abs_file_path
            })

        folder_structure[relative_root] = {
            "absolute_root": absolute_root,
            "dirs": dirs,
            "files": file_info
        }
    
    return folder_structure

def main():
    """
    Usage:
      python script.py [folder_path]

    If folder_path is omitted, it defaults to the current directory.
    This script will save the folder structure in 'folder_structure.json'.
    """
    # Check if a folder path was provided
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(".")

    # Verify the provided path
    if not root_dir.is_dir():
        print(f"Error: The path '{root_dir}' does not exist or is not a directory.")
        sys.exit(1)

    # Get folder structure
    structure = get_folder_structure(root_dir)

    # Save to JSON file
    output_file = "folder_structure.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    print(f"Folder structure saved to '{output_file}'")

if __name__ == "__main__":
    main()
