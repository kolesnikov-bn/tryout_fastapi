from __future__ import annotations

from tortoise import fields, Model
from tortoise.contrib.pydantic import pydantic_model_creator


class Group(Model):
    name = fields.CharField(max_length=150, unique=True)
    parent: fields.ForeignKeyNullableRelation[Group] = fields.ForeignKeyField(
        "models.Group", related_name="children", null=True
    )
    children: fields.ReverseRelation[Group]

    class PydanticMeta:
        allow_cycles = True
        max_recursion = 4

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"


class Product(Model):
    name = fields.CharField(max_length=150)
    id_group = fields.ForeignKeyField("models.Group", related_name="group")


GroupPDModel = pydantic_model_creator(Group, name="GroupPDModel")
