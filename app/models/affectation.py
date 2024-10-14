from tortoise import Model, fields

from app.models.user import User
from app.models.module import Module

from . import course_type


class Affectation(Model):
    module_id: fields.ForeignKeyRelation[Module] = fields.ForeignKeyField(
        model_name="models.Module", related_name="id"
    )
    user_id: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", related_name="id"
    )
    affect_type = fields.CharEnumField(course_type)

    start = fields.DatetimeField(auto_now=False)
    end = fields.DatetimeField(auto_now=False)
