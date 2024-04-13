from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey
from .BaseModel import BaseModel
import sqlalchemy

class FinanceCategory(BaseModel):
    """
    Represents a category for financial information related to projects in the system.
    """
    __tablename__ = "projectfinancecategories"

    id = UUIDColumn()
    name = Column(String, comment="Name of the financial information category")
    name_en = Column(String, comment="English name of the financial information category")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the financial information category was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information category")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that determines access to the financial information category")
    user_id = UUIDFKey(nullable=True, comment="User ID associated with the financial information category")