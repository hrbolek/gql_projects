import typing
import strawberry
from src.GraphTypeDefinitions.BaseGQLModel import IDType


from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
)
from uoishelpers.resolvers import (
    createInputs,
    VectorResolver
)

ProjectGQLModel = typing.Annotated["ProjectGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_Projects.ProjectGQLModel")]

@createInputs(v2=True)
class GroupProjectsInputFilter:
    pass

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: IDType = strawberry.federation.field(external=True)

    from ..BaseGQLModel import resolve_reference

    projects: typing.List[ProjectGQLModel] = strawberry.field(
        description="projects managed directly by this group (it does not return projects managed by subgroups)",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["ProjectGQLModel"](fkey_field_name="rbacobject_id", whereType=GroupProjectsInputFilter)
    )
    # async def event_invitations(self, info:strawberry.types.Info)