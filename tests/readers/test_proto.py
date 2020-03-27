from bubbles.readers.proto import ProtoReader
import pytest
from bubbles.utils import create_stream


def test_proto_reader(user, snapshot):
    stream = create_stream(user, [snapshot])

    reader = ProtoReader(stream)
    assert reader.user == user

    snapshots_iter = iter(reader)
    assert next(snapshots_iter) == snapshot
    with pytest.raises(StopIteration):
        next(snapshots_iter)
