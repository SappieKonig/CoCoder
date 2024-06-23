import os
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class FileData:
    filepath: str
    content: str


def update_files_in_new_branch(files_data: list[FileData], branch_name: Optional[str], commit: bool):
    if branch_name is not None:
        # Create a new branch
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)

    # Iterate through each file data in the list
    for file_data in files_data:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_data.filepath), exist_ok=True)

        # Write the content to the file
        with open(file_data.filepath, 'w') as file:
            file.write(file_data.content)

        # Add the file to the git staging area
        subprocess.run(["git", "add", file_data.filepath], check=True)

    if commit:
        subprocess.run(["git", "commit", "-m", f"Automated changes for branch {branch_name}"], check=True)
