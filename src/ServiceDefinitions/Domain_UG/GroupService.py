import typing
from uoishelpers.dataloaders.IDLoader import IDLoader

from ..BaseService import BaseService, ServiceContext

class GroupService(BaseService):
    @classmethod
    async def getLoader(cls, ctx) -> IDLoader:
        return ctx.loaders.groups
    
    @classmethod
    async def CheckExistence(cls, ctx: ServiceContext, id) -> bool:
        loader = await cls.getLoader(ctx)
        result = await loader.exists(id)
        return result
    
    @classmethod
    async def Create(cls, ctx, **data):
        raise NotImplementedError("Create method must be implemented by GroupService")
        
    @classmethod
    async def ReadById(cls, ctx, id):
        raise NotImplementedError("ReadById method must be implemented by GroupService")
    
    @classmethod
    async def ReadPage(cls, ctx, skip: int = 0, limit: int = 10, where: typing.Any = None, orderby: str = None, desc: bool = None, extendedfilter: dict= None):
        raise NotImplementedError("ReadPage method must be implemented by GroupService")    
    
    @classmethod
    async def Update(cls, ctx, id, **data):
        raise NotImplementedError("Update method must be implemented by GroupService")
    
    @classmethod
    async def Delete(cls, ctx, id):
        raise NotImplementedError("Delete method must be implemented by GroupService")