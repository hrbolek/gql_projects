import dataclasses
import typing

from ..Dataloaders import LoaderMap

if typing.TYPE_CHECKING:
    from .Domain_UG.GroupService import GroupService as GS
    from .Domain_Projects.ProjectService import ProjectService as PS
    from .Domain_Projects.ProjectTypeService import ProjectTypeService as PTS
    from .Domain_Projects.ProjectDependencyService import ProjectDependencyService as PDS
    from .Domain_Projects.FinanceService import FinanceService as FS
    from .Domain_Projects.FinanceTypeService import FinanceTypeService as FTS
    from .Domain_Projects.FinanceTransferService import FinanceTransferService as F2FS

@dataclasses.dataclass(frozen=True)
class ServiceRegistry:

    @property
    def ProjectService(self) -> type["PS"]:
        from .Domain_Projects.ProjectService import ProjectService as PS
        return PS
    
    @property
    def ProjectTypeService(self) -> type["PTS"]:
        from .Domain_Projects.ProjectTypeService import ProjectTypeService as PTS
        return PTS
    
    @property
    def ProjectDependencyService(self) -> type["PDS"]:
        from .Domain_Projects.ProjectDependencyService import ProjectDependencyService as PDS
        return PDS
    
    @property
    def GroupService(self) -> type["GS"]:
        from .Domain_UG.GroupService import GroupService as GS
        return GS
    
    @property
    def FinanceService(self) -> type["FS"]:
        from .Domain_Projects.FinanceService import FinanceService as FS
        return FS
    
    @property
    def FinanceTypeService(self) -> type["FTS"]:
        from .Domain_Projects.FinanceTypeService import FinanceTypeService as FTS
        return FTS  
    
    @property
    def FinanceTransferService(self) -> type["F2FS"]:
        from .Domain_Projects.FinanceTransferService import FinanceTransferService as F2FS
        return F2FS
    


SERVICES = ServiceRegistry()

@dataclasses.dataclass
class ServiceContext:
    # sem pride cokoliv, co chcete mit k dispozici v resolverech a mutacich, napr. dataloadery, informace o prihlasenem uzivateli, atd.
    # vsechny tyto informace budou dostupne v resolverech a mutacich pres info.context
    # info.context je instance teto tridy, tedy ServiceContext
    # pokud budete chtit mit v resolverech a mutacich pristup k dataloaderum, muzete do teto tridy pridat property "loaders" a tam dat svoje dataloadery
    # pak se k nim dostanete v resolverech a mutacich pres info.context.loaders


    loaders: LoaderMap
    user: typing.Any = None
    ug_client: typing.Callable[..., typing.Awaitable[typing.Any]] = None
    request: typing.Any = None

    Services: ServiceRegistry = SERVICES
    

