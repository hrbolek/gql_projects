import uuid
import datetime
import sqlalchemy
from uuid6 import uuid7

# from typing import Optional
# from sqlmodel import SQLModel, Field
# from pydantic import ConfigDict

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column

IDType = uuid.UUID
def uuid7_factory() -> IDType:
    return uuid7()

table_prefix_name = "gql_project_"
table_prefix_name = ""

# def UUIDColumn(**kwargs):
#     return Field(
#         default_factory=uuid7_factory,
#         primary_key=True,
#         index=True,
#         description="primary key",
#         **kwargs
#     )

def fk_name(table_name: str, column_name: str = "id"):
    return (f"{table_prefix_name}{table_name}.{column_name}")

# def UUIDFKey(description: str | None = None, foreign_key: str | None = None, **kwargs):
#     return Field(
#         default=None,
#         # foreign_key=foreign_key,
#         index=True,
#         nullable=True,
#         description=description or "foreign key",
#         **kwargs
#     )


def UUIDFKey(ForeignKeyArg=None, **kwargs):
    newkwargs = {
        **kwargs,
        "index": True, 
        "primary_key": False, 
        "default": None,
        "nullable": True,
        "comment": "foreign key"
    }
    return mapped_column(**newkwargs)

def UUIDColumn(**kwargs):
    newkwargs = {
        **kwargs,
        "index": True, 
        "primary_key": True, 
        "default_factory": uuid7_factory, 
        "comment": "primary key"
    }
    return mapped_column(**newkwargs)

# class BaseDBModel(SQLModel):
#     model_config = ConfigDict(ignored_types=(sqlalchemy.ext.hybrid.hybrid_property,))

#     id: IDType = UUIDColumn()

#     created: Optional[datetime.datetime] = Field(
#         default=None,
#         nullable=True,
#         sa_column_kwargs={
#             "server_default": sqlalchemy.sql.func.now(),
#             "comment": "date time of creation"
#         }
#     )

#     lastchange: Optional[datetime.datetime] = Field(
#         default=None,
#         nullable=True,
#         sa_column_kwargs={
#             "server_default": sqlalchemy.sql.func.now(),
#             "onupdate": sqlalchemy.sql.func.now(),
#             "comment": "date time stamp"
#         }
#     )

#     createdby_id: Optional[IDType] = UUIDFKey(foreign_key="users.id")
#     changedby_id: Optional[IDType] = UUIDFKey(foreign_key="users.id")
#     rbacobject_id: Optional[IDType] = UUIDFKey()


IDType = uuid.UUID

class BaseDBModel(MappedAsDataclass, DeclarativeBase):
    id: Mapped[IDType] = UUIDColumn(index=True, primary_key=True, default_factory=uuid7_factory, comment="primary key")

    created: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, server_default=sqlalchemy.sql.func.now(), comment="date time of creation")
    lastchange: Mapped[datetime.datetime] = mapped_column(
        default=None, 
        nullable=True, 
        server_default=sqlalchemy.sql.func.now(), 
        onupdate=sqlalchemy.sql.func.now(),
        comment="date time stamp"
    )

    createdby_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), comment="id of user who created this entity")
    changedby_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), comment="id of user who changed this entity")
    rbacobject_id: Mapped[IDType] = UUIDFKey(comment="id rbacobject")
###