# -*- coding:utf-8 -*-
import click


@click.group()
def grpc():
    pass


@grpc.command()
def start():
    from api.grpc.server import serve
    serve()
