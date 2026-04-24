import typing
import sqlalchemy
from uoishelpers.dataloaders.IDLoader import IDLoader

from .ServiceContext  import ServiceContext

T = typing.TypeVar("T", bound=IDLoader)

class ServiceExceptionWithCode(Exception):
    def __init__(self, msg: str, code: typing.Union[str, int] = "unknown"):
        super().__init__(msg)
        self.code = code

class BaseService(typing.Generic[T]):

    @classmethod
    async def getLoader(cls, ctx) -> T:
        # return T
        raise NotImplementedError("getLoader method must be implemented by subclass of BaseService")
    
    @classmethod
    async def Create(cls, ctx: ServiceContext, **data) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.insert(**data)
        return result
        
    @classmethod
    async def ReadById(cls, ctx: ServiceContext, id) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.load(id)
        return result
    
    @classmethod
    async def ReadPage(
        cls, 
        ctx: ServiceContext, 
        skip: int = 0, 
        limit: int = 10, 
        where: typing.Any = None,
        orderby: str = None,
        desc: bool = None,
        extendedfilter: dict= None
    ) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.page(
            skip=skip, 
            limit=limit, 
            where=where,
            orderby=orderby,
            desc=desc,
            extendedfilter=extendedfilter
        )
        return result
    
    @classmethod
    async def Update(cls, ctx: ServiceContext, id, **data) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.update(id, **data)
        return result
    
    @classmethod
    async def Delete(cls, ctx: ServiceContext, id) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.delete(id)
        return result

    @classmethod
    async def ExecuteServiceMethod(
        cls, 
        coroutine, 
        *, 
        Error,
        OK
    ):
        try:
            result = await coroutine
            return OK(result=result)
        except sqlalchemy.exc.SQLAlchemyError as e:
            return Error(
                msg=f"Database error: {e} code({e.code})"
            )
        except Exception as e:
            code = getattr(e, "code", "unknown")
            return Error(
                msg=f"Exception {e} code({e.code})"
            )