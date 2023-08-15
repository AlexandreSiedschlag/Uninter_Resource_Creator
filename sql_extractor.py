import re

class Resource:
    class types:
        @staticmethod
        def Int():
            return "int"

        @staticmethod
        def String():
            return "varchar"

        @staticmethod
        def Boolean():
            return "tinyint"


with open("teste.py", "w") as f:
    f.write("class Resource(Model):\n")
    fields = re.findall("`([a-z_]+)`\s+([a-z]+)\(", sql_string, re.IGNORECASE)
    for field in fields:
        name = field[0]
        field_type = field[1]
        if field_type == "int":
            f.write(f"    {name} = types.Int()\n")
        elif field_type == "varchar":
            f.write(f"    {name} = types.String()\n")
        elif field_type == "tinyint":
            f.write(f"    {name} = types.Boolean()\n")
