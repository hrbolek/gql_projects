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
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .BaseDBModel import BaseDBModel, IDType, table_prefix_name, fk_name

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
class ProjectDBModel(BaseDBModel):
    __tablename__ = table_prefix_name + "projects"

    path_attribute_name = "path"
    parent_attribute_name = "masterproject"
    parent_id_attribute_name = "masterproject_id"
    children_attribute_name = "subprojects"

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
    done: Mapped[bool] = mapped_column(default=None, nullable=True)
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)

    @hybrid_property
    def duration(self):
        return self.enddate - self.startdate

    @hybrid_property
    def overdued(self):
        if self.done:
            return False
        if self.enddate:
            return datetime.datetime.now() > self.enddate
        return None
    
    @overdued.expression
    def overdued(cls):        
        return sqlalchemy.case(
            [
                (cls.done == True, False),
                (cls.enddate != None, sqlalchemy.func.now() > cls.enddate)
            ],
            else_=None
        )

    project_type_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("project_types", "id")),
        nullable=True,
        default=None,
        index=True,
    )

    # the real column in the DB
    masterproject_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("projects", "id")),
        nullable=True,
        default=None,
        index=True,
    )


    masterproject = relationship(
        "ProjectDBModel",
        viewonly=True, 
        remote_side="ProjectDBModel.id",
        uselist=False,
        back_populates="subprojects",
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html

    subprojects = relationship(
        "ProjectDBModel", 
        back_populates="masterproject",
        uselist=True,
        init=True,
        cascade="save-update"
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html
    # https://docs.sqlalchemy.org/en/20/_modules/examples/materialized_paths/materialized_paths.html

