from libs.core.exceptions import ParserExceptions
from libs.core.config import PLUGINS


def parse_path(path, excludes=()):
    parsers = [instance
               for instance in PLUGINS.parser.values()]
    for parser in parsers:
        parser_str = str(parser)
        if any(exclude in parser_str for exclude in excludes):
            return path
        if parser.rule_check(path):
            try:
                return parser.get_data(path)
            except Exception as e:
                raise ParserExceptions.Base() from e
    return ""
