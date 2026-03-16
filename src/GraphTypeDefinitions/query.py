
import strawberry

from .Domain_Projects.FinanceGQLModel import (
    FinanceGQLModel, FinanceQuery
)
from .Domain_Projects.ProjectGQLModel import (
    ProjectGQLModel, ProjectQuery
)
from .Domain_Projects.ProjectDependencyGQLModel import (
    ProjectDependencyGQLModel, ProjectDependencyQuery
)
from .Domain_Projects.ProjectTypeGQLModel import (
    ProjectTypeGQLModel, ProjectTypeQuery
)
from .Domain_Projects.FinanceTypeGQLModel import (  
    FinanceTypeGQLModel, FinanceTypeQuery
)
from .Domain_Projects.FinanceTransferGQLModel import (
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
