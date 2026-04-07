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
        info: strawberry.Info,
        project_type: ProjectTypeInsertGQLModel,
        user_roles: typing.List[dict],
        db_row: typing.Any,
        rbacobject_id: IDType,
    ) -> typing.Union[ProjectTypeGQLModel, InsertError[ProjectTypeGQLModel]]:
        
        rbac_id = createUuid()
        rbac = await createRBAC(
            info= info, 
            rbacobjectId= rbac_id,
            mastergroupId= rbacobject_id,
            name= f"{project_type.name}-rbac",
            # "roles": 
        )
        # print(f"project_type_insert, {rbac}")
        # project_type.rbacobject_id = rbac_id
        project_type.set_rbacobject_id(rbac_id)
        return await Insert[ProjectTypeGQLModel].DoItSafeWay(info=info, entity=project_type)
    

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
        info: strawberry.Info,
        project_type: ProjectTypeUpdateGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectTypeGQLModel, UpdateError[ProjectTypeGQLModel]]:
        return await Update[ProjectTypeGQLModel].DoItSafeWay(info=info, entity=project_type)
    

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
        info: strawberry.Info,
        project_type: ProjectTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProjectTypeGQLModel]]:
        return await Delete[ProjectTypeGQLModel].DoItSafeWay(info=info, entity=project_type)
    
