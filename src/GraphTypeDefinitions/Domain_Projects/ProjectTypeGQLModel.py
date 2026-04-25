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
from uoishelpers.gqlpermissions.RolePermissionSchemaExtension import createRBAC
from src.DBDefinitions import ProjectTypeDBModel

from ..BaseGQLModel import BaseGQLModel, IDType, Relation, createUuid
from ..ApplicationInfo import ApplicationInfo

@createInputs2
class ProjectTypeInputFilter:
    name: str
    name_en: str
    id: IDType



@strawberry.federation.type(
    description="""Entity representing a Project type""",
    keys=["id"]
)
class ProjectTypeGQLModel(BaseGQLModel):
    DBModel = ProjectTypeDBModel

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

    mastertype: typing.Optional["ProjectTypeGQLModel"] = strawberry.field(
        description="""Type which owns this particular type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProjectTypeGQLModel"](fkey_field_name="mastertype_id")
    )

    subtypes: typing.List["ProjectTypeGQLModel"] = strawberry.field(
        description="""Type children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["ProjectTypeGQLModel"](fkey_field_name="mastertype_id", whereType=ProjectTypeInputFilter)
    )



@strawberry.interface(
    description="""Project queries"""
)
class ProjectTypeQuery:
    project_type_by_id: typing.Optional[ProjectTypeGQLModel] = strawberry.field(
        description="""get a project by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=ProjectTypeGQLModel.load_with_loader
    )

    project_type_page: typing.List[ProjectTypeGQLModel] = strawberry.field(
        description="""get a page of projects""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[ProjectTypeGQLModel](whereType=ProjectTypeInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a Project"""
)
class ProjectTypeInsertGQLModel(TreeInputStructureMixin):
    getLoader = ProjectTypeGQLModel.getLoader
    mastertype_id: IDType = strawberry.field(
        description="""Project parent id""",
        # default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Project name assigned by an administrator""",
        default="project_type"
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Project eng name assigned by an administrator""",
        default="project_type"
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""Project id""",
        default=None
    )
    subtypes: typing.Optional[typing.List["ProjectTypeInsertGQLModel"]] = strawberry.field(
        description="sub project types",
        default_factory=list
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="""Input type for updating a Project"""
)
class ProjectTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Project id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Project name assigned by an administrator""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Project eng name assigned by an administrator""",
        default=None
    )
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Project"""
)
class ProjectTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Project id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Project mutations"""
)
class ProjectTypeMutation:
    @strawberry.mutation(
        description="""Insert a project type, it could be connected to master project type""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[ProjectTypeGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAccessControlExtension[InsertError, ProjectTypeGQLModel](
                roles=["superadmin", "administrátor"]
            ),
            UserRoleProviderExtension[InsertError, ProjectTypeGQLModel](),
            RbacProviderExtension[InsertError, ProjectTypeGQLModel](),
            LoadDataExtension[InsertError, ProjectTypeGQLModel](
                getLoader=ProjectTypeGQLModel.getLoader,
                primary_key_name="mastertype_id"
            )
        ],
    )
    async def project_type_insert(
        self,
        info: ApplicationInfo,
        project_type: ProjectTypeInsertGQLModel,
        user_roles: typing.List[dict],
        db_row: typing.Any,
        rbacobject_id: IDType,
    ) -> typing.Union[ProjectTypeGQLModel, InsertError[ProjectTypeGQLModel]]:
        ProjectTypeService = info.ServiceCtx.Services.ProjectTypeService
        result = await ProjectTypeService.ExecuteServiceMethod(
            # ProjectTypeService.CreateMasterProjectType(
            ProjectTypeService.Create(
                ctx=info.ServiceCtx,
                entity=project_type
            ),
            OK=lambda result: ProjectTypeGQLModel.from_dataclass(result),
            Error=lambda msg: InsertError[ProjectTypeGQLModel](
                msg=msg,
                code="bf1d3fbe-7c87-416b-875b-ea1e0828c22f",
                location="ProjectTypeMutation.project_type_insert",
                _input=project_type
            )
        )
        # rbac_id = createUuid()
        # rbac = await createRBAC(
        #     info= info, 
        #     rbacobjectId= rbac_id,
        #     mastergroupId= rbacobject_id,
        #     name= f"{project_type.name}-rbac",
        #     # "roles": 
        # )
        # print(f"project_type_insert, {rbac}")
        # project_type.rbacobject_id = rbac_id
        # project_type.set_rbacobject_id(rbac_id)
        # return await Insert[ProjectTypeGQLModel].DoItSafeWay(info=info, entity=project_type)

        return result

    

    @strawberry.mutation(
        description="""Update a Project type.""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[ProjectTypeGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, ProjectTypeGQLModel](
                roles=["superadmin", "administrátor"]
            ),
            UserRoleProviderExtension[UpdateError, ProjectTypeGQLModel](),
            RbacProviderExtension[UpdateError, ProjectTypeGQLModel](),
            LoadDataExtension[UpdateError, ProjectTypeGQLModel]()
        ],
    )
    async def project_type_update(
        self,
        info: ApplicationInfo,
        project_type: ProjectTypeUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectTypeGQLModel, UpdateError[ProjectTypeGQLModel]]:
        ProjectTypeService = info.ServiceCtx.Services.ProjectTypeService
        result = await ProjectTypeService.ExecuteServiceMethod(
            ProjectTypeService.Update(
                ctx=info.ServiceCtx,
                entity=project_type
            ),
            OK=lambda result: ProjectTypeGQLModel.from_dataclass(result),
            Error=lambda msg: UpdateError[ProjectTypeGQLModel](
                msg=msg,
                entity=ProjectTypeGQLModel.resolve_reference(info=info, id=project_type.id),
                code="d1c8b9e7-5c8c-4a3b-9c8e-9a1e0828c22f",
                location="ProjectTypeMutation.project_type_update",
                _input=project_type
            )
        )
        return result
    

    @strawberry.mutation(
        description="""Delete a Project type""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[ProjectTypeGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, ProjectTypeGQLModel](
                roles=["superadmin"]
            )
        ],
    )   
    async def project_type_delete(
        self,
        info: ApplicationInfo,
        project_type: ProjectTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProjectTypeGQLModel]]:
        ProjectTypeService = info.ServiceCtx.Services.ProjectTypeService
        result = await ProjectTypeService.ExecuteServiceMethod(
            ProjectTypeService.Delete(
                ctx=info.ServiceCtx,
                entity=project_type
            ),
            OK=lambda result: None,
            Error=lambda msg: DeleteError[ProjectTypeGQLModel](
                msg=msg,
                entity=ProjectTypeGQLModel.resolve_reference(info=info, id=project_type.id),
                code="e1d8c9f7-6c9c-4b4c-9d9e-9b2e0938d33f",
                location="ProjectTypeMutation.project_type_delete",
                _input=project_type
            )
        )
        return result
    


