import typing
import uuid
from uoishelpers.dataloaders.IDLoader import IDLoader

from ...DBDefinitions.ProjectDBModel import ProjectDBModel
from ...DBDefinitions import FinanceDBModel
from ..BaseService import BaseService, ServiceContext

class FinanceService(BaseService[IDLoader[FinanceDBModel]]):

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[FinanceDBModel]:
        return ctx.loaders.FinanceDBModel

    @classmethod
    async def Project(cls, ctx: ServiceContext, id: uuid.UUID) -> typing.Optional[ProjectDBModel]:
        loader = ctx.loaders.ProjectDBModel
        projects = await loader.filter_by(finance_id=id)
        projects = list(projects)
        if not projects:
            return None
        project = projects[0]
        return project
    

    @classmethod
    async def CreateMasterFinance(cls, ctx, **data) -> typing.Optional[FinanceDBModel]:
        from ..Domain_UG.RBACService import RBACService
        rbacobject_id = data.pop("rbacobject_id", None)
        # rbacobject_id = data.get("rbacobject_id")
        if rbacobject_id is None:
            rbacobject = await RBACService.Create(ctx, masterrbacobject_id=None, name="TopFinance")
            rbacobject_id = rbacobject["id"]

        finance = await cls.Create(
            ctx=ctx,
            **data,
            rbacobject_id=rbacobject_id,
            masterfinance_id=None,
        )
        return finance
