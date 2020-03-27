import bubbles.readers
import gzip
import pathlib
import inspect
import importlib


def find_reader(format):
    # import all submodules of the readers
    root = pathlib.Path(bubbles.readers.__file__).parent
    for path in root.iterdir():
        if path.suffix == '.py' and not path.name.startswith('_'):
            importlib.import_module(f'.{path.stem}', package='bubbles.readers')

    # search for format in the classes we imported
    for _, module in inspect.getmembers(bubbles.readers, inspect.ismodule):
        for _, member in inspect.getmembers(module, inspect.isclass):
            if 'format' in member.__dict__:
                if format == member.__dict__['format']:
                    return member

    raise TypeError("unknown format")


class Reader:
    def __init__(self, path, format):
        self.path = path
        self.format = format
        if path.endswith('.gz'):
            self.fd = gzip.open(path, 'rb')
        else:
            self.fd = open(path, 'rb')
        reader = find_reader(self.format)
        self.reader = reader(self.fd)
        self.user = self.reader.user

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.reader)

        except StopIteration:
            self.fd.close()
            raise StopIteration
