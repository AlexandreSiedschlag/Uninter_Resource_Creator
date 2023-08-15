from handlers.folder_handler import FolderHandler
from handlers.file_handler import FileHandler
from handlers.path_handler import PathHandler
from definitions import definitions
import os

class ResourceCreator:
    def __init__(
            self,
            file=FileHandler(definitions['resource']),
            folder=FolderHandler(),
            path=PathHandler()):
        self.folder = folder
        self.file = file
        self.path = path

    def copy_tree(self):
        self.folder.copy_tree(self.path.new_legacy)

    def search_files(self, pattern):
        matching_files = []
        for root, dirs, files in os.walk(self.path.new_legacy):
            for filename in files:
                if filename.endswith(pattern):
                    matching_files.append(os.path.join(root, filename))

        return matching_files

    def replace_content(self, resource_name):
        pattern = resource_name.lower()
        file_path = self.search_files(pattern)[0]
        self.file.rrw(file_path)

    def rename_folder(self, path):
        self.folder.rename_folder(path, self.path.rename_folder(path))

    def rename_api_route(self, resource_name):
        pattern = resource_name.lower()
        file_path = self.search_files(pattern)[0]
        self.file.replace_api_route(file_path)

    def create_entities(self):
        self.file.create_entities(self.path.entities_path())

    def create_models(self):
        self.file.create_models(self.path.models_path())
