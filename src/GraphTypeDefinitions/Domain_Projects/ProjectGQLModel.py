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

from ..ApplicationInfo import ApplicationInfo
from src.DBDefinitions.ProjectDBModel import ProjectDBModel

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType, Relation


ProjectTypeGQLModel = typing.Annotated["ProjectTypeGQLModel", strawberry.lazy(".ProjectTypeGQLModel")]
FinanceGQLModel = typing.Annotated["FinanceGQLModel", strawberry.lazy(".FinanceGQLModel")]
ProjectDependencyGQLModel = typing.Annotated["ProjectDependencyGQLModel", strawberry.lazy(".ProjectDependencyGQLModel")]

@createInputs2#(v2=True)
class ProjectInputFilter:
    name: str
    name_en: str
    description: str
    project_type_id: IDType = strawberry.field(
        description="Filter for project type id", 
        # directives=[Relation(to="ProjectTypeGQLModel")]
    )
    masterproject_id: IDType = strawberry.field(
        description="Filter for project id", 
        # directives=[Relation(to="ProjectTypeGQLModel")]
    )
    done: bool = strawberry.field(
        description="Filter for finished projects", 
        # directives=[Relation(to="ProjectTypeGQLModel")]
    )
    start_date: datetime.datetime = strawberry.field(
        description="Filter for project start date", 
        # directives=[Relation(to="ProjectTypeGQLModel")]
    )
    end_date: datetime.datetime = strawberry.field(
        description="Filter for project end date", 
        # directives=[Relation(to="ProjectTypeGQLModel")]
    )
    id: IDType = strawberry.field(
        description="Filter for project id", 
        # directives=[Relation(to="ProjectTypeGQLModel")]
    )

@strawberry.federation.type(
    description="""Entity representing a Project""",
    keys=["id"]
)
class ProjectGQLModel(BaseGQLModel):
    DBModel = ProjectDBModel


    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the group's hierarchical location.  
Materializovaná cesta reprezentující umístění skupiny v hierarchii.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Project name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Project eng name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    done: typing.Optional[bool] = strawberry.field(
        default=None,
        description="""Is the project done?""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Project start date""",
        permission_classes=[
            OnlyForAuthentized
        ]   
    )
    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Project end date""",
        permission_classes=[
            OnlyForAuthentized
        ]   
    )
    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Project description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    project_type_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Project type id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    masterproject_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Project parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    
    masterproject: typing.Optional["ProjectGQLModel"] = strawberry.field(
        description="""Project which owns this particular project""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProjectGQLModel"](fkey_field_name="masterproject_id")
    )

    subprojects: typing.List["ProjectGQLModel"] = strawberry.field(
        description="""Project children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["ProjectGQLModel"](fkey_field_name="masterproject_id", whereType=ProjectInputFilter)
    )

    finance_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Finance id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    finance: typing.Optional["FinanceGQLModel"] = strawberry.field(
        description="""Project which owns this particular project""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FinanceGQLModel"](fkey_field_name="finance_id")
    )

    type_: typing.Optional["ProjectTypeGQLModel"] = strawberry.field(
        name="type",
        description="""Project type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProjectTypeGQLModel"](fkey_field_name="project_type_id")
    )

    strawberry.field(
        description="""Projects which are linked to this project as next projects (e.g. projects which have this project as masterproject and at the same time have startdate greater than enddate of this project)""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def prevs(self, info: ApplicationInfo) -> typing.List["ProjectDependencyGQLModel"]:
        ProjectService = info.ServiceCtx.Services.ProjectService
        dependencies = await ProjectService.PreviousProjects(info.ServiceCtx, id=self.id)
        return [ProjectDependencyGQLModel.from_dataclass(dep) for dep in dependencies]
        
    
    strawberry.field(
        description="""Projects which are linked to this project as next projects (e.g. projects which have this project as masterproject and at the same time have startdate greater than enddate of this project)""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def nexts(self, info: ApplicationInfo) -> typing.List["ProjectDependencyGQLModel"]:
        ProjectService = info.ServiceCtx.Services.ProjectService
        dependencies = await ProjectService.NextProjects(info.ServiceCtx, id=self.id)
        return [ProjectDependencyGQLModel.from_dataclass(dep) for dep in dependencies]
    
@strawberry.interface(
    description="""Project queries"""
)
class ProjectQuery:
    project_by_id: typing.Optional[ProjectGQLModel] = strawberry.field(
        description="""get a project by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=ProjectGQLModel.load_with_loader
    )

    project_page: typing.List[ProjectGQLModel] = strawberry.field(
        description="""get a page of projects""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[ProjectGQLModel](whereType=ProjectInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a Project within another project"""
)
class ProjectInsertGQLModel(TreeInputStructureMixin):
    getLoader = ProjectGQLModel.getLoader
    masterproject_id: IDType = strawberry.field(
        description="""Project parent id""",
        # default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Project name assigned by an administrator""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Project eng name assigned by an administrator""",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Project description""",
        default=None
    )
    done: typing.Optional[bool] = strawberry.field(
        description="""Is the project done?""",
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""Project id""",
        default=None
    )
    subprojects: typing.Optional[typing.List["ProjectInsertGQLModel"]] = strawberry.field(
        description="sub projects",
        default_factory=list
    )
    project_type_id: typing.Optional[IDType] = strawberry.field(
        description="""Project type id""",
        default=None
    )
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for creating a Project within another project"""
)
class ProjectInsertMasterGQLModel(TreeInputStructureMixin):
    getLoader = ProjectGQLModel.getLoader
    group_id: IDType = strawberry.field(
        description="""Where the project belongs (faculty, university, ...)""",
        # default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Project name assigned by an administrator""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Project eng name assigned by an administrator""",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Project description""",
        default=None
    )
    done: typing.Optional[bool] = strawberry.field(
        description="""Is the project done?""",
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""Project id""",
        default=None
    )
    subprojects: typing.Optional[typing.List["ProjectInsertGQLModel"]] = strawberry.field(
        description="sub projects",
        default_factory=list
    )
    project_type_id: typing.Optional[IDType] = strawberry.field(
        description="""Project type id""",
        default=None
    )
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="""Input type for updating a Project"""
)
class ProjectUpdateGQLModel:
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
    description: typing.Optional[str] = strawberry.field(
        description="""Project description""",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Project"""
)
class ProjectDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Project id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Project mutations"""
)
class ProjectMutation:
    @strawberry.mutation(
        description="""Insert a sub project""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, ProjectGQLModel](
                roles=[
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, ProjectGQLModel](),
            RbacProviderExtension[InsertError, ProjectGQLModel](),
            LoadDataExtension[InsertError, ProjectGQLModel](
                getLoader=ProjectGQLModel.getLoader,
                primary_key_name="masterproject_id"
            )
        ],
    )
    async def project_insert(
        self,
        info: ApplicationInfo,
        project: ProjectInsertGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectGQLModel, InsertError[ProjectGQLModel]]:
        ProjectService = info.ServiceCtx.Services.ProjectService
        result = await ProjectService.ExecuteServiceMethod(
            ProjectService.Create(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(project),
                rbacobject_id=rbacobject_id
            ),
            OK=ProjectGQLModel,
            Error=lambda msg: InsertError[ProjectGQLModel](
                code="edbb8e7a-a769-4db3-88b5-9b28b50c99ef",
                location="project_insert",
                msg=msg,
                _input=project
            )
        )
        return result
    
    @strawberry.mutation(
        description="""Insert a master project""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, ProjectGQLModel](
                roles=[
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, ProjectGQLModel](),
            RbacProviderExtension[InsertError, ProjectGQLModel](),
            LoadDataExtension[InsertError, ProjectGQLModel](
                getLoader=ProjectGQLModel.getLoader,
                primary_key_name="group_id"
            )
        ],
    )
    async def project_master_insert(
        self,
        info: ApplicationInfo,
        project: ProjectInsertMasterGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectGQLModel, InsertError[ProjectGQLModel]]:
        ProjectService = info.ServiceCtx.Services.ProjectService
        result = await ProjectService.ExecuteServiceMethod(
            ProjectService.CreateMasterProject(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(project),
                masterrbacobject_id=rbacobject_id
            ),
            OK=ProjectGQLModel,
            Error=lambda msg: InsertError[ProjectGQLModel](
                code="4f885abd-4076-4d99-a749-a7db074b42dd",
                location="project_master_insert",
                msg=msg,
                _input=project
            )
        )
        return result

    @strawberry.mutation(
        description="""Update a Project""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, ProjectGQLModel](
                roles=[
                    "administrátor", 
                ]
            ),
            UserRoleProviderExtension[UpdateError, ProjectGQLModel](),
            RbacProviderExtension[UpdateError, ProjectGQLModel](),
            LoadDataExtension[UpdateError, ProjectGQLModel]()
        ],
    )
    async def project_update(
        self,
        info: ApplicationInfo,
        project: ProjectUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectGQLModel, UpdateError[ProjectGQLModel]]:
        ProjectService = info.ServiceCtx.Services.ProjectService
        result = await ProjectService.ExecuteServiceMethod(
            ProjectService.Update(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(project),
            ),
            OK=ProjectGQLModel,
            Error=lambda msg: UpdateError[ProjectGQLModel](
                code="6915527e-a68f-40c8-8aff-23333e798091",
                location="project_update",
                msg=msg,
                _input=project,
                entity=ProjectGQLModel.from_dataclass(db_row)
            )
        )     
        return result
    

    @strawberry.mutation(
        description="""Delete a Project""",
        permission_classes=[
            OnlyForAuthentized,
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, ProjectGQLModel](
                roles=[
                    "administrátor", 
                ]
            ),
            UserRoleProviderExtension[DeleteError, ProjectGQLModel](),
            RbacProviderExtension[DeleteError, ProjectGQLModel](),
            LoadDataExtension[DeleteError, ProjectGQLModel]()
        ],
    )   
    async def project_delete(
        self,
        info: ApplicationInfo,
        project: ProjectDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProjectGQLModel]]:
        ProjectService = info.ServiceCtx.Services.ProjectService
        result = await ProjectService.ExecuteServiceMethod(
            ProjectService.Delete(
                ctx=info.ServiceCtx,
                **dataclasses.asdict(project),
            ),
            OK=lambda result: None,
            Error=lambda msg: DeleteError[ProjectGQLModel](
                code="422cdbe2-6699-4b72-bfbb-777b418f35ae",
                location="project_delete",
                msg=msg,
                _input=project,
                entity=ProjectGQLModel.from_dataclass(db_row)
            )
        )   
        return result
        
    
