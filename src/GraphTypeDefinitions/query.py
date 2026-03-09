
import strawberry

from .FinanceGQLModel import (
    FinanceGQLModel, FinanceQuery
)
from .ProjectGQLModel import (
    ProjectGQLModel, ProjectQuery
)
from .ProjectDependencyGQLModel import (
    ProjectDependencyGQLModel, ProjectDependencyQuery
)
from .ProjectTypeGQLModel import (
    ProjectTypeGQLModel, ProjectTypeQuery
)
from .FinanceTypeGQLModel import (  
    FinanceTypeGQLModel, FinanceTypeQuery
)
from .FinanceTransferGQLModel import (
    FinanceTransferGQLModel, FinanceTransferQuery
)

@strawberry.type(description="""Type for query root""")
class Query(
    FinanceQuery, 
    ProjectQuery,
    ProjectDependencyQuery,
    ProjectTypeQuery,
    FinanceTypeQuery,
    FinanceTransferQuery
):

    pass
