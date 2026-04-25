import logging
import pytest
import types

from src.ServiceDefinitions.Domain_Projects.FinanceService import FinanceService
from src.ServiceDefinitions.ServiceContext import ServiceContext
from src.ServiceDefinitions.BaseService import BaseService

class FakeLoader:
    async def insert(self, entity, extraAttributes):
        return {"id": "finance-id", **extraAttributes, "entity": entity}

class FakeLoaders:
    FinanceDBModel = FakeLoader()

@pytest.mark.asyncio
async def test_create_master_finance_creates_rbac_when_missing(monkeypatch):

    # GIVEN
    ctx = ServiceContext(
        loaders=FakeLoaders(),
        user={"id": "user-1"},
    )

    async def fake_rbac_create(ctx, **kw):
        logging.info(f"Fake RBAC Create called with {kw}")
        return {"id": "rbac-123"}

    monkeypatch.setattr(
        "src.ServiceDefinitions.Domain_UG.RBACService.RBACService.Create",
        fake_rbac_create,
    )

    # WHEN
    finance = await FinanceService.CreateMasterFinance(
        ctx,
        entity=None,
        name="Test finance",
    )

    # THEN
    assert finance.get("rbacobject_id") == "rbac-123", f"Expected RBAC object to be created and linked, got {finance}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,args",
    [
        ("Create", dict(name="A")),
        ("Update", dict(id=1, name="B")),
        ("Delete", types.SimpleNamespace(id=1)),
    ],
)
async def test_base_service_forwards_to_loader(method, args):

    calls = {}

    class FakeLoader:
        async def insert(self, entity, extraAttributes):
            calls["insert"] = (entity, extraAttributes)
        async def update(self, entity, extraValues):
            calls["update"] = (entity, extraValues)
        async def delete(self, id):
            calls["delete"] = id

    class TestService(BaseService):
        @classmethod
        async def getLoader(cls, ctx):
            return FakeLoader()

    ctx = ServiceContext(loaders=None)

    await getattr(TestService, method)(ctx, args)

    assert calls


@pytest.mark.asyncio
async def test_execute_service_method_error():

    async def fail():
        raise ValueError("fail")

    result = await BaseService.ExecuteServiceMethod(
        fail(),
        OK=lambda result: result,
        Error=lambda msg: {
            "msg": msg,
            "code": "X",
            "location": "L",
        }
    )

    assert "fail" in result["msg"]


@pytest.mark.asyncio
async def test_execute_service_method_ok():

    async def ok():
        return 123

    result = await BaseService.ExecuteServiceMethod(
        ok(),
        OK=lambda result: result,
        Error=lambda **kw: kw
    )

    assert result == 123
