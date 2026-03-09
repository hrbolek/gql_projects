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
class FinanceTransferDBModel(BaseDBModel):
    __tablename__ = table_prefix_name + "finance_transfers"

    name: Mapped[str] = mapped_column(default=None, nullable=True)

    finance_source_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("finances", "id")),
        nullable=True,
        default=None,
        index=True,
    )

    # the real column in the DB
    finance_destination_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("finances", "id")),
        nullable=True,
        default=None,
        index=True,
    )

    startdate: Mapped[datetime.datetime] = mapped_column(
        default=None, 
        nullable=True,
        comment="Start date of the finance transfer",
        server_default=sqlalchemy.func.now()
    )
    amount: Mapped[float] = mapped_column(default=None, nullable=True)

    finance_source = relationship(
        "FinanceDBModel",
        uselist=False,
        primaryjoin="FinanceTransferDBModel.finance_source_id == FinanceDBModel.id",
    )

    finance_destination = relationship(
        "FinanceDBModel",
        uselist=False,
        primaryjoin="FinanceTransferDBModel.finance_destination_id == FinanceDBModel.id",
    )


