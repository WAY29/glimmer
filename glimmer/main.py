from os import path
import click

from glimmer.libs.controller import init, init_output_plugins, load_plugins, load_pocs, load_targets, start, load_config, set_config, end, init_plugins, enable_plugins, end_plugins
from glimmer.libs.core.config import POCS, CONFIG
from glimmer.utils import banner, cprint, header, print_traceback, get_full_exception_name


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--url", "-u", type=str, multiple=True, help="Load targets from {parser}.")
@click.option("--file", "-f", type=str, multiple=True, help="Load targets from file and parse each line with {parser}.")
@click.option("--poc", "-p", multiple=True, help="Load pocs from {parser}.")
@click.option("--poc-file", "-pf", multiple=True, help="Load pocs from file and parse each line with {parser}.")
@click.option("--pocs_path", type=str, default="", help="User custom poc dir.")
@click.option("--attack", count=True, help="set poc mode to attack mode, default is check mode.")
@click.option("--out", "-o", default=["console", ], multiple=True, help="Use output plugins. default is console")
@click.option("--plugins_path", type=str, default="", help="User custom output plugin dir.")
@click.option("--threads", type=int, help="Number of threads", default=10)
@click.option("--config", "-c", type=str, help="Load config from a configuration toml file.")
@click.option("--timeout", "-t", default=300, help="Max program runtime.")
@click.option("--verbose", "-v", count=True, help="display verbose information.")
@click.option("-vv", count=True, help="display more verbose information.")
@click.option("--debug", count=True, help="setup debug mode.")
def main(ctx, verbose: int = 0, vv: bool = False, threads: int = 10, config: str = "", url: list = [], file: list = [], poc: list = [], poc_file: list = [], pocs_path: str = "", attack: int = 0, out=[], plugins_path: str = "", debug: int = 0, timeout: int = 300):
    """
    A poc framework base on python.

    Tips:
    {parser} are plugins in plugins/parser which parse user input by protocol and get data for poc and target, you can write yourself parser.
    """
    run_in_main = not ctx.invoked_subcommand
    root_path = path.dirname(path.realpath(path.join(__file__, '..')))

    if run_in_main:
        banner()
    init(root_path, debug)
    # redefine options
    local_vars = locals()
    option_keys = [key for key in local_vars.keys() if key not in (
        "ctx", "run_in_main", "root_path", "debug")]
    new_options = load_config(config)
    # force type translate
    for key in option_keys:
        desired_type = type(local_vars[key])
        if key in new_options and not isinstance(new_options[key], desired_type):
            try:
                if desired_type in (tuple, list):
                    new_options[key] = [v.strip()
                                        for v in new_options[key].split(",")]
                else:
                    new_options[key] = desired_type(new_options[key])
            except Exception:
                del new_options[key]
    options = dict(local_vars, **new_options)

    set_config(options['verbose'], options['vv'], options['debug'], options['attack'])
    try:
        load_plugins(options['plugins_path'])
        load_pocs(options['poc'], options['poc_file'], options['pocs_path'])

        if run_in_main:
            enable_plugins(options['out'])
            try:
                init_plugins()
                init_output_plugins(options['out'])
                load_targets(options['url'], options['file'])
                start(options['threads'], options['timeout'])
            finally:
                end_plugins()
                end()
    except Exception as e:
        if CONFIG.option.debug:
            print_traceback()
        else:
            cprint(header("Base", "-", "Main breakout: %s: %s\n" %
                   (get_full_exception_name(e), str(e))))


@main.command()
@click.argument("pocs", nargs=-1)
def show_poc_info(pocs):
    """
    Show poc information by poc filename.
    """
    for poc_name in pocs:
        if poc_name in POCS.instances:
            poc_s = POCS.instances[poc_name]
            for poc in poc_s:
                poc.show_info()
        else:
            cprint(header("", "-", "can't find %s" % poc_name))


@main.command()
@click.option("--type", "-t", type=str, help="search pocs with input string by type.")
@click.option("--filename", "-fn", type=str, help="search pocs with input string by poc filename.")
@click.option("--name", "-n", type=str, help="search pocs with input string by poc name.")
def search_poc(type="", filename="", name=""):
    """
    Search pocs by poc type / poc name / poc filename.
    """
    if type:
        result = ", ".join(poc_name for poc_name,
                           poc_s in POCS.instances.items() if any(type.lower() in poc.type.lower() for poc in poc_s))
    elif filename:
        result = ", ".join(poc_name for poc_name,
                           _ in POCS.instances.items() if filename.lower() in poc_name.lower())
    elif name:
        result = ", ".join(poc_name for poc_name,
                           poc_s in POCS.instances.items() if any(name.lower() in poc.name.lower() for poc in poc_s))

    result = "[cyan]%s[/]" % result if result else "[red]No result[/]"
    cprint("[yellow]Search result:[/]\n    " + result)


if __name__ == "__main__":
    main()
