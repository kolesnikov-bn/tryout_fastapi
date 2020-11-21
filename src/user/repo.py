from src.repositories import DBRepo
from src.user.models import User, UserPDModel


class UserRepo(DBRepo):
    model = User
    get_schema = UserPDModel


user_repo = UserRepo()
