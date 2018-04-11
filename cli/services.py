# -*- coding:utf-8 -*-
import click


@click.group()
def service():
    pass


@service.command()
@click.argument('command', type=click.Choice(('start', )))
def grpc(command):
    if command == 'start':
        from api.grpc.server import serve
        serve()
