from tortoise import Model, fields


class User(Model):

    id = fields.IntField(primary_key=True)
    first_name = fields.CharField(max_length=10)
    last_name = fields.CharField(max_length=10)

    # status: Role
    # affectations: list[Affectation]
