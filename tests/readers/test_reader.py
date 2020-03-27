import gzip
import pytest
from bubbles.readers import Reader
from bubbles.readers.proto import ProtoReader
import bubbles.readers
from bubbles.utils import create_stream


def test_find_reader():
    assert bubbles.readers.reader.find_reader('protobuf') == ProtoReader
    with pytest.raises(TypeError):
        bubbles.readers.reader.find_reader('blabla')


def test_reader(tmp_path, user, snapshot):
    stream = create_stream(user, [snapshot])

    path = tmp_path / 'snapshot.data'
    path.write_bytes(stream.read())

    reader = Reader(str(path), 'protobuf')
    assert reader.user == user

    snapshots_iter = iter(reader)
    assert next(snapshots_iter) == snapshot
    with pytest.raises(StopIteration):
        next(snapshots_iter)


def test_reader_gzip(tmp_path, user, snapshot):
    stream = create_stream(user, [snapshot])

    path = tmp_path / 'snapshot.data.gz'
    path.write_bytes(gzip.compress(stream.read()))

    reader = Reader(str(path), 'protobuf')
    assert reader.user == user

    snapshots_iter = iter(reader)
    assert next(snapshots_iter) == snapshot
    with pytest.raises(StopIteration):
        next(snapshots_iter)
