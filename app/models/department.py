from tortoise import Model, fields

from models.formation import Formation


class Department(Model):

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=10)
    formations: fields.ManyToManyRelation[Formation] = fields.ManyToManyField("models.formation", through="...")
