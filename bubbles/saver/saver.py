from sqlalchemy import create_engine
import pathlib
import bubbles.saver
import importlib
import inspect
import json


class Saver:
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(self.url)
        self.savers = self.load_savers()

    def load_savers(self):
        # import all submodules of the savers
        root = pathlib.Path(bubbles.saver.__file__).parent
        for path in root.iterdir():
            if path.suffix == '.py' and not path.name.startswith('_'):
                importlib.import_module(f'.{path.stem}',
                                        package='bubbles.saver')

        # map parser name to its function or class
        out = dict()
        for _, module in inspect.getmembers(bubbles.saver, inspect.ismodule):
            for _, member in inspect.getmembers(module):
                if inspect.isclass(member) or inspect.isfunction(member):
                    if 'name' in member.__dict__:
                        parser_name = member.__dict__['name']
                        if inspect.isclass(member):
                            out[parser_name] = member()
                        else:
                            out[parser_name] = member

        return out

    def save(self, topic, data):
        if topic in self.savers:
            self.savers[topic](self.engine, json.loads(data))
        else:
            raise ValueError('invalid saver name')
