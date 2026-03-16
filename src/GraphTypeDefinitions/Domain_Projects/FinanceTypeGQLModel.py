import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,
    createInputs2,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from src.DBDefinitions import FinanceTypeDBModel

from ..BaseGQLModel import BaseGQLModel, IDType, Relation

@createInputs2
class FinanceTypeInputFilter:
    name: str
    name_en: str
    id: IDType


@strawberry.federation.type(
    description="""Entity representing a Event type""",
    keys=["id"]
)
class FinanceTypeGQLModel(BaseGQLModel):
    DBModel = FinanceTypeDBModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the type's hierarchical location.  """,
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Type name""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Type eng name""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    mastertype_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Parent type id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    

    mastertype: typing.Optional["FinanceTypeGQLModel"] = strawberry.field(
        description="""Type which owns this particular type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FinanceTypeGQLModel"](fkey_field_name="mastertype_id")
    )

    subtypes: typing.List["FinanceTypeGQLModel"] = strawberry.field(
        description="""Type children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["FinanceTypeGQLModel"](fkey_field_name="mastertype_id", whereType=FinanceTypeInputFilter)
    )



@strawberry.interface(
    description="""Event queries"""
)
class FinanceTypeQuery:
    finance_type_by_id: typing.Optional[FinanceTypeGQLModel] = strawberry.field(
        description="""get a event by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=FinanceTypeGQLModel.load_with_loader
    )

    finance_type_page: typing.List[FinanceTypeGQLModel] = strawberry.field(
        description="""get a page of events""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[FinanceTypeGQLModel](whereType=FinanceTypeInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a Event"""
)
class FinanceTypeInsertGQLModel(TreeInputStructureMixin):
    getLoader = FinanceTypeGQLModel.getLoader
    mastertype_id: IDType = strawberry.field(
        description="""Event parent id""",
        # default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Event name assigned by an administrator""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Event eng name assigned by an administrator""",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""Event id""",
        default=None
    )
    subtypes: typing.Optional[typing.List["FinanceTypeInsertGQLModel"]] = strawberry.field(
        description="sub event types",
        default_factory=list
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="""Input type for updating a Event"""
)
class FinanceTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Event id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Event name assigned by an administrator""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Event eng name assigned by an administrator""",
        default=None
    )
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Event"""
)
class FinanceTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Event id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Event mutations"""
)
class FinanceTypeMutation:
    @strawberry.mutation(
        description="""Insert a event type, it could be connected to master event type""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[FinanceTypeGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, FinanceTypeGQLModel](
                roles=["superadmin"]
            )
        ],
    )
    async def finance_type_insert(
        self,
        info: strawberry.Info,
        event: FinanceTypeInsertGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[FinanceTypeGQLModel, InsertError[FinanceTypeGQLModel]]:
        return await Insert[FinanceTypeGQLModel].DoItSafeWay(info=info, entity=event)
    

    @strawberry.mutation(
        description="""Update a Event type.""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[FinanceTypeGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, FinanceTypeGQLModel](
                roles=["superadmin"]
            )
        ],
    )
    async def finance_type_update(
        self,
        info: strawberry.Info,
        event: FinanceTypeUpdateGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[FinanceTypeGQLModel, UpdateError[FinanceTypeGQLModel]]:
        return await Update[FinanceTypeGQLModel].DoItSafeWay(info=info, entity=event)
    

    @strawberry.mutation(
        description="""Delete a Event type""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[FinanceTypeGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, FinanceTypeGQLModel](
                roles=["superadmin"]
            )
        ],
    )   
    async def finance_type_delete(
        self,
        info: strawberry.Info,
        event: FinanceTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[FinanceTypeGQLModel]]:
        return await Delete[FinanceTypeGQLModel].DoItSafeWay(info=info, entity=event)
    
