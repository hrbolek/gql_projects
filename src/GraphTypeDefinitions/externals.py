import strawberry
import uuid

from src.utils.Dataloaders import getLoadersFromInfo

# @classmethod
# async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
#     return cls(id=id)
@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID): return cls(id=id)


class BaseEternal:
    id: uuid.UUID = strawberry.federation.field(external=True)


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference


@strawberry.federation.type(extend=True, keys=["id"])
class RoleTypeGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference


@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference


@strawberry.federation.type(extend=True, keys=["id"])
class RBACObjectGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    # @classmethod
    # async def resolve_roles(cls, info: strawberry.types.Info, id: uuid.UUID):
    #     loader = getLoadersFromInfo(info).authorizations
    #     authorizedroles = await loader.load(id)
    #     return authorizedroles