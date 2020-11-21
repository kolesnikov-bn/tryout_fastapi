from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


class Group(models.Model):
    name = fields.CharField(max_length=150, unique=True)
    parent: fields.ForeignKeyNullableRelation["Group"] = fields.ForeignKeyField(
        "models.Group", related_name="children", null=True
    )
    children: fields.ReverseRelation["Group"]
    products: fields.ReverseRelation["Product"]

    class PydanticMeta:
        allow_cycles = False
        exclude = ("children", "group", "products")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"


class Product(models.Model):
    name = fields.CharField(max_length=150)
    group = fields.ForeignKeyField("models.Group", related_name="products")


Tortoise.init_models(["src.product.models"], "models")
GroupPDModel = pydantic_model_creator(Group, name="GroupPDModel", exclude=("children",))
ProductPDModel = pydantic_model_creator(Product, name="ProductPDModel")
