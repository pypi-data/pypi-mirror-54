import click
import logging
import os
from clint.textui import puts, colored, indent

@click.group('query', help='Run queries against the database(s)')
@click.pass_context
def query(ctx):
    #create a database object and place it in the context
    pass

@query.command('cypher')
@click.option('-c','--command', type=click.STRING, default=None)
@click.pass_context
def cypher(ctx, command):
    if command:
        puts(colored.white('Running cypher query:'))
        with indent(4, quote='>>>'):
            puts(colored.green(command))