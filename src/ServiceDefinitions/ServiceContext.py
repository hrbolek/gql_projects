import dataclasses
import typing

from .Domain_UG.GroupService import GroupService as GS
from .Domain_Projects.ProjectService import ProjectService as PS
from .Domain_Projects.ProjectTypeService import ProjectTypeService as PTS
from .Domain_Projects.FinanceService import FinanceService as FS
from .Domain_Projects.FinanceTypeService import FinanceTypeService as FTS
from .Domain_Projects.FinanceTransferService import FinanceTransferService as F2FS
from ..Dataloaders import LoaderMap

@dataclasses.dataclass(frozen=True)
class ServiceRegistry:
    ProjectService: type[PS] = PS
    GroupService: type[GS] = GS
    FinanceService: type[FS] = FS
    FinanceTypeService: type[FTS] = FTS
    FinanceTransferService: type[F2FS] = F2FS
    ProjectTypeService: type[PTS] = PTS


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
    

