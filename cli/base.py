# -*- coding:utf-8 -*-
import click

from initialize import genesis # noqa


@click.group()
def manager():
    pass


manager.add_command(genesis)
