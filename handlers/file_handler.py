import os
from pathlib import Path
import re
from definitions import definitions

class FileHandler:
    def __init__(self, resource_name):
        self.classes_base_name = 'Resources'
        self.class_base_name = 'Resource'
        self.variables_base_name = 'resources'
        self.variable_base_name = 'resource'
        self.new_classes_base_name = ''
        self.new_class_base_name = ''
        self.new_variables_base_name = ''
        self.new_variable_base_name = ''

        if resource_name.endswith('s'):
            resource_name = resource_name[:-1]

        if '_' in resource_name:
            self.new_variables_base_name += resource_name + 's'
            self.new_variable_base_name += resource_name

            for name in resource_name.split('_'):
                self.new_classes_base_name += name.lower().capitalize()
                self.new_class_base_name += name.lower().capitalize()
        else:
            self.new_classes_base_name = self.new_classes_base_name.lower().capitalize()
            self.new_variable_base_name = resource_name.lower()

        if not self.new_classes_base_name.endswith('s'):
                self.new_classes_base_name += 's'

        if not self.new_variables_base_name.endswith('s'):
                self.new_variables_base_name += 's'

    def reader1(self, path):
        data = ''
        with open(Path(path),'r') as f:
            data = f.read()
            f.seek(0)
        return data

    def replace(self, data, order_list=['Resources', 'Resource', 'resources', 'resource']):
        for item in order_list:
            if item == 'Resources':
                data = re.sub(self.classes_base_name, self.new_classes_base_name, data)
            elif item == 'Recource':
                data = re.sub(self.class_base_name, self.new_class_base_name, data)
            elif item == 'resources':
                data = re.sub(self.variables_base_name, self.new_variables_base_name, data)
            elif item == 'resource':
                data = re.sub(self.variable_base_name, self.new_variable_base_name, data)
        return data

    def write_file(self, path):
        with open(Path(path), 'w+') as new:
            new.write(self.replace(self.reader1(path)))
            new.truncate()

    def rrw(self, path, order_list=['Resources', 'Resource', 'resources', 'resource']):
        with open(path, 'r') as file :
            filedata = file.read()

        for item in order_list:
            if item == 'Resources':
                filedata = filedata.replace(self.classes_base_name, self.new_classes_base_name)
            elif item == 'Resource':
                filedata = filedata.replace(self.class_base_name, self.new_class_base_name)
            elif item == 'resources':
                filedata = filedata.replace(self.variables_base_name, self.new_variables_base_name)
            elif item == 'resource':
                filedata = filedata.replace(self.variable_base_name, self.new_variable_base_name)

        with open(path, 'w') as file:
            file.write(filedata)

    def replace_api_route(self, path):
        patterns = [f'-{self.new_variables_base_name}', f'/{self.new_variables_base_name}']
        with open(path, 'r') as file:
            filedata = file.read()

        filedata = filedata.replace(patterns[0], f"-{self.new_variables_base_name.replace('_', '-')}")
        filedata = filedata.replace(patterns[1], fr"/{self.new_variables_base_name.replace('_', '-')}")


        with open(path, 'w') as file:
            file.write(filedata)

    def create_entities(self, path):
        sql_string = definitions['infra']['pkgs']['sql_string']
        with open(path, "w") as f:
            f.write('from hadron import Model, types\n')
            f.write('\n')
            f.write(f"class {self.new_class_base_name}(Model):\n")

            for line in sql_string.splitlines():
                regex = r"`(\w+)`\s+(\w+)\((\d+)\)\s*(\w+)?"
                matchs = re.findall(regex, line)

                for match in matchs:
                    if match:
                        field_name = match[0]
                        field_type = match[1]
                        field_quantity = match[2]
                        if 'NOT NULL' in line:
                            nullable = False
                        elif 'NULL' in line:
                            nullable = True
                        else:
                            nullable = False

                        if field_type == "int":
                            field_type = 'Int'
                        elif field_type == "varchar":
                            field_type = 'String'
                        elif field_type == "tinyint":
                            field_type = 'Boolean'

                        if nullable:
                            f.write(f"    {field_name} = types.{field_type}(required=False)\n")
                        else:
                            f.write(f"    {field_name} = types.{field_type}()\n")

    def create_models(self, path):
        sql_string = definitions['infra']['pkgs']['sql_string']
        unique_keys = []
        with open(path, "w") as f:
            for line in sql_string.splitlines():
                if 'UNIQUE KEY' in line:
                    regex = r"\(`([\w-]+)`\)"
                    found = re.findall(regex, line)
                    unique_keys.append(found[0])

        print(unique_keys, type(unique_keys))
        with open(path, "w") as f:
            f.write('import sqlalchemy as sa\n')
            f.write('from core.deps import SQLBase\n')
            f.write('\n')
            f.write(f"class SQL{self.new_class_base_name}(SQLBase):\n")
            table_name = sql_string.splitlines()[1].split('`')[1]
            print(table_name)

            for line in sql_string.splitlines():
                regex = r"`(\w+)`\s+(\w+)\((\d+)\)\s*(\w+)?"
                matchs = re.findall(regex, line)

                for match in matchs:
                    if match:
                        field_name = match[0]
                        field_type = match[1]
                        field_quantity = match[2]
                        if 'NOT NULL' in line:
                            nullable = False
                        elif 'NULL' in line:
                            nullable = True
                        else:
                            nullable = False

                        if field_type == "int":
                            field_type = 'Integer'
                        elif field_type == "varchar":
                            field_type = 'String'
                        elif field_type == "tinyint":
                            field_type = 'Boolean'
                        elif field_type == "text":
                            field_type = 'Text'
                        elif field_type == "datetime":
                            field_type = 'DateTime'
                        elif field_type == "date":
                            field_type = 'Date'
                        elif field_type == "time":
                            field_type = 'Time'
                        print(field_type)
                        substring = f"    {field_name} = sa.Column('{field_name}',sa.{field_type})"

                        if 'AUTO_INCREMENT' in line:
                            substring = substring[:-1] + ',' + 'primary_key=True' + ')'

                        if field_type == 'String':
                            substring = substring[:-1] + '(' + f'{field_quantity}' + '))'

                        if field_name in unique_keys:
                            substring = substring[:-1] + ',' + 'unique=True' + ')'

                        if nullable:
                            substring = substring[:-1] + ',' + 'nullable=True' + ')'


                        substring += '\n'
                        f.write(substring)
