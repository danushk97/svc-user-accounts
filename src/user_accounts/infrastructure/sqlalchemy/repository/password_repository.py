"""
This modle holds the repository class for Password.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

from user_accounts.infrastructure._repository.password_repository import AbstractPasswordRepository
from user_accounts.infrastructure.sqlalchemy.models.password import PasswordModel
from user_accounts.infrastructure.sqlalchemy.models.user import UserModel
from user_accounts.common.constants import Constants
from user_accounts.common.exception import RepositoryException
from apputils.error_handler import ErrorHandler


class PasswordRepository(AbstractPasswordRepository):
    """
    Contains helper functions to query user's password info.
    """

    def __init__(self, session):
        """
        Instantiates the class.
        """
        self._session = session

    @ErrorHandler.handle_exception([SQLAlchemyError], RepositoryException)
    def add(self, entity) -> None:
        self.session.add(entity)

    @ErrorHandler.handle_exception([SQLAlchemyError], RepositoryException)
    def update_password_by_user_id(self, user_id: str, password_hash: str) -> int:
        """
        Upates the password for the user_id.

        Args:
            user_id (str): User ID.
            password_hash (str): Encrypted password.

        Returns:
            row_affected (int): Number of rows affected.

        Raises:
            RepositoryException: On SQLAlachemyError
        """
        attr = {Constants.CREDENTIAL: password_hash}
        row_affected = self._session\
                            .query(PasswordModel)\
                            .filter(PasswordModel.user_id == user_id)\
                            .update({Constants.ATTR: attr})

        return row_affected

    @ErrorHandler.handle_exception([SQLAlchemyError], RepositoryException)
    def get_password_hash_by_email(self, email: str) -> tuple:
        """
        Fetches password hash for the user_id.

        Args:
            email (str): User email id.

        Returns:
            user_id (str): User id, password_hash (str): Password Hash.

        Raises:
            RepositoryException: On SQLAlachemyError
        """
        password = self._session\
                       .query(PasswordModel)\
                       .join(UserModel, and_(PasswordModel.user_id == UserModel.stable_id))\
                       .filter(UserModel.attr[Constants.EMAIL].astext == email)\
                       .one_or_none()

        if password:
            password_hash = password.attr[Constants.CREDENTIAL]

            return password.user_id, password_hash