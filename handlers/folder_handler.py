import os
import shutil
from handlers.path_handler import PathHandler

class FolderHandler:
    def __init__(self):
        self.path = PathHandler()
        self.default_path = self.path.legacy

    def copy_tree(self, destination):
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree(self.default_path, destination)

    def rename_folder(self, path, new_path):
        os.rename(path, new_path)

