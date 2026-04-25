import typing
from uoishelpers.dataloaders.IDLoader import IDLoader

from ...DBDefinitions import ProjectTypeDBModel
from ..BaseService import BaseService, ServiceContext

class ProjectTypeService(BaseService[IDLoader[ProjectTypeDBModel]]):

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[ProjectTypeDBModel]:
        return ctx.loaders.ProjectTypeDBModel

    @classmethod
    async def CreateMasterProjectType(cls, ctx, entity) -> typing.Optional[ProjectTypeDBModel]:
        from ..Domain_UG.RBACService import RBACService
        rbacobject_id = entity.rbacobject_id
        # rbacobject_id = data.get("rbacobject_id")
        if rbacobject_id is None:
            rbacobject = await RBACService.Create(ctx, masterrbacobject_id=None, name="TopProjectType")
            entity.rbacobject_id = rbacobject["id"]

        projecttype = await cls.Create(
            ctx=ctx,
            entity=entity,
            extraAttributes={
                "mastertype_id": None,
            }
        )
        return projecttype
    
    # @classmethod
    # async def SubProjectTypes(cls, ctx: ServiceContext, id: typing.Union[int, str]) -> typing.List[ProjectTypeDBModel]:
    #     loader = cls.getLoader(ctx)
    #     projecttypes = await loader.filter_by(masterprojecttype_id=id)
    #     return projecttypes