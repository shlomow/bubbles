from sqlalchemy import create_engine
import sqlalchemy
import contextlib
import pathlib
import bubbles.saver
import importlib
import inspect
import json


class Saver:
    '''Saver object that given a url can save to db every topic it supports.
        `url` can be any url compatible with sqlalchemy.
    '''
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(self.url)
        self.savers = self.load_savers()

    def load_savers(self):
        '''Load the savers objects that the system supports.

        :return: dictionary that maps each topic to its save function
        '''
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
        '''Save topic data to db.

        :param topic: `topic` to save.
        :param data: `data` of topic to save.
        :raises: ValueError if `topic` has no saver
        '''
        if topic in self.savers:
            with contextlib.suppress(sqlalchemy.exc.IntegrityError):
                self.savers[topic](self.engine, json.loads(data))
        else:
            raise ValueError('invalid saver name')
