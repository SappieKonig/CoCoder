# CoCoder

CoCoder is a CLI tool designed to help manage changes in a project by leveraging AI to generate and apply modifications. This tool is particularly useful for developers looking to automate the process of making specific changes across their codebase.

## Installation

To install CoCoder, you need to have Python 3.x installed on your system. You can install CoCoder via pip:

```bash
pip install git+https://github.com/SappieKonig/CoCoder.git
```

## Usage

CoCoder provides a simple CLI interface to interact with your project. Here are the basic commands:

### Build Command

To request changes and apply them to a new branch, use the `build` command:

```bash
coco build --request "Your change request here" --branch new-feature-branch
```

- `--request` or `-r`: The change you want the model to make. This option is required.
- `--branch` or `-b`: The branch to move the change to. If not provided, changes will be applied to the current branch, and the user will be alerted.
- `--root_dir` or `-d`: The directory where the `.git` is located (default is the current directory).
- `--extensions` or `-e`: File extensions to consider (default is `.py`, `.md`).
- `--commit` or `-c`: Whether to commit changes immediately (default is `False`).

### Set Configuration Command

To set default values for `root_dir` and `extensions`, use the `set_config` command:

```bash
coco set_config --root_dir . --extensions ".py .md"
```

- `--root_dir` or `-d`: The directory where the `.git` is located (default is the current directory).
- `--extensions` or `-e`: File extensions to consider (default is `.py`).

### Add Extensions Command

To add new file extensions to the existing list, use the `add_extensions` command:

```bash
coco add_extensions --extensions ".txt .js"
```

- `--extensions` or `-e`: File extensions to add to the list. This option is required.

### Example

```bash
coco build --request "Add a function to calculate the sum of two numbers" --branch add-sum-function
```

This command will create a new branch named `add-sum-function`, apply the requested change, and commit the changes to the new branch if the `--commit` option is specified.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
