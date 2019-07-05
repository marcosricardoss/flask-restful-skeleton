"""The model layer."""


from .models import User
from .user_repository import UserRepository

__all__ = ["User", "UserRepository"]
