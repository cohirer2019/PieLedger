# -*- coding:utf-8 -*-
import click

from initialize import genesis
from services import service


@click.group()
def manager():
    pass


manager.add_command(genesis)
manager.add_command(service)
