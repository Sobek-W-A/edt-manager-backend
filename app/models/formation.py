from tortoise import Model

from models.module import Module

class Formation(Model):
    formation_id: int
    name: str
    modules: list[Module]
