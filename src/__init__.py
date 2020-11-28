import sys

from fastapi import HTTPException
from loguru import logger
from starlette import status

from src.constants import GroupId
from src.user.schemas import UserSchema

logger.add(
    sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)
forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied"
)


async def is_group_allowed(group_id: GroupId, user: UserSchema) -> bool:
    if user.permissions:
        allowed_groups_id = [x.group.id for x in user.permissions]
        if group_id not in allowed_groups_id:
            raise forbidden_exception
    else:
        raise forbidden_exception

    return True
