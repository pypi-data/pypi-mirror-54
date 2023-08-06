import click
import logging
import os
from clint.textui import puts, colored, indent
import questionary
import pprint

from . import configfile

def interactive_query_config(server='127.0.0.1',port='5800',user='admin',password='admin'):
    
    questions = [
        {
            'type': 'input',
            'name': 'server',
            'default': server,
            'message': 'Server: ',
        },
        {
            'type': 'input',
            'name': 'port',
            'default': port,
            'message': 'Server Port: ',
        },
        {
            'type': 'input',
            'name': 'user',
            'default': user,
            'message': 'Username: ',
        },
        {
            'type': 'input',
            'name': 'password',
            'default': password,
            'message': 'Password: ',
        },
    ]

    answers = questionary.prompt(questions)
    return answers

@click.group('config', help="View, edit, or create your configuration file")
@click.pass_context
def config(ctx):
    pass


@config.command('show', help="View your configuration file")
@click.pass_context
def show(ctx):
    
    config_file = ctx.obj['config_path']
    config_exists = os.path.exists(config_file)

    if not config_exists:
        click.echo("Configuration file \"" + config_file + "\" does not exist")
        click.echo("Quitting.")
        return
    config = configfile.get_config(config_file)

    for section in config.sections():
        click.echo('['+section+']')
        pprint.pprint(dict(config.items(section)))
    

@config.command('edit', help="Edit your configuration file")
@click.pass_context
def edit(ctx):

    config_file = ctx.obj['config_path']
    config_exists = os.path.exists(config_file)

    if not config_exists:
        click.echo("Configuration file \"" + config_file + "\" does not exist")
        click.echo("Quitting.")
        return

    config = configfile.get_config(config_file)

    if 'NEOSERVER' not in config:
        answers = interactive_query_config()
    else:
        c = config['NEOSERVER']
        answers = interactive_query_config(c['server'],c['serverport'],c['username'],c['password'])
    
    try:
        configfile.write_config(config_file, answers['server'],answers['port'],answers['user'],answers['password'])
        click.echo('Config written')
    except Exception as e:
        click.echo("Error writing config: " + e)

    pass

@config.command('create', help="Create your configuration file")
@click.pass_context
def create(ctx):

    config_file = ctx.obj['config_path']
    config_exists = os.path.exists(config_file)

    if config_exists:
        overwrite = questionary.confirm("Config file \"" + config_file + "\" already exist, overwrite?").ask()
        if not overwrite:
            click.echo("Nothing to do, quitting.")
            return
    else:
        do_create = questionary.confirm("Create config file \"" + config_file + "\" ? ").ask
        if not do_create:
            click.echo("Nothing to do, quitting.")
            return

    answers = interactive_query_config()
    try:
        configfile.write_config(config_file, answers['server'],answers['port'],answers['user'],answers['password'])
        click.echo('Config written')
    except Exception as e:
        click.echo("Error writing config: " + e)
