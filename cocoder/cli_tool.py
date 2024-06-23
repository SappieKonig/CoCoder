#!/usr/bin/env python3
import click
from .api_utils import get_deepseek_answer
from .change_manager import update_files_in_new_branch


@click.group()
def cli():
    pass


DEFAULT_EXTENSIONS = ['.py', '.md']


@cli.command()
@click.option('--request', '-r', help='The change you want the model to make')
@click.option('--branch', '-b', help='Branch to move the change to.')
@click.option('--root_dir', '-d', default='.', help='Directory where the .git is located')
@click.option('--extensions', '-e', multiple=True, default=DEFAULT_EXTENSIONS, help='File extensions to consider')
def build(request, branch, root_dir, extensions):
    """Build the project"""
    changes = get_deepseek_answer(request, root_dir, extensions)
    update_files_in_new_branch(changes, branch)


if __name__ == "__main__":
    cli()
