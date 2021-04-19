from os import path

import click

from libs.controller import init, load_plugins, load_pocs, load_targets, start, load_config, end, init_plugins, end_plugins
from utils import banner


@click.command()
@click.option("--url", "-u", type=str, multiple=True, help="Load targets from {parser}.")
@click.option("--file", "-f", type=str, multiple=True, help="Load targets from file and use {parser}.")
@click.option("--poc", "-p", multiple=True, help="Load poc from {parser}.")
@click.option("--pocs_path", help="User custom poc dir.")
@click.option("--out", "-o", default=["console", ], multiple=True, help="Use output plugins. default is console")
@click.option("--plugins_path", help="User custom output plugin dir.")
@click.option("--threads", type=int, default=10)
@click.option("--config", "-c", type=str, help="Load config from a configuration toml file.")
@click.option("--verbose", "-v", count=True, help="display verbose information.")
@click.option("-vv", count=True, help="display more verbose information.")
def main(verbose: bool = False, vv: bool = False, threads: int = 10, config: str = "", url: str = "", file: str = "", poc=[], pocs_path: str = "", out=[], plugins_path: str = ""):
    # load targets from url or file
    root_path = path.dirname(path.realpath(__file__))
    banner()
    init(root_path, verbose, vv)

    load_config(config)
    load_plugins(plugins_path)
    load_targets(url, file)
    load_pocs(pocs_path, poc)

    init_plugins()

    try:
        start(threads, out)
    finally:
        end_plugins()
        end()
    ...


if __name__ == "__main__":
    main()
