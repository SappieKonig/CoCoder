import os
import subprocess


def list_directory_structure(root_dir) -> str:
    ret = ""
    result = subprocess.run(['git', 'ls-files'], cwd=root_dir, capture_output=True, text=True)
    files = result.stdout.splitlines()
    for file in files:
        ret += f"{file}\n"
    return ret


def list_files_and_contents(root_dir) -> str:
    ret = ""
    result = subprocess.run(['git', 'ls-files'], cwd=root_dir, capture_output=True, text=True)
    files = result.stdout.splitlines()
    for file_name in files:
        file_path = os.path.join(root_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                ret += repr({"file_path": file_path, "content": content})
        except Exception as e:
            ret += f"Could not read file {file_path}: {e}"
        ret += "\n"
    return ret


def collapse_directory(root_dir) -> str:
    ret = "Directory Structure:\n"
    ret += list_directory_structure(root_dir)
    ret += "\n\n"
    ret += "Files and Contents:\n"
    ret += list_files_and_contents(root_dir)
    return ret
