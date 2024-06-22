import os


def list_directory_structure(root_dir) -> str:
    ret = ""
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        ret += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            ret += f"{sub_indent}{f}\n"
    return ret


def list_files_and_contents(root_dir, file_extensions: list[str] = [".py"]) -> str:
    ret = ""
    for root, dirs, files in os.walk(root_dir):
        for file_name in files:
            if not any(file_name.endswith(extension) for extension in file_extensions):
                continue
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    ret += repr({"file_path": file_path, "content": content})
            except Exception as e:
                ret += f"Could not read file {file_path}: {e}"
            ret += "\n"
    return ret


def collapse_directory(root_dir, file_extensions: list[str]) -> str:
    ret = "Directory Structure:\n"
    ret += list_directory_structure(root_dir)
    ret += "\n\n"
    ret += "Files and Contents:\n"
    ret += list_files_and_contents(root_dir, file_extensions)
    return ret
