from fastapi import HTTPException
from starlette import status
from tortoise.query_utils import Q

from src.constants import GroupId
from src.models import (
    Permission,
    UserGroupPermission,
    User,
    Group,
    Product,
)
from src.user.schemas import UserSchema

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied"
)


async def is_group_allowed(group_id: GroupId, user: UserSchema) -> bool:
    if user.permissions:
        allowed_groups_id = [x.group.id for x in user.permissions]
        derived_groups_id = await Group.filter(
            Q(parent_id__in=allowed_groups_id) | Q(id__in=allowed_groups_id)
        ).values_list("id", flat=True)

        if group_id not in derived_groups_id:
            raise forbidden_exception
    else:
        raise forbidden_exception

    return True
