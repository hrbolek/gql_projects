from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from .BaseModel import BaseModel
import sqlalchemy
from sqlalchemy.orm import relationship

class FinanceModel(BaseModel):
    """
    Represents financial information related to projects in the system.
    """
    __tablename__ = "projectfinances"

    id = UUIDColumn()
    name = Column(String, comment="Name of the financial information")
    amount = Column(sqlalchemy.types.DECIMAL(precision=13, scale=3), comment="Amount of the financial information")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information")
    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")

    project_id = Column(ForeignKey("projects.id"), index=True, comment="Foreign key referencing the associated project")

    financetype_id = Column(ForeignKey("projectfinancetypes.id"), index=True, comment="Foreign key referencing the financial information type")
    financetype = relationship("FinanceTypeModel", back_populates="finances")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the financial information was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that determines access to the financial information")
    user_id = UUIDFKey(nullable=True, comment="User ID associated with the financial information")