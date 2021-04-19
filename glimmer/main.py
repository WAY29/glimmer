from os import path

import click

from libs.controller import init, init_output_plugins, load_plugins, load_pocs, load_targets, start, load_config, end, init_plugins, enable_plugins, end_plugins
from libs.core.config import POCS
from utils import banner, cprint
from utils.printer import header


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--url", "-u", type=str, multiple=True, help="Load targets from {parser}.")
@click.option("--file", "-f", type=str, multiple=True, help="Load targets from file and parse each line with {parser}.")
@click.option("--poc", "-p", multiple=True, help="Load poc from {parser}.")
@click.option("--pocs_path", help="User custom poc dir.")
@click.option("--out", "-o", default=["console", ], multiple=True, help="Use output plugins. default is console")
@click.option("--plugins_path", help="User custom output plugin dir.")
@click.option("--threads", type=int, default=10)
@click.option("--config", "-c", type=str, help="Load config from a configuration toml file.")
@click.option("--verbose", "-v", count=True, help="display verbose information.")
@click.option("-vv", count=True, help="display more verbose information.")
@click.option("--debug", count=True, help="setup debug mode.")
def main(ctx, verbose: int = 0, vv: bool = False, threads: int = 10, config: str = "", url: str = "", file: str = "", poc=[], pocs_path: str = "", out=[], plugins_path: str = "", debug: int = 0):
    """
    A poc framework base on python.

    Tips:
    {parser} are plugins in plugins/parser which parse user input by protocol and get data for poc and target, you can write yourself parser.
    """
    run_in_main = not ctx.invoked_subcommand
    root_path = path.dirname(path.realpath(__file__))

    if run_in_main:
        banner()

    init(root_path, verbose, vv, debug)
    load_config(config)
    load_plugins(plugins_path)
    load_pocs(pocs_path, poc)

    if run_in_main:
        enable_plugins(out)
        try:
            init_plugins()
            init_output_plugins(out)
            load_targets(url, file)
            start(threads)
        finally:
            end_plugins()
            end()

    ...


@main.command()
@click.argument("pocs", nargs=-1)
def show_poc_info(pocs):
    for poc_name in pocs:
        if poc_name in POCS.instances:
            poc = POCS.instances[poc_name]
            poc.show_info()
        else:
            cprint(header("", "-", "can't find %s" % poc_name))

if __name__ == "__main__":
    main()
