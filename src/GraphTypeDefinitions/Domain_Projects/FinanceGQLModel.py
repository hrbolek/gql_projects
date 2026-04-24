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
from uoishelpers.dataloaders.IDLoader import IDLoader
# from src.DBDefinitions.FinanceDBModel import FinanceDBModel

from ..BaseGQLModel import BaseGQLModel, IDType, Relation
from ..ApplicationInfo import ApplicationInfo

FinanceTypeGQLModel = typing.Annotated["FinanceTypeGQLModel", strawberry.lazy(".FinanceTypeGQLModel")]
FinanceTransferGQLModel = typing.Annotated["FinanceTransferGQLModel", strawberry.lazy(".FinanceTransferGQLModel")]
FinanceTransferInputFilter = typing.Annotated["FinanceTransferInputFilter", strawberry.lazy(".FinanceTransferGQLModel")]
ProjectGQLModel = typing.Annotated["ProjectGQLModel", strawberry.lazy(".ProjectGQLModel")]

@createInputs2
class FinanceInputFilter:
    name: str
    name_en: str
    description: str
    finance_type_id: IDType
    masterfinance_id: IDType
    id: IDType

@strawberry.federation.type(
    description="""Entity representing a Finance""",
    keys=["id"]
)
class FinanceGQLModel(BaseGQLModel):
    # DBModel = FinanceDBModel
    @classmethod
    def getLoader(cls, info: ApplicationInfo) -> IDLoader:
        return info.loaders.FinanceDBModel
        # return getLoadersFromInfo(info).get(FinanceDBModel)


    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the group's hierarchical location.  
Materializovaná cesta reprezentující umístění skupiny v hierarchii.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Finance name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Finance eng name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    value: typing.Optional[float] = strawberry.field(
        default=None,
        description="""value at this finnace (account?)""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Finance description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    finance_type_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Finance type id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    masterfinance_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Finance parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    
    masterfinance: typing.Optional["FinanceGQLModel"] = strawberry.field(
        description="""Finance which owns this particular finance""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FinanceGQLModel"](fkey_field_name="masterfinance_id")
    )

    subfinances: typing.List["FinanceGQLModel"] = strawberry.field(
        description="""Finance children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["FinanceGQLModel"](fkey_field_name="masterfinance_id", whereType=FinanceInputFilter)
    )

    type_: typing.Optional["FinanceTypeGQLModel"] = strawberry.field(
        name="type",
        description="""Finance type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FinanceTypeGQLModel"](fkey_field_name="finance_type_id")
    )

    # transfers: typing.List["FinanceTransferGQLModel"] = strawberry.field(
    #     description="transfers from this finance (account)",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     resolver=VectorResolver["FinanceTransferGQLModel"](fkey_field_name="finance_source_id", whereType=FinanceTransferInputFilter)
    # )

    strawberry.field(
        description="transfers from this finance (account)",
        permission_classes=[
            OnlyForAuthentized
        ],
    )
    async def transfers_from(self, info: ApplicationInfo) -> typing.List["FinanceTransferGQLModel"]:
        FinanceTransferService = info.ServiceCtx.Services.FinanceTransferService
        rows = await FinanceTransferService.TransfersFrom(
            ctx=info.ServiceCtx, finance_id=self.id
        )
        return [FinanceTransferGQLModel.from_dataclass(row) for row in rows]

    strawberry.field(
        description="transfers to this finance (account)",
        permission_classes=[
            OnlyForAuthentized
        ],
    )
    async def transfers_to(self, info: ApplicationInfo) -> typing.List["FinanceTransferGQLModel"]:
        FinanceTransferService = info.ServiceCtx.Services.FinanceTransferService
        rows = await FinanceTransferService.TransfersTo(
            ctx=info.ServiceCtx, finance_id=self.id
        )
        return [FinanceTransferGQLModel.from_dataclass(row) for row in rows]


    # async def _project_id(self, info: strawberry.Info):
    #     from .ProjectGQLModel import ProjectGQLModel
    #     loader = ProjectGQLModel.getLoader(info)
    #     projects = await loader.filter_by(finance_id=self.id)
    #     projects = list(projects)
    #     if len(projects) == 1: return ProjectGQLModel.from_dataclass(projects[0])
    #     if len(projects) == 0: return None
    #     return projects

    @strawberry.field(
        description="project id related to this finance",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def project_id(self, info: ApplicationInfo) -> typing.Optional[IDType]:
        FinanceService = info.ServiceCtx.Services.FinanceService
        db_row = await FinanceService.Project(ctx=info.ServiceCtx, id=self.id)
        return db_row.id if db_row else None
    
    @strawberry.field(
        description="project related to this finance",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def project(self, info: ApplicationInfo) -> typing.Optional[ProjectGQLModel]:
        from .ProjectGQLModel import ProjectGQLModel
        FinanceService = info.ServiceCtx.Services.FinanceService
        result = await FinanceService.Project(ctx=info.ServiceCtx, id=self.id)
        return ProjectGQLModel.from_dataclass(result) if result else None


@strawberry.interface(
    description="""Finance queries"""
)
class FinanceQuery:
    finance_by_id: typing.Optional[FinanceGQLModel] = strawberry.field(
        description="""get a finance by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=FinanceGQLModel.load_with_loader
    )

    finance_page: typing.List[FinanceGQLModel] = strawberry.field(
        description="""get a page of finances""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[FinanceGQLModel](whereType=FinanceInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a Finance"""
)
class FinanceInsertGQLModel(TreeInputStructureMixin):
    getLoader = FinanceGQLModel.getLoader
    masterfinance_id: IDType = strawberry.field(
        description="""Finance parent id""",
        # default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Finance name assigned by an administrator""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Finance eng name assigned by an administrator""",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Finance description""",
        default=None
    )
    value: typing.Optional[float] = strawberry.field(
        description="""Finance value""",
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""Finance id""",
        default=None
    )
    # subfinances: typing.Optional[typing.List["FinanceInsertGQLModel"]] = strawberry.field(
    #     description="sub finances",
    #     default_factory=list
    # )
    finance_type_id: typing.Optional[IDType] = strawberry.field(
        description="""Finance type id""",
        default=None
    )
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="""Input type for updating a Finance"""
)
class FinanceUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Finance id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Finance name assigned by an administrator""",
        default=strawberry.UNSET
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Finance eng name assigned by an administrator""",
        default=strawberry.UNSET
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Finance description""",
        default=strawberry.UNSET
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Finance"""
)
class FinanceDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Finance id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Finance mutations"""
)
class FinanceMutation:
    @strawberry.mutation(
        description="""Insert a finance without master""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, FinanceGQLModel](
                roles=[
                    "superadmin"
                ]
            )
            # UserAccessControlExtension[InsertError, FinanceGQLModel](
            #     roles=[
            #         "administrátor"
            #     ]
            # ),
            # UserRoleProviderExtension[InsertError, FinanceGQLModel](),
            # RbacProviderExtension[InsertError, FinanceGQLModel](),
            # LoadDataExtension[InsertError, FinanceGQLModel](
            #     getLoader=FinanceGQLModel.getLoader,
            #     primary_key_name="masterfinance_id"
            # )
        ],
    )
    async def finance_master_insert(
        self,
        info: ApplicationInfo,
        finance: FinanceInsertGQLModel,
        # db_row: typing.Any,
        # rbacobject_id: IDType,
        # user_roles: typing.List[dict],
    ) -> typing.Union[FinanceGQLModel, InsertError[FinanceGQLModel]]:
        FinanceService = info.ServiceCtx.Services.FinanceService
        result = await FinanceService.ExecuteServiceMethod(
            FinanceService.CreateMasterFinance(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(finance)
            ),
            Error=lambda msg: InsertError[FinanceGQLModel](
                code="d1660087-a7a9-471f-b2a6-58c2e42c9e6a",
                location="finance_insert",
                msg=msg,
                _input=finance
            ),
            OK=FinanceGQLModel
        )
        return result

    @strawberry.mutation(
        description="""Insert a master finance""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAccessControlExtension[InsertError, FinanceGQLModel](
                roles=[
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, FinanceGQLModel](),
            RbacProviderExtension[InsertError, FinanceGQLModel](),
            LoadDataExtension[InsertError, FinanceGQLModel](
                getLoader=FinanceGQLModel.getLoader,
                primary_key_name="masterfinance_id"
            )
        ],
    )
    async def finance_insert(
        self,
        info: ApplicationInfo,
        finance: FinanceInsertGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[FinanceGQLModel, InsertError[FinanceGQLModel]]:
        FinanceService = info.ServiceCtx.Services.FinanceService
        result = await FinanceService.ExecuteServiceMethod(
            FinanceService.CreateMasterFinance(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(finance)
            ),
            Error=lambda msg: InsertError[FinanceGQLModel](
                code="d1660087-a7a9-471f-b2a6-58c2e42c9e6a",
                location="finance_insert",
                msg=msg,
                _input=finance
            ),
            OK=FinanceGQLModel
        )
        return result


    @strawberry.mutation(
        description="""Update a Finance""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, FinanceGQLModel](
                roles=[
                    "administrátor", 
                ]
            ),
            UserRoleProviderExtension[UpdateError, FinanceGQLModel](),
            RbacProviderExtension[UpdateError, FinanceGQLModel](),
            LoadDataExtension[UpdateError, FinanceGQLModel]()
        ],
    )
    async def finance_update(
        self,
        info: ApplicationInfo,
        finance: FinanceUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[FinanceGQLModel, UpdateError[FinanceGQLModel]]:
        FinanceService = info.ServiceCtx.Services.FinanceService
        result = await FinanceService.ExecuteServiceMethod(
            FinanceService.Update(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(finance)
            ),
            Error=lambda msg: UpdateError[FinanceGQLModel](
                code="e1660087-a7a9-471f-b2a6-58c2e42c9e6a",
                location="finance_update",
                msg=msg,
                _input=finance,
                entity=ProjectGQLModel.from_dataclass(db_row)
            ),
            OK=FinanceGQLModel
        )
        return result


    @strawberry.mutation(
        description="""Delete a Finance""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, FinanceGQLModel](
                roles=[
                    "administrátor", 
                ]
            ),
            UserRoleProviderExtension[DeleteError, FinanceGQLModel](),
            RbacProviderExtension[DeleteError, FinanceGQLModel](),
            LoadDataExtension[DeleteError, FinanceGQLModel]()
        ],
    )   
    async def finance_delete(
        self,
        info: ApplicationInfo,
        finance: FinanceDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[FinanceGQLModel]]:
        FinanceService = info.ServiceCtx.Services.FinanceService
        result = await FinanceService.ExecuteServiceMethod(
            FinanceService.Delete(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(finance)
            ),
            Error=lambda msg: DeleteError[FinanceGQLModel](
                code="f1660087-a7a9-471f-b2a6-58c2e42c9e6a",
                location="finance_delete",
                msg=msg,
                _input=finance,
                entity=ProjectGQLModel.from_dataclass(db_row)
            ),
            OK=lambda: None
        )
        return result
    