
import pytest


class AsyncSpy:
    def __init__(self, return_value=None, raises=None):
        self.called = False
        self.call_args = None
        self.return_value = return_value
        self.raises = raises

    async def __call__(self, *args, **kwargs):
        self.called = True
        self.call_args = (args, kwargs)
        if self.raises:
            raise self.raises
        return self.return_value

def patch_service_method(monkeypatch, service_class, method_name, return_value=None, raises=None):
    spy = AsyncSpy(return_value=return_value, raises=raises)
    monkeypatch.setattr(service_class, method_name, spy)
    return spy

@pytest.fixture
def ServicePatcher(monkeypatch):
    def patch(service_class, method_name, return_value=None, raises=None):
        return patch_service_method(monkeypatch, service_class, method_name, return_value, raises)
    return patch

def make_authorization_test(
    *,
    mutation_name: str,
    service_class,
    service_method: str,
    allowed_roles: list[str],
    denied_roles: list[str],
    dummy_args: dict = None
):
    params = [ ([role], True) for role in allowed_roles ] + [ ([role], False) for role in denied_roles ]
    @pytest.mark.asyncio
    @pytest.mark.parametrize("roles, should_call", params)
    async def test(
        SchemaExecutor,
        CreateMutation,
        WhoAmIExtensionOverride,
        RolePermissionSchemaExtensionOverride,
        monkeypatch,
        roles,
        should_call,
    ):
        # --- nastav role ---
        user = {
            "id": "u1",
            "roles": [{"roletype": {"name": r}, "valid": True} for r in roles],
        }
        WhoAmIExtensionOverride.set_user(user)
        RolePermissionSchemaExtensionOverride.set_response({"result": user["roles"]})

        # --- spy místo service metody ---
        # spy = AsyncSpy(return_value={"id": "ok"})
        # monkeypatch.setattr(service_class, service_method, spy)
        patch_service_method(monkeypatch, service_class, service_method, return_value={"id": "ok"})
        # --- GraphQL call ---
        mutation = CreateMutation(mutation_name)
        variables = {
            "id": "00000000-0000-0000-0000-000000000001",
            "lastchange": "2024-01-01T00:00:00",
            # "name": "X",
        }
        if dummy_args:
            variables.update(dummy_args)

        result = await SchemaExecutor(query=mutation, variable_values=variables)

        # --- assertion ---
        if should_call:
            assert spy.called, f"Service metoda {service_method} měla být zavolána, role {roles} by měla mít přístup"
            # assert "errors" not in result
        else:
            assert not spy.called, f"Service metoda {service_method} NESMÍ být zavolána, role {roles} by neměla mít přístup"
            assert "errors" in result

    return test
