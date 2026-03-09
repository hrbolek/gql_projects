import sqlalchemy
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseDBModel import BaseDBModel, IDType, table_prefix_name, fk_name



class ProjectDependencyDBModel(BaseDBModel):
    """
    Represents a link between projects in the system.
    """
    __tablename__ = table_prefix_name + "project_dependencies"

    previous_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("projects", "id")),
        nullable=True,
        default=None,
        index=True,
        comment="Foreign key referencing the previous project"
    )

    next_id: Mapped[IDType] = mapped_column(
        ForeignKey(fk_name("projects", "id")),
        nullable=True,
        default=None,
        index=True,
        comment="Foreign key referencing the next project"
    )