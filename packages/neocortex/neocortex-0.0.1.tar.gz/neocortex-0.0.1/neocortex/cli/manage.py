import click
from pkg_resources import iter_entry_points
from click_plugins import with_plugins
import configparser
import logging
import os

from clint.textui import puts, colored, indent

from .plugins.config import commands as config_commands
from .plugins.query import commands as query_commands

from .plugins.config import configfile


@with_plugins(iter_entry_points('neocortex.cli_plugin'))
@click.group()
@click.option('--debug', is_flag=True, default=False, help='Verbose printing')
@click.option('--config-path', type=click.Path(), default='~/neo.cfg', help='Configuration file to use, default: "~/neo.cfg"')
@click.pass_context
def cli(ctx, debug, config_path):
    if debug:
        click.echo(colored.green('Debug mode is on.'))

    config_path = os.path.abspath(os.path.expanduser(config_path)).replace("\\","/")

    ctx_obj = {}
    ctx_obj["config_path"] = config_path
    ctx_obj["debug"] = debug

    if not os.path.exists(config_path):
        click.echo(colored.red("Config file not found: " + config_path))
        click.echo(colored.red("Run 'neo config create' to create a required configuration file."))
    else:
        click.echo(colored.green("Config file loaded: " + config_path))
        config = configfile.get_config(config_path)
        ctx_obj['config'] = {}
        for section in config.sections():
            ctx_obj['config'][section] = dict(config.items(section))
     
    ctx.obj = ctx_obj


cli.add_command(config_commands.config)
cli.add_command(query_commands.query)

if __name__ == "__main__":
    cli()