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

from src.DBDefinitions.FinanceTransferDBModel import FinanceTransferDBModel

from ..BaseGQLModel import BaseGQLModel, IDType, Relation
from ..ApplicationInfo import ApplicationInfo

FinanceGQLModel = typing.Annotated["FinanceGQLModel", strawberry.lazy(".FinanceGQLModel")]

@createInputs2
class FinanceTransferInputFilter:
    name: str
    finance_source_id: IDType
    finance_destination_id: IDType
    amount: float
    id: IDType

@strawberry.federation.type(
    description="""Entity representing a FinanceTransfer""",
    keys=["id"]
)
class FinanceTransferGQLModel(BaseGQLModel):
    DBModel = FinanceTransferDBModel


    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Finance name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    finance_source_id: typing.Optional[IDType] = strawberry.field(
        description="""Finance source id""",    
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    finance_destination_id: typing.Optional[IDType] = strawberry.field(
        description="""Finance destination id""",    
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    amount: typing.Optional[float] = strawberry.field(
        description="""Finance transfer amount""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    startdate: typing.Optional[datetime.date] = strawberry.field(
        description="""Finance transfer start date""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    finance_source: typing.Optional[FinanceGQLModel] = strawberry.field(
        description="""Finance source""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FinanceGQLModel"](fkey_field_name="finance_source_id")
    )

    finance_destination : typing.Optional[FinanceGQLModel]= strawberry.field(
        description="""Finance destination""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FinanceGQLModel"](fkey_field_name="finance_destination_id")
    )


@strawberry.interface(
    description="""FinanceTransfer queries"""
)
class FinanceTransferQuery:
    finance_transfer_by_id: typing.Optional[FinanceTransferGQLModel] = strawberry.field(
        description="""get a financetransfer by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=FinanceTransferGQLModel.load_with_loader
    )

    finance_transfer_page: typing.List[FinanceTransferGQLModel] = strawberry.field(
        description="""get a page of financetransfers""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[FinanceTransferGQLModel](whereType=FinanceTransferInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a FinanceTransfer"""
)
class FinanceTransferInsertGQLModel:
    getLoader = FinanceTransferGQLModel.getLoader
    finance_source_id: IDType = strawberry.field(
        description="""Finance source id""",
        # default=None
    )
    finance_destination_id: IDType = strawberry.field(
        description="""Finance destination id""",
        # default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="""transfer name / description""",
        default=None
    )
    
    amount: typing.Optional[float] = strawberry.field(
        description="""transfer transfer amount""",
        default=0
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""transfer id""",
        default=None
    )
    
    start_date: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a FinanceTransfer"""
)
class FinanceTransferUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""FinanceTransfer id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""transfer description""",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a FinanceTransfer"""
)
class FinanceTransferDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""FinanceTransfer id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""FinanceTransfer mutations"""
)
class FinanceTransferMutation:
    from .FinanceGQLModel import FinanceGQLModel
    @strawberry.mutation(
        description="""Make a financetransfer""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAccessControlExtension[InsertError, FinanceTransferGQLModel](
                roles=[
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, FinanceTransferGQLModel](),
            RbacProviderExtension[InsertError, FinanceTransferGQLModel](),
            LoadDataExtension[InsertError, FinanceTransferGQLModel](
                getLoader=FinanceGQLModel.getLoader,
                primary_key_name="finance_source_id"
            )
        ],
    )
    async def finance_transfer_insert(
        self,
        info: ApplicationInfo,
        finance_transfer: FinanceTransferInsertGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[FinanceTransferGQLModel, InsertError[FinanceTransferGQLModel]]:
        FinanceTransferService = info.ServiceCtx.Services.FinanceTransferService
        result = await FinanceTransferService.ExecuteServiceMethod(
            FinanceTransferService.Create(
                ctx=info.ServiceCtx,
                finance_source_id=finance_transfer.finance_source_id,
                finance_destination_id=finance_transfer.finance_destination_id,
                amount=finance_transfer.amount
            ),
            OK=lambda result: FinanceTransferGQLModel.from_dataclass(result),
            Error=lambda msg: InsertError[FinanceTransferGQLModel](
                msg=msg,
                _input=finance_transfer,
                code="46084b9a-324d-4751-b2fd-a5f4a8740a99",
                location="FinanceTransferMutation.finance_transfer_insert"
            )
        )
        return result
    

    @strawberry.mutation(
        description="""Update a FinanceTransfer""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[FinanceTransferGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, FinanceTransferGQLModel](
                roles=[
                    "administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, FinanceTransferGQLModel](),
            RbacProviderExtension[UpdateError, FinanceTransferGQLModel](),
            LoadDataExtension[UpdateError, FinanceTransferGQLModel]()
        ],
    )
    async def finance_transfer_update(
        self,
        info: ApplicationInfo,
        finance_transfer: FinanceTransferUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[FinanceTransferGQLModel, UpdateError[FinanceTransferGQLModel]]:
        FinanceTransferService = info.ServiceCtx.Services.FinanceTransferService
        result = await FinanceTransferService.ExecuteServiceMethod(
            FinanceTransferService.Update(
                ctx=info.ServiceCtx,
                entity=finance_transfer
            ),
            OK=lambda result: FinanceTransferGQLModel.from_dataclass(result),
            Error=lambda msg: UpdateError[FinanceTransferGQLModel](
                msg=msg,
                _input=finance_transfer,
                _entity=FinanceTransferGQLModel.from_dataclass(db_row),
                code="e00bdc3b-e13e-496f-bc7d-d847c517f41e",
                location="FinanceTransferMutation.finance_transfer_update"
            )
        )
        return result

    @strawberry.mutation(
        description="""Delete a FinanceTransfer""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[FinanceTransferGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, FinanceTransferGQLModel](
                roles=[
                    "administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, FinanceTransferGQLModel](),
            RbacProviderExtension[DeleteError, FinanceTransferGQLModel](),
            LoadDataExtension[DeleteError, FinanceTransferGQLModel]()
        ],
    )   
    async def finance_transfer_delete(
        self,
        info: ApplicationInfo,
        finance_transfer: FinanceTransferDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[FinanceTransferGQLModel]]:
        FinanceTransferService = info.ServiceCtx.Services.FinanceTransferService
        result = await FinanceTransferService.ExecuteServiceMethod(
            FinanceTransferService.Delete(
                ctx=info.ServiceCtx,
                entity=finance_transfer
            ),
            OK=lambda result: None,
            Error=lambda msg: DeleteError[FinanceTransferGQLModel](
                msg=msg,
                _input=finance_transfer,
                _entity=FinanceTransferGQLModel.from_dataclass(db_row),
                code="d5deed43-bbdf-4a5a-9259-35cf7556ca7e",
                location="FinanceTransferMutation.finance_transfer_delete"
            )
        )
        return result
