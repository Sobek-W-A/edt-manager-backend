from tortoise import Model
from models import course_type


class Module(Model):
    module_id: int
    name: str
    hours: dict[course_type, int]
