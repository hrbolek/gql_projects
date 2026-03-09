
import datetime
import typing
import sqlalchemy

from typing import Optional
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
class ProjectTypeDBModel(BaseDBModel):
    __tablename__ = table_prefix_name + "project_types"

    path_attribute_name = "path"
    parent_attribute_name = "mastertype"
    parent_id_attribute_name = "mastertype_id"
    children_attribute_name = "subtypes"

    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique, not implemented"
    )

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)

    mastertype_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("project_types", "id")),
        nullable=True,
        default=None,
        index=True,
    )

    mastertype = relationship(
        "ProjectTypeDBModel",
        viewonly=True, 
        remote_side="ProjectTypeDBModel.id",
        uselist=False,
        back_populates="subtypes",
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html

    subtypes = relationship(
        "ProjectTypeDBModel", 
        back_populates="mastertype",
        uselist=True,
        init=True,
        cascade="save-update"
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html
    # https://docs.sqlalchemy.org/en/20/_modules/examples/materialized_paths/materialized_paths.html

