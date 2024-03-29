from logging import getLogger
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    func,
    ForeignKey,
    Integer,
    Table
)
from sqlalchemy.dialects.postgresql import UUID, BYTEA, BOOLEAN, VARCHAR
from sqlalchemy.orm import registry, relationship

from useraccounts.domain import models


_logger = getLogger(__name__)
_mapper_registry = registry()


accounts = Table(
    "accounts",
    _mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("stable_id", UUID, nullable=False, unique=True, server_default=str(uuid4())),
    Column("name", VARCHAR(128), nullable=False),
    Column("dob", DateTime, nullable=False),
    Column("username", VARCHAR(50), nullable=False, unique=True),
    Column("phone_number", Integer, nullable=False, unique=True),
    Column("email", VARCHAR(128), nullable=False, unique=True),
    Column("isemail_verified", BOOLEAN, nullable=False, server_default='false'),
    Column("isphone_number_verified", BOOLEAN, nullable=False, server_default='false'),
    Column("is_active", BOOLEAN, nullable=False, server_default='true'),
    Column("created_by", UUID),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("last_updated_by", UUID),
    Column("last_updated_at", DateTime)
)


passwords = Table(
    "passwords",
    _mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", ForeignKey("accounts.username")),
    Column("hash", BYTEA, nullable=False),
    Column("is_active", BOOLEAN, nullable=False, server_default='true'),
    Column("created_by", ForeignKey("accounts.id")),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("last_updated_by", ForeignKey("accounts.id"), ),
    Column("last_updated_at", DateTime, server_default=func.now())
)


def start_orm_mappers(is_create_tables=False, engine=None):
    _logger.info("Starting orm mappers...")
    _mapper_registry.map_imperatively(
        models.Account,
        accounts,
        properties={
            "_password": relationship(
                models.Password,
                foreign_keys=[passwords.c.username],
                uselist=False,
                back_populates="user"
            )
        }
    )
    _mapper_registry.map_imperatively(
        models.Password,
        passwords,
        properties={
            "created_by_user": relationship(
                models.Account,
                foreign_keys=[passwords.c.created_by]
            ),
            "updated_by_user": relationship(
                models.Account,
                foreign_keys=[passwords.c.last_updated_by]
            ),
            "user": relationship(
                models.Account,
                foreign_keys=[passwords.c.username],
                back_populates="_password",
                viewonly=True
            )
        }
    )
    _logger.info("Successfully mapped orm's.")

    if is_create_tables:
        _mapper_registry.metadata.create_all(engine)
