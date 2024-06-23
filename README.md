# CoCoder

CoCoder is a CLI tool designed to help manage changes in a project by leveraging AI to generate and apply modifications. This tool is particularly useful for developers looking to automate the process of making specific changes across their codebase.

## Installation

To install CoCoder, you need to have Python 3.x installed on your system. You can install CoCoder via pip:

```bash
pip install cocoder
```

## Usage

CoCoder provides a simple CLI interface to interact with your project. Here are the basic commands:

### Build Command

To request changes and apply them to a new branch, use the `build` command:

```bash
coco build --request "Your change request here" --branch new-feature-branch --root_dir . --extensions .py
```

- `--request` or `-r`: The change you want the model to make.
- `--branch` or `-b`: The branch to move the change to.
- `--root_dir` or `-d`: The directory where the `.git` is located (default is the current directory).
- `--extensions` or `-e`: File extensions to consider (default is `.py`).

### Example

```bash
coco build --request "Add a function to calculate the sum of two numbers" --branch add-sum-function --root_dir . --extensions .py
```

This command will create a new branch named `add-sum-function`, apply the requested change, and commit the changes to the new branch.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
