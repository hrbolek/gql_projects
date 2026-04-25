import typing
import sqlalchemy
import traceback
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
    async def Model(cls, ctx, **attributes) -> typing.Any:
        loader = await cls.getLoader(ctx)
        model = loader.getModel()(**attributes)
        return model
    
    @classmethod
    async def Create(cls, ctx: ServiceContext, entity, extraAttributes={}) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.insert(entity=entity, extraAttributes=extraAttributes)
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
    async def Update(cls, ctx: ServiceContext, entity, extraValues={}) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.update(entity=entity, extraValues=extraValues)
        return result
    
    @classmethod
    async def Delete(cls, ctx: ServiceContext, entity) -> typing.Any:
        loader = await cls.getLoader(ctx)
        result = await loader.delete(entity.id)
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

            tb = e.__traceback__
            filename = tb.tb_frame.f_code.co_filename
            lineno = tb.tb_lineno


            frames = traceback.extract_tb(e.__traceback__)
            origin = frames[-1]  # Get the last frame where the exception was raised
            filename = origin.filename
            lineno = origin.lineno

            code = getattr(e, "code", "unknown")
            return Error(
                msg=f"{filename}:{lineno} => {type(e).__name__}: {e} code({code})"
            )