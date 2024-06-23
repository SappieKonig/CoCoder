#!/usr/bin/env python3
import click
from .api_utils import get_deepseek_answer
from .change_manager import update_files_in_new_branch
import os
import json


@click.group()
def cli():
    pass


DEFAULT_EXTENSIONS = ['.py', '.md']
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
@click.option('--request', '-r', help='The change you want the model to make')
@click.option('--branch', '-b', help='Branch to move the change to.')
@click.option('--root_dir', '-d', default=None, help='Directory where the .git is located')
@click.option('--extensions', '-e', multiple=True, default=None, help='File extensions to consider')
def build(request, branch, root_dir, extensions):
    """Build the project"""
    config = load_config()
    root_dir = root_dir or config.get('root_dir', '.')
    extensions = extensions or config.get('extensions', DEFAULT_EXTENSIONS)
    changes = get_deepseek_answer(request, root_dir, extensions)
    update_files_in_new_branch(changes, branch)


@cli.command()
@click.option('--root_dir', '-d', default=None, help='Directory where the .git is located')
@click.option('--extensions', '-e', multiple=True, default=None, help='File extensions to consider')
def set_config(root_dir, extensions):
    """Set configuration values"""
    config = load_config()
    if root_dir is not None:
        config['root_dir'] = root_dir
    if extensions is not None:
        config['extensions'] = list(extensions)
    save_config(config)
    if 'root_dir' in config:
        click.echo(f"Set root_dir to {config['root_dir']}")
    if 'extensions' in config:
        click.echo(f"Set extensions to {config['extensions']}")


if __name__ == "__main__":
    cli()