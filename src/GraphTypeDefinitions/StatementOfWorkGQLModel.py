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
    resolve_created,
    resolve_lastchange,
    resolve_startdate,
    resolve_enddate,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject,
    resolve_valid
)

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".externals")]

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a SOW"""
)
class StatementOfWorkGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).statementofwork

    id = resolve_id
    lastchange = resolve_lastchange
    startdate = resolve_startdate
    enddate = resolve_enddate

    created = resolve_created
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    
   #project_id
    @strawberryA.field(description="""Project of statement of work""", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Optional ["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projects
        result = await loader.load(self.project_id)
        return result
    
    #event_id
    @strawberry.field(description="""Event, related to a statement of work""", permission_classes=[OnlyForAuthentized()])
    def event(self) -> Union["EventGQLModel", None]:
        from .externals import EventGQLModel
        return EventGQLModel(id=self.event_id)
    
###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class StatementOfWorkWhereFilter:
    id: uuid.UUID
    value: str
    valid: bool

@strawberryA.field(description="""Returns a list of statement of work""", permission_classes=[OnlyForAuthentized()])
async def statement_of_work_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[StatementOfWorkWhereFilter] = None
) -> List[StatementOfWorkGQLModel]:
    loader = getLoadersFromInfo(info).statementofwork
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

statement_of_work_by_id = createRootResolver_by_id(StatementOfWorkGQLModel, description="Returns SOW by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of a statement of work used for creation")
class StatementOfWorkInsertGQLModel:
    event_id: uuid.UUID = strawberryA.field(description="The ID of the event data")
    project_id: uuid.UUID = strawberryA.field(description="The ID of the project data")
    
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the statement of work", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the statement of work", default=datetime.datetime.now() + datetime.timedelta(days=30))
    
    valid: Optional[bool] = strawberryA.field(description="Indicates whether the statement of work data is valid or not", default=True)
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the statement of work data", default=None)
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None

@strawberryA.input(description="Definition of a statement of work used for update")
class StatementOfWorkUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the statement of work")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the financial data is valid or not", default=None)
    project_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the project type",default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the milestone",default=None)
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the milestone",default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="Input structure for deleting a statement of work")
class StatementOfWorkDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key (UUID) that identifies the statement of work to be deleted")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last changeS")


@strawberryA.type(description="Result of a mutation for statement of work")
class StatementOfWorkResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the statement of work", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the statement of work", permission_classes=[OnlyForAuthentized()])
    async def statementofwork(self, info: strawberryA.types.Info) -> Union[StatementOfWorkGQLModel, None]:
        result = await StatementOfWorkGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new statement of work.", permission_classes=[OnlyForAuthentized()])
async def statement_of_work_insert(self, info: strawberryA.types.Info, statementofwork: StatementOfWorkInsertGQLModel) -> StatementOfWorkResultGQLModel:
    user = getUserFromInfo(info)
    statementofwork.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).statementofwork
    row = await loader.insert(statementofwork)
    result = StatementOfWorkResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the statement of work.", permission_classes=[OnlyForAuthentized()])
async def statement_of_work_update(self, info: strawberryA.types.Info, statementofwork: StatementOfWorkUpdateGQLModel) -> StatementOfWorkResultGQLModel:
    user = getUserFromInfo(info)
    statementofwork.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).statementofwork
    row = await loader.update(statementofwork)
    result = StatementOfWorkResultGQLModel()
    result.msg = "ok"
    result.id = statementofwork.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

