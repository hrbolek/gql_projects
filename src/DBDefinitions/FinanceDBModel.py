import typing
import datetime
import dataclasses
import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import relationship

from .BaseDBModel import BaseDBModel, IDType, table_prefix_name, fk_name

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
class FinanceDBModel(BaseDBModel):
    __tablename__ = table_prefix_name + "finances"

    path_attribute_name = "path"
    parent_attribute_name = "masterfinance"
    parent_id_attribute_name = "masterfinance_id"
    children_attribute_name = "subfinances"

    # Materialized path technique
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique"
    )

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)

    value: Mapped[float] = mapped_column(default=None, nullable=True)

    finance_type_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("finance_types", "id")),
        nullable=True,
        default=None,
        index=True,
    )

    # the real column in the DB
    masterfinance_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("finances", "id")),
        nullable=True,
        default=None,
        index=True,
    )


    masterfinance = relationship(
        "FinanceDBModel",
        viewonly=True, 
        remote_side="FinanceDBModel.id",
        uselist=False,
        back_populates="subfinances",
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html

    subfinances = relationship(
        "FinanceDBModel", 
        back_populates="masterfinance",
        uselist=True,
        init=True,
        cascade="save-update"
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html
    # https://docs.sqlalchemy.org/en/20/_modules/examples/materialized_paths/materialized_paths.html

