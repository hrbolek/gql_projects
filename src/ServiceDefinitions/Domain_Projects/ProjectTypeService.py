import typing
from uoishelpers.dataloaders.IDLoader import IDLoader

from ...DBDefinitions import ProjectTypeDBModel
from ..BaseService import BaseService, ServiceContext

class ProjectTypeService(BaseService[IDLoader[ProjectTypeDBModel]]):

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[ProjectTypeDBModel]:
        return ctx.loaders.ProjectTypeDBModel

    @classmethod
    async def CreateMasterProjectType(cls, ctx, **data) -> typing.Optional[ProjectTypeDBModel]:
        from ..Domain_UG.RBACService import RBACService
        rbacobject_id = data.pop("rbacobject_id", None)
        # rbacobject_id = data.get("rbacobject_id")
        if rbacobject_id is None:
            rbacobject = await RBACService.Create(ctx, masterrbacobject_id=None, name="TopProjectType")
            rbacobject_id = rbacobject["id"]

        projecttype = await cls.Create(
            ctx=ctx,
            **data,
            rbacobject_id=rbacobject_id,
            masterprojecttype_id=None,
        )
        return projecttype
    
    # @classmethod
    # async def SubProjectTypes(cls, ctx: ServiceContext, id: typing.Union[int, str]) -> typing.List[ProjectTypeDBModel]:
    #     loader = cls.getLoader(ctx)
    #     projecttypes = await loader.filter_by(masterprojecttype_id=id)
    #     return projecttypes