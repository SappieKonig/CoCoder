#!/usr/bin/env python3
import click
from .api_utils import get_deepseek_answer
from .change_manager import update_files_in_new_branch
import os
import json


class VariableArgs(click.ParamType):
    name = "variable_args"

    def convert(self, value, param, ctx):
        return value.split()


@click.group()
def cli():
    pass


CONFIG_PATH = os.path.expanduser('~/.cocoder/config.json')


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)


@cli.command()
@click.option('--request', '-r', required=True, help='The change you want the model to make')
@click.option('--branch', '-b', default=None, help='Branch to move the change to.')
@click.option('--root_dir', '-d', default=None, help='Directory where the .git is located')
@click.option('--extensions', '-e', default=None, help='File extensions to consider', type=VariableArgs())
@click.option('--commit', '-c', is_flag=True, default=None, help='Whether to commit changes immediately')
def build(request, branch, root_dir, extensions, commit):
    """Build the project"""
    config = load_config()
    root_dir = root_dir or config.get('root_dir', '.')
    commit = commit if commit is not None else config.get('commit', False)
    api_key = config.get('deepseek_api_key', None)
    if api_key is not None:
        os.environ['DEEPSEEK_API_KEY'] = api_key
    changes = get_deepseek_answer(request, root_dir)
    if not branch:
        click.echo("Branch not provided. Applying changes to the current branch.")
    else:
        branch = branch.replace(' ', '_')  # Replace spaces with underscores
    update_files_in_new_branch(changes, branch, commit)


@cli.command()
@click.option('--root_dir', '-d', default=None, help='Directory where the .git is located')
@click.option('--extensions', '-e', default=None, help='File extensions to consider', type=VariableArgs())
@click.option('--commit', '-c', is_flag=True, default=None, help='Whether to commit changes immediately')
@click.option('--deepseek_api_key', default=None, help='DeepSeek API key for authentication')
def set_config(root_dir, extensions, commit, deepseek_api_key):
    """Set configuration values"""
    config = load_config()
    if root_dir is not None:
        config['root_dir'] = root_dir
    if extensions is not None:
        config['extensions'] = list(extensions)
    if commit is not None:
        config['commit'] = commit
    if deepseek_api_key is not None:
        config['deepseek_api_key'] = deepseek_api_key
    save_config(config)
    if 'root_dir' in config:
        click.echo(f"Set root_dir to {config['root_dir']}")
    if 'extensions' in config:
        click.echo(f"Set extensions to {config['extensions']}")
    if 'commit' in config:
        click.echo(f"Set commit to {config['commit']}")
    if 'deepseek_api_key' in config:
        click.echo("DeepSeek API key set")


@cli.command()
@click.option('--extensions', '-e', required=True, help='File extensions to add to the list', type=VariableArgs())
def add_extensions(extensions):
    """Add extensions to the existing list"""
    config = load_config()
    current_extensions = config.get('extensions', DEFAULT_EXTENSIONS)
    new_extensions = list(set(current_extensions + list(extensions)))
    config['extensions'] = new_extensions
    save_config(config)
    click.echo(f"Added extensions: {extensions}")
    click.echo(f"Updated extensions list: {new_extensions}")


if __name__ == "__main__":
    cli()