from tortoise import Model, fields

from models.permission import Permission

class Role(Model):
    name = fields.CharField(max_length=10)
    perms: list[Permission]
    credits: int
