import typing
from uoishelpers.dataloaders.IDLoader import IDLoader

from ...DBDefinitions import FinanceTypeDBModel
from ..BaseService import BaseService, ServiceContext

class FinanceTypeService(BaseService[IDLoader[FinanceTypeDBModel]]):
    
    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[FinanceTypeDBModel]:
        return ctx.loaders.FinanceTypeDBModel
