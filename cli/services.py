# -*- coding:utf-8 -*-
import click

from api.grpc.server import serve as serve_grpc


@click.group()
def service():
    pass


@click.command()
@click.argument('command')
def grpc(command):
    if command == 'start':
        serve_grpc()
    else:
        click.echo('Unknown command')


service.add_command(grpc)
