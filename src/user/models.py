from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)

    def full_name(self) -> str:
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()

        return self.username

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password"]


UserPDModel = pydantic_model_creator(User, name="User")
UserInPDModel = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
