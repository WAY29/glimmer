from glimmer.libs.core.exceptions import ParserExceptions
from glimmer.libs.core.config import PLUGINS


def parse_path(path, excludes=()):
    parsers = [instance
               for instance in PLUGINS.parser.values()]
    for parser in parsers:
        parser_str = str(parser)
        if any(exclude in parser_str for exclude in excludes):
            continue
        if parser.rule_check(path):
            try:
                return parser.get_data(path)
            except Exception as e:
                raise ParserExceptions.Base(e) from e
    return (path, )
