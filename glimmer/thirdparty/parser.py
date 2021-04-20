import sys
from io import StringIO
import contextlib


@contextlib.contextmanager
def catch_stdout(stdout=None):
    """
    Reference:
        https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
    """
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
