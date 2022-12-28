"""
This module holds the class which defines password entity.
"""

from datetime import datetime
from uuid import uuid4
import bcrypt
import logging

from useraccounts.domain import models
from useraccounts.domain.models.base_model import BaseModel


logger = logging.getLogger(__name__)


class Password(BaseModel):
    """
    Password is a value object.

    Attributes:
        user_id (int): User ID.
        password_hash (str): Encrypted form of password_str.
    """
    def __init__(
        self,
        password_hash: bytes,
        active_flag: bool = True,
        created_at: datetime = None,
        created_by: str = None,
        updated_by: str = None,
        updated_at: datetime = None
    ):
        """
        Instantiates class.
        """
        super().__init__(
            active_flag,
            created_by,
            created_at,
            updated_by,
            updated_at
        )
        self.stable_id = str(uuid4())
        self.hash = password_hash
        self.created_by_user = None
        self.updated_by_user = None

    @staticmethod
    def do_match(password: bytes, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password, hashed_password)
