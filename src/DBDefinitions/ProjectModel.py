from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from .BaseModel import BaseModel
import sqlalchemy
from sqlalchemy.orm import relationship

class ProjectModel(BaseModel):
     """
     Represents a project in the system.
     """
     __tablename__ = "projects"

     id = UUIDColumn()

     name = Column(String, comment="Name of the project")
     startdate = Column(DateTime, comment="Start date of the project")
     enddate = Column(DateTime, comment="End date of the project")
     valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")

     projecttype_id = Column(ForeignKey("projecttypes.id"), index=True, comment="Foreign key referencing the project type")
     projecttype = relationship("ProjectTypeModel", back_populates="projects")

     group_id = UUIDFKey(nullable=True)#Column(ForeignKey("groups.id"), index=True)
     #group = relationship("groupModel")

     created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the project was created")
     lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the project")
     createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
     changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
     rbacobject = UUIDFKey(nullable=True, comment="User or group ID that determines access to the proejct informatio")
     user_id = UUIDFKey(nullable=True, comment="User ID associated with the project information")