import bubbles.parsers
import pathlib
import importlib
import inspect
from bubbles.protocol import deserialize_message


def load_parsers():
    # import all submodules of the parsers
    root = pathlib.Path(bubbles.parsers.__file__).parent
    for path in root.iterdir():
        if path.name.startswith('_') or not path.suffix == '.py':
            continue
        importlib.import_module(f'.{path.stem}', package='bubbles.parsers')

    # map parser name to its function or class
    out = dict()
    for _, module in inspect.getmembers(bubbles.parsers, inspect.ismodule):
        for _, member in inspect.getmembers(module):
            if inspect.isclass(member) or inspect.isfunction(member):
                if 'name' in member.__dict__:
                    parser_name = member.__dict__['name']
                    if inspect.isclass(member):
                        out[parser_name] = member()
                    else:
                        out[parser_name] = member

    return out


def run_parser(topic, data):
    parsers = load_parsers()
    user, snapshot = deserialize_message(data)
    if topic in parsers:
        return parsers[topic](None, user, snapshot)
    else:
        raise ValueError('invalid parser name')
