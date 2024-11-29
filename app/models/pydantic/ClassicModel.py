from pydantic import BaseModel


class ClassicModel(BaseModel):
    name: str
    description: str
