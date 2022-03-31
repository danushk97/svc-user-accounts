import pytest

from user_accounts.infrastructure._repository.password_repository import AbstractPasswordRepository


@pytest.fixture
def password_repo():
    class PasswordRepo(AbstractPasswordRepository):
        def add(self, entity):
            return super().add(entity)

        def update_password_by_user_id(self, user_id: str, password_hash: str) -> int:
            return super().update_password_by_user_id(user_id, password_hash)

    return PasswordRepo()


def test_update_password_by_user_id_rasies_not_implemented_error(password_repo: AbstractPasswordRepository):
    with pytest.raises(NotImplementedError):
        password_repo.update_password_by_user_id('key', 'value')
