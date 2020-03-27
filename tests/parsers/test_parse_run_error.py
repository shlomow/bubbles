import pytest
from bubbles.parsers import run_parser
from bubbles.utils import create_stream


def test_run_error(user, snapshot):
    data = create_stream(user, [snapshot]).read()
    with pytest.raises(ValueError):
        run_parser('blabla', data)
