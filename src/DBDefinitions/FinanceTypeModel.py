from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from .BaseModel import BaseModel
import sqlalchemy
from sqlalchemy.orm import relationship

class FinanceTypeModel(BaseModel):
    """
    Represents a type of financial information related to projects in the system.
    """
    __tablename__ = "projectfinancetypes"

    id = UUIDColumn()
    name = Column(String, comment="Name of the financial information type")
    name_en = Column(String, comment="English name of the financial information type")
    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")

    finances = relationship("FinanceModel", back_populates="financetype")
    category_id = Column(ForeignKey("projectfinancecategories.id"), index=True, nullable=True, comment="Foreign key referencing the project category")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the financial information type was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information type")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that determines access to the financial informatio type")
    user_id = UUIDFKey(nullable=True, comment="User ID associated with the financial information type")