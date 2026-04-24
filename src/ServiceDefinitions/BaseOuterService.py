import typing
from uoishelpers.dataloaders.IDLoader import IDLoader

from .BaseService import BaseService, ServiceContext

class BaseOuterService(BaseService):
    
    @classmethod
    async def ug_client(cls, ctx: ServiceContext, query, **params):
        ug_client = ctx.ug_client
        return await ug_client(query=query, variables=params)

    @classmethod
    async def Create(cls, ctx, **data):
        raise NotImplementedError("Create method must be implemented")
        
    @classmethod
    async def ReadById(cls, ctx, id):
        raise NotImplementedError("ReadById method must be implemented")
    @classmethod
    async def ReadPage(cls, ctx, skip: int = 0, limit: int = 10, where: typing.Any = None, orderby: str = None, desc: bool = None, extendedfilter: dict= None):
        raise NotImplementedError("ReadPage method must be implemented")    
    
    @classmethod
    async def Update(cls, ctx, id, **data):
        raise NotImplementedError("Update method must be implemented")
    
    @classmethod
    async def Delete(cls, ctx, id):
        raise NotImplementedError("Delete method must be implemented")