"""
This moudule acts as the service layer which helps to update user password.
"""

import jwt
from injector import inject
from apputils.error_handler import ErrorHandler
from apputils.status_code import StatusCode

from user_accounts.infrastructure.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from user_accounts.application._service import Service
from user_accounts.common.constants import Constants
from user_accounts.common.exception import InvalidCredetialException, PasswordServiceException
from user_accounts.common.exception import InvalidRequestException
from user_accounts.common.exception import InvalidPasswordException
from user_accounts.common.exception import RepositoryException
from user_accounts.common.error_codes.invalid_user_error_codes import InvalidUserErrorCodes
from user_accounts.domain.value_object.password import Password


class PasswordService(Service):
    """
    Holds business usecase/logic which are related to password creation/updation.

    Attributes:
        postgres_unit_of_work (SQLAlchemyUnitOfWork): Helps communicating with
        the postgres database.
    """
    @inject
    def __init__(self, unit_of_work: SQLAlchemyUnitOfWork):
        """
        Instantiates the class.
        """
        self.unit_of_work = unit_of_work

    @ErrorHandler.handle_exception([RepositoryException], PasswordServiceException)
    def update_password(self, user_id: str, password: str) -> dict:
        """
        Update Password.

        Args:
            update_info (dict): Should hold the password and user_id.
        """
        self._check_user_id(user_id)
        password = self._get_password_object(password)

        if not password.is_valid():
            raise InvalidPasswordException([
                InvalidUserErrorCodes.INVALID_PASSWORD_LENGTH
            ])

        self.initiate_db_transaction(
            self._update_password, user_id, password.hash
        )

    @ErrorHandler.handle_exception([RepositoryException], PasswordServiceException)
    def validate_credential(self, email: str, password: str) -> None:
        """
        Validates credential and returns a JWT if the credential is valid.

        Args:
            email (str): User email id.
            password (str): Password.

        Returns:
            jwt_token ()
        """
        self._check_email(email)
        user_id, credential = self.initiate_db_transaction(self._get_password_hash, email)

        if not Password.do_match(password.encode(), credential):
            raise InvalidCredetialException()

        # TODO: Need to move secret to env_var and to update the payload
        jwt_token = jwt.encode({Constants.USER_ID: user_id}, 'secret')

        return jwt_token

    def _get_password_hash(self, unit_of_work: SQLAlchemyUnitOfWork, email: str) -> tuple:
        """
        Helps to get password hash of the under the requested user_id.

        Args:
            unit_of_work (SQLAlchemyUnitOfWork)
            email (str): User email id.

        Returns:
            user_password (tuple): Contains the user_id at place 0 and
            password_hash at place 1

        Raises:
            PasswordServiceException: On no data found.
        """
        repository = unit_of_work.password_repository()
        user_password = repository.get_password_hash_by_email(email)

        if not user_password:
            raise PasswordServiceException([
                InvalidUserErrorCodes.NO_USER_FOUND
            ], StatusCode.BAD_REQUEST)

        return user_password[0], user_password[1]


    def _update_password(self, unit_of_work: SQLAlchemyUnitOfWork, user_id: str, password_hash: str):
        """
        Helps to update password.

        Args:
            unit_of_work (SQLAlchemyUnitOfWork): An interface to communicate with
            Database.
            user_id (str): User ID.
            password_hash (str): Hashed password string.

        Raises:
            PasswordServiceException: On no record got updated.
        """
        repository = unit_of_work.password_repository()
        affected_rows = repository.update_password_by_user_id(user_id, password_hash)

        if not affected_rows:
            raise PasswordServiceException([
                InvalidUserErrorCodes.NO_USER_FOUND
            ], StatusCode.BAD_REQUEST)

        unit_of_work.commit()

    def _get_password_object(self, password: str) -> Password:
        return Password(password)

    def _check_email(self, email: str):
        if not email:
            raise InvalidRequestException([
                InvalidUserErrorCodes.INVALID_EMAIL
            ])

    def _check_user_id(self, user_id: str):
        if not user_id:
            raise InvalidRequestException([
                InvalidUserErrorCodes.INVALID_USER_ID
            ])
