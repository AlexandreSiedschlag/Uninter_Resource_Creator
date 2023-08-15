class Resource(Model):
    id = types.Int()
    username = types.String()
    fullname = types.String()
    email = types.String()
    password_hash = types.String()
    superuser = types.Boolean()
    enabled = types.Boolean()
