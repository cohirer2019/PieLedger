# -*- coding:utf-8 -*-
import click

from api.grpc.server import serve as serve_grpc


@click.group()
def service():
    pass


@service.command()
@click.argument('command', type=click.Choice(('start', )))
def grpc(command):
    if command == 'start':
        serve_grpc()
