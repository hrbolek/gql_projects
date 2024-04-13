import strawberry as strawberryA
import uuid
from typing import List, Annotated, Optional, Union
from contextlib import asynccontextmanager
import datetime

from .BaseGQLModel import BaseGQLModel

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
import strawberry
from src.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo


FinanceGQLModel = Annotated ["FinanceGQLModel",strawberryA.lazy(".FinanceGQLModel")]
FinanceCategoryGQLModel = Annotated ["FinanceCategoryGQLModel",strawberryA.lazy(".FinanceCategoryGQLModel")]


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance type"""
)
class FinanceTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).financetypes

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    
    @strawberryA.field(description="""List of finances, related to finance type""", permission_classes=[OnlyForAuthentized()])
    async def finances(
        self, info: strawberryA.types.Info
    ) -> List["FinanceGQLModel"]:
        loader = getLoadersFromInfo(info).financetypes
        result = await loader.filter_by(id = self.id)
        return result

    
    @strawberryA.field(description="""List of category Id's, related to finance type""", permission_classes=[OnlyForAuthentized()])
    async def category(self, info: strawberryA.types.Info) -> Optional ["FinanceCategoryGQLModel"]:
        from .FinanceCategoryGQLModel import FinanceCategoryGQLModel  # Import here to avoid circular dependency
        result = await FinanceCategoryGQLModel.resolve_reference(info, self.category_id)
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
class FinanceTypeWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str
    valid: bool

@strawberryA.field(description="""Returns a list of finance types""", permission_classes=[OnlyForAuthentized()])
async def finance_type_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[FinanceTypeWhereFilter] = None
) -> List[FinanceTypeGQLModel]:
    loader = getLoadersFromInfo(info).financetypes
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

finance_type_by_id = createRootResolver_by_id(FinanceTypeGQLModel, description="Returns finance type by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of a finance type used for creation")
class FinanceTypeInsertGQLModel:
    name: str = strawberryA.field(description="Name/label of the finance type")
    category_id: uuid.UUID = strawberryA.field(description="The ID of the finance category")
    
    name_en: Optional[str] = strawberryA.field(description="Name/label of the finance type in English",default=None)
    valid: Optional[bool] = strawberryA.field(description="Indicates whether the financial data is valid or not", default=True)
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the finance type data", default=None)
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None

@strawberryA.input(description="Definition of finance type used for update")
class FinanceTypeUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the finance type")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the financial data is valid or not", default=None)
    name: Optional[str] = strawberryA.field(description="Updated name/label of the finance category", default=None)
    name_en: Optional[str] = strawberryA.field(description="Updated name/label of the finance category in English", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberryA.type(description="Result of a mutation result of finance type")
class FinanceTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the finance type", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the finance type", permission_classes=[OnlyForAuthentized()])
    async def finance(self, info: strawberryA.types.Info) -> Union[FinanceTypeGQLModel, None]:
        result = await FinanceTypeGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new finance type.", permission_classes=[OnlyForAuthentized()])
async def finance_type_insert(self, info: strawberryA.types.Info, finance: FinanceTypeInsertGQLModel) -> FinanceTypeResultGQLModel:
    user = getUserFromInfo(info)
    finance.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).financetypes
    row = await loader.insert(finance)
    result = FinanceTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the finance type.", permission_classes=[OnlyForAuthentized()])
async def finance_type_update(self, info: strawberryA.types.Info, finance: FinanceTypeUpdateGQLModel) -> FinanceTypeResultGQLModel:
    user = getUserFromInfo(info)
    finance.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).financetypes
    row = await loader.update(finance)
    result = FinanceTypeResultGQLModel()
    result.msg = "ok"
    result.id = finance.id
    result.msg = "ok" if (row is not None) else "fail"
    return result