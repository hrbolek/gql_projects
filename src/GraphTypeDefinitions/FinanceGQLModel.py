import strawberry as strawberryA
import datetime
import uuid
from typing import List, Annotated, Optional, Union
from .BaseGQLModel import BaseGQLModel

import strawberry
from src.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo


from src.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

from src.GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_amount,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject,
    resolve_valid
)

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]
FinanceTypeGQLModel = Annotated ["FinanceTypeGQLModel",strawberryA.lazy(".FinanceTypeGQLModel")]



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance"""
)
class FinanceGQLModel(BaseGQLModel):
    @classmethod

    def getLoader(cls, info):
        return getLoadersFromInfo(info).finances

    id = resolve_id
    name = resolve_name
    amount = resolve_amount
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    
    @strawberryA.field(description="""Project of finance""", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Optional ["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projects
        result = await loader.load(self.project_id)
        return result
    
    @strawberryA.field(description="""Finance type of finance""", permission_classes=[OnlyForAuthentized()])
    async def financeType(
        self, info: strawberryA.types.Info
    ) -> List["FinanceTypeGQLModel"]:
        loader = getLoadersFromInfo(info).financetypes
        result = await loader.filter_by(id = self.financetype_id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################
    
from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class FinanceWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str
    valid: bool

@strawberryA.field(description="""Returns a list of finances""", permission_classes=[OnlyForAuthentized()])
async def finance_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[FinanceWhereFilter] = None
) -> List[FinanceGQLModel]:
    loader = getLoadersFromInfo(info).finances
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

finance_by_id = createRootResolver_by_id(FinanceGQLModel, description="Returns finance by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of finance data used for creation")
class FinanceInsertGQLModel:
    name: str = strawberryA.field(description="Name/label of the finance")
    financetype_id: uuid.UUID = strawberryA.field(description="The ID of the associated financial type")
    project_id: uuid.UUID = strawberryA.field(description="The ID of the associated project")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the financial data is valid or not (optional)", default=True)
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the finance",default=None)
    amount: Optional[float] = strawberryA.field(description="The amount of finance", default=0.0)
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None

@strawberryA.input(description="Definition of finance data used for update")
class FinanceUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the finance data")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the financial data is valid or not (optional)", default=None)
    name: Optional[str] = strawberryA.field(description="Updated name/label of the finance",default=None)
    financetype_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the financial data type",default=None)
    amount: Optional[float] = strawberryA.field(description="Updated the amount of financial", default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberryA.type(description="Result of a financial data operation")
class FinanceResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the financial data", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the financial data", permission_classes=[OnlyForAuthentized()])
    async def finance(self, info: strawberryA.types.Info) -> Union[FinanceGQLModel, None]:
        result = await FinanceGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################
    

@strawberryA.mutation(description="Adds a new finance.", permission_classes=[OnlyForAuthentized()])
async def finance_insert(self, info: strawberryA.types.Info, finance: FinanceInsertGQLModel) -> FinanceResultGQLModel:
    user = getUserFromInfo(info)
    finance.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).finances
    row = await loader.insert(finance)
    result = FinanceResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the finance.", permission_classes=[OnlyForAuthentized()])
async def finance_update(self, info: strawberryA.types.Info, finance: FinanceUpdateGQLModel) -> FinanceResultGQLModel:
    user = getUserFromInfo(info)
    finance.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).finances
    row = await loader.update(finance)
    result = FinanceResultGQLModel()
    result.msg = "ok"
    result.id = finance.id
    result.msg = "ok" if (row is not None) else "fail"
    return result