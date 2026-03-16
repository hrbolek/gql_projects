import asyncio
import logging
import pytest
import pytest_asyncio

from graphql import parse

@pytest_asyncio.fixture(scope="session")
async def Database():
    # create in-memory SQLite database and run migrations
    from src.DBDefinitions import startEngine

    connectionstring = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(connectionstring, makeDrop=True, makeUp=True)

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("DEMODATA", "True")

    from src.DBFeeder import initDB
    await initDB(asyncSessionMaker=async_session_maker, filename="./systemdata.test.json")

    yield async_session_maker

    # await asyncEngine.dispose()

@pytest_asyncio.fixture
async def ContextBase(Database):

    from src.Dataloaders import createLoadersContext
    
    async_session_maker = Database
    class Request:
        @property
        def cookies(self):
            return {}
        @property
        def headers(self):
            return {}
    async with async_session_maker() as session:
        loadersContext = createLoadersContext(session=session)
        logging.info(f"ContextBase created with session: {session}")
        yield {
            **loadersContext, 
            "request": Request(),
        }
        await session.commit()
        logging.info(f"ContextBase teardown with session: {session}")

@pytest.fixture
def UserPatch():
    local_roles = [
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ]
    def exec(roles: list = None):
        nonlocal local_roles
        local_roles = roles or []
    
    
    class PseudoLoader:
        async def load(self, params):
            # mock response for user roles query
            # logging.info(f"userRolesForRBACQuery_loader called with params: {params}")
            return {
                "result": local_roles
            }    
    return exec, PseudoLoader()

@pytest_asyncio.fixture
async def FullContext(ContextBase, UserPatch):
    
    loadersContext = ContextBase
    userRolesForRBACQuery_patch, userRolesForRBACQuery_loader = UserPatch
    context_ = {
        **loadersContext,
        "userRolesForRBACQuery_loader": userRolesForRBACQuery_loader,
        "userRolesForRBACQuery_patch": userRolesForRBACQuery_patch
    }
    return context_

@pytest.fixture
def WhoAmIExtensionOverride(FullContext):
    from uoishelpers.schema import WhoAmIExtension
    class WhoAmIExtension_Debug(WhoAmIExtension):
        user = None
        async def on_execute(self):
            user = self.__class__.user or {
                "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
                "roles": [{
                    "roletype": {"name": "superadmin"}
                }]
            }

            self.execution_context.context["user"] = user
            yield

        @classmethod
        def set_user(cls, user):
            cls.user = user

        
    return WhoAmIExtension_Debug


@pytest.fixture
def RolePermissionSchemaExtensionOverride(FullContext):
    from uoishelpers.gqlpermissions.RolePermissionSchemaExtension import RolePermissionSchemaExtension
    class RolePermissionSchemaExtension_Debug(RolePermissionSchemaExtension):
        response_override = None

        async def load(self, key):
            response = self.__class__.response_override
            if response is None:
                response = {
                    "result": self.execution_context.context["user"].get("roles", [])
                }
            return response

        async def on_execute(self):
            self.execution_context.context["userRolesForRBACQuery_loader"] = self
            yield

        @classmethod
        def set_response(cls, response):
            cls.response_override = response

    return RolePermissionSchemaExtension_Debug

@pytest.fixture
def SchemaExecutor(
    FullContext,
    WhoAmIExtensionOverride,
    RolePermissionSchemaExtensionOverride
):
    # GQLUG_ENDPOINT_URL
    # monkeypatch = pytest.MonkeyPatch()
    # monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8125/gql")

    from uoishelpers.schema import WhoAmIExtension
    # schema.extensions.append(WhoAmIExtension)
    from uoishelpers.gqlpermissions.RolePermissionSchemaExtension import RolePermissionSchemaExtension


    from src.GraphTypeDefinitions import schema
    schema.extensions = list(
        filter(lambda ex: ex not in [
            WhoAmIExtension, 
            RolePermissionSchemaExtension,
            WhoAmIExtensionOverride,
            RolePermissionSchemaExtensionOverride
        ], schema.extensions)
    )
    schema.extensions = list(
        filter(lambda ex: getattr(ex, "__name__", None) not in [
            "WhoAmIExtension_Debug",
            "RolePermissionSchemaExtension_Debug"
        ], schema.extensions)
    )
    schema.extensions.append(WhoAmIExtensionOverride)
    schema.extensions.append(RolePermissionSchemaExtensionOverride)

    for ext in schema.extensions:
        logging.info(f"Schema extension: {ext}")
    FullContext["user"] = {
        "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
        "roles": [{
            "roletype": {"name": "superadmin"}
        }]
    }
    async def Execute(query, variable_values={}):
        result = await schema.execute(query=query, variable_values=variable_values, context_value=FullContext)
        value = {"data": result.data} 
        if result.errors:
            value["errors"] = result.errors
        return value
    return Execute


@pytest.fixture
async def Sdl(SchemaExecutor):
    SERVICE_SDL_QUERY = """
      query {
        _service {
          sdl
        }
      }
    """
    sdl_json_result = await SchemaExecutor(query=SERVICE_SDL_QUERY)
    data = sdl_json_result.get("data", {})
    sdl_str = data["_service"]["sdl"]
    sdl_doc = parse(sdl_str)

    return sdl_doc

@pytest.fixture
async def CreateMutation(Sdl):
    from .utils_sdl_2 import build_expanded_mutation
    def createMutation(name):
        query = build_expanded_mutation(Sdl, name)
        logging.info(f"query {name}\n{query}")
        assert query is not None, f"Failed to build mutation for {name}"
        return query
    return createMutation

@pytest.fixture
async def CreateQuery(Sdl):
    from .utils_sdl_2 import build_query_scalar, build_query_page
    def createQuery(name):
        query = build_query_scalar(Sdl, name)
        if not query:
            query = build_query_page(Sdl, name)
        assert query is not None, f"Failed to build mutation for {name}"
        logging.info(f"query {name}\n{query}")
        return query
    return createQuery