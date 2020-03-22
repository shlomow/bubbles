from bubbles.readers.proto import ProtoReader
import gzip


def find_reader(format):
    if format == 'protobuf':
        return ProtoReader

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


def read(path, format):
    reader = Reader(path, format)
    print(reader.user)
    for snapshot in reader:
        print(snapshot)
