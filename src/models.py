from tortoise import models, fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import SET_NULL


class User(models.Model):
    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    permissions: fields.ManyToManyRelation["UserGroupPermission"]

    def full_name(self) -> str:
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()

        return self.username

    class PydanticMeta:
        computed = ["full_name"]


class Group(models.Model):
    name = fields.CharField(max_length=150, unique=True)
    parent: fields.ForeignKeyNullableRelation["Group"] = fields.ForeignKeyField(
        "models.Group", related_name="children", null=True, on_delete=SET_NULL
    )
    permissions: fields.ManyToManyRelation["UserGroupPermission"]
    children: fields.ReverseRelation["Group"]

    class PydanticMeta:
        allow_cycles = False
        exclude = ("group", "products", "permissions")

    def __str__(self):
        return f"<{self.__class__.__name__}>: {self.name}"


class UserGroupPermission(models.Model):
    user = fields.ForeignKeyField("models.User", related_name="permissions")
    group = fields.ForeignKeyField("models.Group", related_name="permissions")
    permission = fields.ForeignKeyField("models.Permission", related_name="children")

    class Meta:
        table = "user_group_permission"


class Permission(models.Model):
    name = fields.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = fields.CharField(max_length=150)
    group = fields.ForeignKeyField("models.Group", related_name="products")


Tortoise.init_models(["src.models"], "models")

UserPDModel = pydantic_model_creator(User, name="User", exclude=("permissions",))
UserInPDModel = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True, exclude=("password",)
)
PermissionPDModel = pydantic_model_creator(Permission, name="permission")
GroupPDModel = pydantic_model_creator(
    Group, name="GroupPDModel", exclude=("permissions",)
)
ProductPDModel = pydantic_model_creator(Product, name="ProductPDModel")
