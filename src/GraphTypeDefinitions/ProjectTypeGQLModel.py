import uuid
import strawberry as strawberryA
from typing import List, Annotated, Optional, Union
from contextlib import asynccontextmanager
import datetime
from .BaseGQLModel import BaseGQLModel
import strawberry
from src.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

from src.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

from src.GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject,
    resolve_valid
)

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]
ProjectCategoryGQLModel = Annotated["ProjectCategoryGQLModel",strawberryA.lazy(".ProjectCategoryGQLModel")]



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a project types"""
)
class ProjectTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).projecttypes

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    
    @strawberryA.field(description="""List of projects, related to project type""", permission_classes=[OnlyForAuthentized()])
    async def projects(self, info: strawberryA.types.Info) -> List["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projecttypes
        result = await loader.filter_by(id = self.id)
        return result
        
    @strawberryA.field(description="""Category ID of project, related to project""", permission_classes=[OnlyForAuthentized()])
    async def category(self, info: strawberryA.types.Info) -> Optional ["ProjectCategoryGQLModel"]:
        from .ProjectCategoryGQLModel import ProjectCategoryGQLModel  # Import here to avoid circular dependency
        result = await ProjectCategoryGQLModel.resolve_reference(info, self.category_id)
        return result

    # startdate = resolve_startdate
    # enddate = resolve_enddate
    # accesslevel = resolve_accesslevel

###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class ProjectTypeWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str
    valid: bool

@strawberryA.field(description="""Returns a list of project types""", permission_classes=[OnlyForAuthentized()])
async def project_type_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[ProjectTypeWhereFilter] = None
) -> List[ProjectTypeGQLModel]:
    loader = getLoadersFromInfo(info).projecttypes
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

project_type_by_id = createRootResolver_by_id(ProjectTypeGQLModel, description="Returns project type by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of a project type used for creation")
class ProjectTypeInsertGQLModel:
    category_id: uuid.UUID = strawberryA.field(description="The ID of the project category")
    name: str = strawberryA.field(description="Name/label of the project type")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the project type data is valid or not", default=True)
    name_en: str = strawberryA.field(description="Name/label of the finance type in English", default=None)
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the project type", default=None)
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None

@strawberryA.input(description="Definition of a project type used for update")
class ProjectTypeUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project type")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the projcet type data is valid or not", default=None)
    name: Optional[str] = strawberryA.field(description="Updated name/label of the project type", default=None)
    name_en: Optional[str] = strawberryA.field(description="Updated name/label of the project in English", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberryA.type(description="Result of a mutation for project type")
class ProjectTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project type", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project type", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectTypeGQLModel, None]:
        result = await ProjectTypeGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new project type.", permission_classes=[OnlyForAuthentized()])
async def project_type_insert(self, info: strawberryA.types.Info, project: ProjectTypeInsertGQLModel) -> ProjectTypeResultGQLModel:
    user = getUserFromInfo(info)
    project.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projecttypes
    row = await loader.insert(project)
    result = ProjectTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project type.", permission_classes=[OnlyForAuthentized()])
async def project_type_update(self, info: strawberryA.types.Info, project: ProjectTypeUpdateGQLModel) -> ProjectTypeResultGQLModel:
    user = getUserFromInfo(info)
    project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projecttypes
    row = await loader.update(project)
    result = ProjectTypeResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    result.msg = "ok" if (row is not None) else "fail"
    return result