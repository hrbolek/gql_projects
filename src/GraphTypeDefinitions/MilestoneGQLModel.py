import asyncio
import strawberry as strawberryA
from typing import List, Annotated, Optional, Union
import datetime
import uuid
# from src.GraphResolvers import (
#     resolveProjectById,
#     resolveMilestoneAll
# )
from src.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

from src.GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_startdate,
    resolve_enddate,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject,
    resolve_valid
)
from contextlib import asynccontextmanager
from .ProjectGQLModel import ProjectResultGQLModel
from .BaseGQLModel import BaseGQLModel

import strawberry
from src.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo


ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]




@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a milestone"""
)
class MilestoneGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).milestones

    id = resolve_id
    name = resolve_name
    startdate = resolve_startdate
    enddate = resolve_enddate
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    
    @strawberryA.field(description="""Project of milestone""", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Optional ["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projects
        result = await loader.load(self.project_id)
        return result

    @strawberryA.field(description="""Milestones which has this one as follower""", permission_classes=[OnlyForAuthentized()])
    async def previous(self, info: strawberryA.types.Info) -> List["MilestoneGQLModel"]:
        loader = getLoadersFromInfo(info).milestonelinks
        rows = await loader.filter_by(next_id=self.id)
        awaitable = (MilestoneGQLModel.resolve_reference(info, row.previous_id) for row in rows)
        return await asyncio.gather(*awaitable)

    @strawberryA.field(description="""Milestone which follow this milestone""", permission_classes=[OnlyForAuthentized()])
    async def nexts(self, info: strawberryA.types.Info) -> List["MilestoneGQLModel"]:
        loader = getLoadersFromInfo(info).milestonelinks
        rows = await loader.filter_by(previous_id=self.id)
        awaitable = (MilestoneGQLModel.resolve_reference(info, row.next_id) for row in rows)
        return await asyncio.gather(*awaitable)
    
###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class MilestoneWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of milestones""", permission_classes=[OnlyForAuthentized()])
async def milestone_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[MilestoneWhereFilter] = None
) -> List[MilestoneGQLModel]:
    loader = getLoadersFromInfo(info).milestones
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

milestone_by_id = createRootResolver_by_id(MilestoneGQLModel, description="Returns milestone by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of a milestone used for creation")
class MilestoneInsertGQLModel:
    name: str = strawberryA.field(description="Name/label of the milestone")
    project_id: uuid.UUID = strawberryA.field(description="The ID of the associated project")
    
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the milestone", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the milestone", default=datetime.datetime.now() + datetime.timedelta(days=30))
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the milestone",default=None)
    rbacobject: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of a milestone used for update")
class MilestoneUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="Timestamp of the last change")
    id: uuid.UUID = strawberryA.field(description="The ID of the milestone")
    name: Optional[str] = strawberryA.field(description="Updated name/label of the milestone",default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the milestone",default=None)
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the milestone",default=None)

@strawberry.input(description="Input structure for deleting a milestone")
class MilestoneDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the milestone")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

@strawberryA.type(description="Result of a user operation on a milestone")
class MilestoneResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the milestone", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the milestone", permission_classes=[OnlyForAuthentized()])
    async def milestone(self, info: strawberryA.types.Info) -> Union[MilestoneGQLModel, None]:
        result = await MilestoneGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input(description="Definition of milestone link used for addition")
class MilestoneLinkAddGQLModel:
    previous_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the previous milestone")
    next_id: Optional[uuid.UUID]  = strawberryA.field(description="The ID of the next milestone")

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new milestones link.", permission_classes=[OnlyForAuthentized()])
async def milestones_link_add(self, info: strawberryA.types.Info, link: MilestoneLinkAddGQLModel) -> MilestoneResultGQLModel:
    user = getUserFromInfo(info)
    link.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).milestonelinks
    rows = await loader.filter_by(previous_id=link.previous_id, next_id=link.next_id)
    row = next(rows, None)
    result = MilestoneResultGQLModel()
    if row is None:
        row = await loader.insert(link)
        result.msg = "ok"
    if row is not None:
        result.msg = "exists"
    result.id = link.previous_id
    return result

@strawberryA.mutation(description="Adds a new milestones link.", permission_classes=[OnlyForAuthentized()])
async def milestones_link_remove(self, info: strawberryA.types.Info, link: MilestoneLinkAddGQLModel) -> MilestoneResultGQLModel:
    user = getUserFromInfo(info)
    link.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).milestonelinks
    rows = await loader.filter_by(previous_id=link.previous_id, next_id=link.next_id)
    row = next(rows, None)
    result = MilestoneResultGQLModel()
    result.msg = "fail"
    if (row):
        await loader.delete(row.id)
        result.msg = "ok"
    return result

@strawberryA.mutation(description="Adds a new milestone.", permission_classes=[OnlyForAuthentized()])
async def milestone_insert(self, info: strawberryA.types.Info, milestone: MilestoneInsertGQLModel) -> MilestoneResultGQLModel:
    user = getUserFromInfo(info)
    milestone.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).milestones
    row = await loader.insert(milestone)
    result = MilestoneResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the milestone.", permission_classes=[OnlyForAuthentized()])
async def milestone_update(self, info: strawberryA.types.Info, milestone: MilestoneUpdateGQLModel) -> MilestoneResultGQLModel:
    user = getUserFromInfo(info)
    milestone.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).milestones
    row = await loader.update(milestone)
    result = MilestoneResultGQLModel()
    result.msg = "ok"
    result.id = milestone.id
    result.msg = "ok" if (row is not None) else "fail"
    return result
