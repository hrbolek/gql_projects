import asyncio
import typing
import uuid
from uoishelpers.dataloaders.IDLoader import IDLoader

from ...DBDefinitions import ProjectDependencyDBModel
from ..BaseService import BaseService, ServiceContext, ServiceExceptionWithCode

class ProjectDependencyService(BaseService[IDLoader[ProjectDependencyDBModel]]):

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[ProjectDependencyDBModel]:
        return ctx.loaders.ProjectDependencyDBModel

    @classmethod
    async def Create(cls, 
        ctx: ServiceContext, 
        previous_id: uuid.UUID,
        next_id: uuid.UUID,
        id: typing.Optional[uuid.UUID] = None,
        **data
    ) -> typing.Any:
        loader = await cls.getLoader(ctx)
        exists = await loader.filter_by(previous_id=previous_id, next_id=next_id)
        exists = list(exists)
        if exists:
            raise ServiceExceptionWithCode(f"Dependency between project {previous_id} and {next_id} already exists", code="c9d8e7f6-5432-1098-7654-321098765432")
        
        projectLoader = ctx.loaders.ProjectDBModel
        futures = [
            projectLoader.load(previous_id),
            projectLoader.load(next_id)
        ]
        (previous_project, next_project) = await asyncio.gather(*futures)
        if previous_project is None:
            raise ServiceExceptionWithCode(f"Previous project with id {previous_id} does not exist", code="f6b5e693-413a-44f0-9cc6-2538619f5ad2")
        if next_project is None:
            raise ServiceExceptionWithCode(f"Next project with id {next_id} does not exist", code="4ed51fa5-62f6-4188-97dc-f3ed074ba133")
        if previous_project.masterproject_id != next_project.masterproject_id:
            raise ServiceExceptionWithCode(f"Project {next_id} cannot depend on project {previous_id} from a different master project", code="a1b2c3d4-5678-9012-3456-789012345678")
        result = await loader.insert(
            previous_id=previous_id,
            next_id=next_id,
            id=id,
            **data
        )
        return result
