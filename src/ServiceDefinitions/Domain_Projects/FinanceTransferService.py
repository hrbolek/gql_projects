import typing
import uuid
import asyncio

from types import SimpleNamespace

from uoishelpers.dataloaders.IDLoader import IDLoader

from ...DBDefinitions import FinanceTransferDBModel
from ..BaseService import BaseService, ServiceContext, ServiceExceptionWithCode

class FinanceTransferService(BaseService[IDLoader[FinanceTransferDBModel]]):
    
    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[FinanceTransferDBModel]:
        # print(f"{list(ctx.loaders.keys())} are the available loaders in context")
        return ctx.loaders.FinanceTransferDBModel

    @classmethod
    async def TransfersFrom(cls, ctx: ServiceContext, finance_id: int) -> typing.List[FinanceTransferDBModel]:
        loader = await cls.getLoader(ctx)
        rows = await loader.filter_by(finance_destination_id=finance_id)
        return rows
    
    @classmethod
    async def TransfersTo(cls, ctx: ServiceContext, finance_id: int) -> typing.List[FinanceTransferDBModel]:
        loader = await cls.getLoader(ctx)
        rows = await loader.filter_by(finance_source_id=finance_id)
        return rows
    
    @classmethod
    async def Create(
        cls, 
        ctx: ServiceContext, 
        finance_source_id: uuid.UUID, 
        finance_destination_id: uuid.UUID,
        amount: float,
        **data
    ) -> typing.Any:
        # finance_transfer = await cls.Create(ctx, **data)
        loader = await cls.getLoader(ctx)
        finance_loader = ctx.loaders.FinanceDBModel
        futures = [
            finance_loader.load(finance_source_id),
            finance_loader.load(finance_destination_id)
        ]
        (finance_source, finance_destination) = await asyncio.gather(*futures)
        if finance_source is None:
            raise ServiceExceptionWithCode(f"Finance with id {finance_source_id} does not exist", code="f6b5e693-413a-44f0-9cc6-2538619f5ad2")
        if finance_destination is None:
            raise ServiceExceptionWithCode(f"Finance with id {finance_destination_id} does not exist", code="4ed51fa5-62f6-4188-97dc-f3ed074ba133")
        if finance_source.value < amount:
            raise ServiceExceptionWithCode(f"Finance with id {finance_source_id} does not have enough value to transfer", code="a1b2c3d4-5678-9012-3456-789012345678")
        if finance_destination.value is None:
            raise ServiceExceptionWithCode(f"Finance with id {finance_destination_id} has null value, cannot transfer to it", code="e5f6a7b8-9012-3456-7890-123456789012")
        
        await loader.update(finance_source, extraValues={"value": finance_source.value - amount})
        await loader.update(finance_destination, extraValues={"value": finance_destination.value + amount})
        finance_transfer = await loader.insert(
            entity=SimpleNamespace(
                finance_source_id=finance_source_id,
                finance_destination_id=finance_destination_id,
                amount=amount
            ),
            extraAttributes=data
        )
        return finance_transfer
    
    @classmethod
    async def Delete(cls, ctx: ServiceContext, entity) -> typing.Any:
        loader = await cls.getLoader(ctx)
        id = entity.id
        finance_transfer = await loader.load(id)
        if finance_transfer is None:
            raise ServiceExceptionWithCode(f"Finance transfer with id {id} does not exist", code="f6b5e693-413a-44f0-9cc6-2538619f5ad2")
        finance_loader = ctx.loaders.FinanceDBModel
        futures = [
            finance_loader.load(finance_transfer.finance_source_id),
            finance_loader.load(finance_transfer.finance_destination_id)
        ]
        (finance_source, finance_destination) = await asyncio.gather(*futures)
        if finance_source is None:
            raise ServiceExceptionWithCode(f"Finance with id {finance_transfer.finance_source_id} does not exist", code="f6b5e693-413a-44f0-9cc6-2538619f5ad2")
        if finance_destination is None:
            raise ServiceExceptionWithCode(f"Finance with id {finance_transfer.finance_destination_id} does not exist", code="4ed51fa5-62f6-4188-97dc-f3ed074ba133")
        if finance_destination.value < finance_transfer.amount:
            raise ServiceExceptionWithCode(f"Finance with id {finance_destination.id} does not have enough value to reverse transfer", code="a1b2c3d4-5678-9012-3456-789012345678")
        if finance_source.value is None:
            raise ServiceExceptionWithCode(f"Finance with id {finance_source.id} has null value, cannot reverse transfer to it", code="e5f6a7b8-9012-3456-7890-123456789012")
        await loader.update(finance_source, extraValues={"value": finance_source.value + finance_transfer.amount})
        await loader.update(finance_destination, extraValues={"value": finance_destination.value - finance_transfer.amount})
        await loader.delete(id)
        return None
