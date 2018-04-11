# -*- coding:utf-8 -*-
import click

from initialize import genesis
from grpc import grpc


@click.group()
def manager():
    pass


manager.add_command(genesis)
manager.add_command(grpc)
