import typing
from uoishelpers.dataloaders.IDLoader import IDLoader

from ...DBDefinitions import ProjectDBModel
from ..BaseService import BaseService, ServiceContext

class ProjectService(BaseService[IDLoader[ProjectDBModel]]):

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[ProjectDBModel]:
        return ctx.loaders.ProjectDBModel

    # @classmethod
    # async def Create_Within(self, ctx: ServiceContext, group_id: int, **data) -> typing.Any:
    #     GroupService = ctx.Services.GroupService
    #     exists = await GroupService.CheckExistence(ctx, group_id)
    #     if not exists:
    #         raise ValueError(f"Group with id {group_id} does not exist")

    #     result = await self.Create(ctx, group_id=group_id, **data)
    #     return result

    @classmethod
    async def PreviousProjects(cls, ctx: ServiceContext, id: typing.Union[int, str]) -> typing.List[ProjectDBModel]:
        # loader = await cls.getLoader(ctx)
        loader = ctx.loaders.ProjectDependencyDBModel
        dependencies = await loader.filter_by(next_id=id)
        return dependencies
    
    @classmethod
    async def NextProjects(cls, ctx: ServiceContext, id: typing.Union[int, str]) -> typing.List[ProjectDBModel]:
        loader = ctx.loaders.ProjectDependencyDBModel
        dependencies = await loader.filter_by(previous_id=id)
        return dependencies
    
    @classmethod
    async def CreateMasterProject(cls, ctx, **data) -> typing.Optional[ProjectDBModel]:
        from ..Domain_UG.RBACService import RBACService
        rbacobject_id = data.pop("rbacobject_id", None)
        # rbacobject_id = data.get("rbacobject_id")
        if rbacobject_id is None:
            rbacobject = await RBACService.Create(ctx, masterrbacobject_id=None, name="TopProject")
            rbacobject_id = rbacobject["id"]

        finance = await cls.Create(
            ctx=ctx,
            **data,
            rbacobject_id=rbacobject_id,
            masterfinance_id=None,
        )
        return finance    