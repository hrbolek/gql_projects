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

from src.DBDefinitions.ProjectDependencyDBModel import ProjectDependencyDBModel

from .BaseGQLModel import BaseGQLModel, IDType, Relation

ProjectGQLModel = ["ProjectGQLModel", strawberry.lazy(".ProjectGQLModel")]

@createInputs2
class ProjectDependencyInputFilter:
    name: str
    previous_id: IDType
    next_id: IDType
    id: IDType

@strawberry.federation.type(
    description="""Entity representing a ProjectDependency""",
    keys=["id"]
)
class ProjectDependencyGQLModel(BaseGQLModel):
    DBModel = ProjectDependencyDBModel


    previous_id: typing.Optional[IDType] = strawberry.field(
        description="""Finance source id""",    
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    next_id: typing.Optional[IDType] = strawberry.field(
        description="""Finance destination id""",    
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    previous = strawberry.field(
        description="""Finance source""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProjectGQLModel"](fkey_field_name="masterfinance_id")
    )

    next = strawberry.field(
        description="""Finance destination""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProjectGQLModel"](fkey_field_name="masterfinance_id")
    )


@strawberry.interface(
    description="""ProjectDependency queries"""
)
class ProjectDependencyQuery:
    project_dependency_by_id: typing.Optional[ProjectDependencyGQLModel] = strawberry.field(
        description="""get a projectdependency by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=ProjectDependencyGQLModel.load_with_loader
    )

    project_dependency_page: typing.List[ProjectDependencyGQLModel] = strawberry.field(
        description="""get a page of projectdependencies""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[ProjectDependencyGQLModel](whereType=ProjectDependencyInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a ProjectDependency"""
)
class ProjectDependencyInsertGQLModel(TreeInputStructureMixin):
    getLoader = ProjectDependencyGQLModel.getLoader
    previous_id: IDType = strawberry.field(
        description="""Finance source id""",
        # default=None
    )
    next_id: IDType = strawberry.field(
        description="""Finance destination id""",
        # default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""Finance id""",
        default=None
    )
    
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a ProjectDependency"""
)
class ProjectDependencyUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""ProjectDependency id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a ProjectDependency"""
)
class ProjectDependencyDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""ProjectDependency id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""ProjectDependency mutations"""
)
class ProjectDependencyMutation:
    from .ProjectGQLModel import ProjectGQLModel
    @strawberry.mutation(
        description="""Make a projectdependency""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[ProjectGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAccessControlExtension[InsertError, ProjectDependencyGQLModel](
                roles=[
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, ProjectDependencyGQLModel](),
            RbacProviderExtension[InsertError, ProjectDependencyGQLModel](),
            LoadDataExtension[InsertError, ProjectDependencyGQLModel](
                getLoader=ProjectGQLModel.getLoader,
                primary_key_name="previous_id"
            )
        ],
    )
    async def project_dependency_insert(
        self,
        info: strawberry.Info,
        project_dependency: ProjectDependencyInsertGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectDependencyGQLModel, InsertError[ProjectDependencyGQLModel]]:
        from .ProjectGQLModel import ProjectGQLModel
        project_dependency.rbacobject_id = rbacobject_id
        next_project = await ProjectGQLModel.getLoader(info).load(project_dependency.next_id)
        source_project = db_row
        if source_project.masterproject_id != next_project.id:
            return InsertError[ProjectDependencyGQLModel](
                entity=project_dependency,
                message="Source project does not match the expected project",
                code="16f66af3-052e-4ac8-8b07-035a2a5d9114"
            )
        return await Insert[ProjectDependencyGQLModel].DoItSafeWay(info=info, entity=project_dependency)
    

    @strawberry.mutation(
        description="""Update a ProjectDependency""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, ProjectDependencyGQLModel](
                roles=[
                    "administrátor", 
                ]
            ),
            UserRoleProviderExtension[UpdateError, ProjectDependencyGQLModel](),
            RbacProviderExtension[UpdateError, ProjectDependencyGQLModel](),
            LoadDataExtension[UpdateError, ProjectDependencyGQLModel]()
        ],
    )
    async def projectdependency_update(
        self,
        info: strawberry.Info,
        project_dependency: ProjectDependencyUpdateGQLModel
    ) -> typing.Union[ProjectDependencyGQLModel, UpdateError[ProjectDependencyGQLModel]]:
        return await Update[ProjectDependencyGQLModel].DoItSafeWay(info=info, entity=project_dependency)
    

    @strawberry.mutation(
        description="""Delete a ProjectDependency""",
        permission_classes=[
            OnlyForAuthentized,
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, ProjectDependencyGQLModel](
                roles=[
                    "administrátor", 
                ]
            ),
            UserRoleProviderExtension[DeleteError, ProjectDependencyGQLModel](),
            RbacProviderExtension[DeleteError, ProjectDependencyGQLModel](),
            LoadDataExtension[DeleteError, ProjectDependencyGQLModel]()
        ],
    )   
    async def projectdependency_delete(
        self,
        info: strawberry.Info,
        project_dependency: ProjectDependencyDeleteGQLModel
    ) -> typing.Optional[DeleteError[ProjectDependencyGQLModel]]:
        return await Delete[ProjectDependencyGQLModel].DoItSafeWay(info=info, entity=project_dependency)
    
