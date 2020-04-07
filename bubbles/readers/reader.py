import bubbles.readers
import gzip
import pathlib
import inspect
import importlib


def find_reader(format):
    '''Find availabe reader according to the `format`.

    :param format: format of the file we want to read.
    :return: object which is iterable and can parse the given `format`.
    :raises: TypeError, if `format` is not supported.
    '''
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
    '''Class that represents a generic snapshots reader mechansim.
        Every reader should be iterable and return a snapshot every iteration.
    '''
    def __init__(self, path, format):
        '''Contructor.
        :param path: path to the file to parse.
        :param format: format of `path`.
        '''
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
