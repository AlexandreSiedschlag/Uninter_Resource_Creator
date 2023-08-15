from definitions import definitions
from pathlib import PurePosixPath, Path, PurePath


class PathHandler:
    def __init__(self):
        self.root_dir = PurePosixPath(definitions['root_dir'])
        self.legacy = self.root_dir.joinpath('legacies', 'legacy')
        self.new_legacy = self.root_dir.joinpath('legacies','new_legacy')
        self.resource = definitions['resource']

        if self.resource.endswith('s'):
            raise Exception('Cant end with letter s')

    def rename_folder(self, path):
        old_path = PurePath(path).parent
        return old_path.joinpath(self.resource.lower() + 's')

    def entities_path(self):
        return Path.joinpath(self.new_legacy, 'backend', 'core', 'entities.py')

    def models_path(self):
        return Path.joinpath(self.new_legacy, 'backend', 'core', 'models.py')







