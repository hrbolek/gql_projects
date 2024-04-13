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
    resolve_name_en,
    resolve_user_id,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject
)

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance category"""
)
class FinanceCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).financecategory
    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject
    user_id = resolve_user_id

###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class FinanceCategoryWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of finance categories""", permission_classes=[OnlyForAuthentized()])
async def finance_category_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[FinanceCategoryWhereFilter] = None
) -> List[FinanceCategoryGQLModel]:
    loader = getLoadersFromInfo(info).financecategory
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

finance_category_by_id = createRootResolver_by_id(FinanceCategoryGQLModel, description="Returns finance category by its id")


###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional
@strawberryA.input(description="Definition of a finance category used for creation")
class FinanceCategoryInsertGQLModel:
    name: str = strawberryA.field(description="Name/label of the finance category")
    name_en: str = strawberryA.field(description="Name/label of the finance category in English")

    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the finance category data", default=None)
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None

@strawberryA.input(description="Definition of a finance category used for update")
class FinanceCategoryUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the finance category")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of the last change")

    name: Optional[str] = strawberryA.field(description="Updated name/label of the finance category", default=None)
    name_en: Optional[str] = strawberryA.field(description="Updated name/label of the finance category in English", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberryA.type(description="Result of a mutation for a finance category")
class FinanceCategoryResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the finance category", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the finance category", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Union[FinanceCategoryGQLModel, None]:
        result = await FinanceCategoryGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new finance category.", permission_classes=[OnlyForAuthentized()])
async def finance_category_insert(self, info: strawberryA.types.Info, finance: FinanceCategoryInsertGQLModel) -> FinanceCategoryResultGQLModel:
    user = getUserFromInfo(info)
    finance.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).financecategory
    row = await loader.insert(finance)
    result = FinanceCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the finance category.", permission_classes=[OnlyForAuthentized()])
async def finance_category_update(self, info: strawberryA.types.Info, finance: FinanceCategoryUpdateGQLModel) -> FinanceCategoryResultGQLModel:
    user = getUserFromInfo(info)
    finance.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).financecategory
    row = await loader.update(finance)
    result = FinanceCategoryResultGQLModel()
    result.msg = "ok" if (row is not None) else "fail"
    result.id = finance.id
    return result

@strawberry.mutation(description="Delete the finance category",
        permission_classes=[OnlyForAuthentized()])
async def finance_category_delete(self, info: strawberryA.types.Info, id: uuid.UUID) -> FinanceCategoryResultGQLModel:
    loader = getLoadersFromInfo(info).financecategory
    row = await loader.delete(id=id)
    result = FinanceCategoryResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result

