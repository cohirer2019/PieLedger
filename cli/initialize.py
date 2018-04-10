# -*- coding:utf-8 -*-
import click
from piecash import GnucashException

from core.book import create_book


@click.command()
@click.option(
    '--overwrite', is_flag=True, help='Overwrite existing data')
def genesis(overwrite):
    try:
        create_book(overwrite=overwrite)
    except GnucashException, e:
        click.echo(e)
