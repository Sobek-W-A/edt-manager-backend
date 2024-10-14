from tortoise import Model, fields

class Permission(Model):

    affect_user = fields.BooleanField()