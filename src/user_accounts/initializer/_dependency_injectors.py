from user_accounts.application.user_service import UserService
from user_accounts.application.validator.user_validator import UserValidator
from user_accounts.infrastructure.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from user_accounts.application.error_code_generator.invalid_user_error_code_generator import \
    InvalidUserErrorCodeGenerator


def di_configurator(binder):
    """
    configures dependency injection.
    """
    binder.bind(UserService, UserService)
    binder.bind(SQLAlchemyUnitOfWork, SQLAlchemyUnitOfWork)
    binder.bind(InvalidUserErrorCodeGenerator, InvalidUserErrorCodeGenerator)
    binder.bind(UserValidator, UserValidator)
