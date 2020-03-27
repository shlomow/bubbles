import pathlib


class Context:
    work_path = '/tmp/bubbles'

    def __init__(self, path=None):
        if path is None:
            path = Context.work_path
        self.work_path = pathlib.Path(path)
        self.work_path.mkdir(parents=True, exist_ok=True)

    def path(self, filename):
        return self.work_path / filename
