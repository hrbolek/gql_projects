
import strawberry

from .FinanceGQLModel import (
    FinanceGQLModel, FinanceQuery, FinanceMutation
)
from .ProjectGQLModel import (
    ProjectGQLModel, ProjectQuery, ProjectMutation
)
from .ProjectDependencyGQLModel import (
    ProjectDependencyGQLModel, ProjectDependencyQuery, ProjectDependencyMutation
)
from .ProjectTypeGQLModel import (
    ProjectTypeGQLModel, ProjectTypeQuery, ProjectTypeMutation
)
from .FinanceTypeGQLModel import (  
    FinanceTypeGQLModel, FinanceTypeQuery, FinanceTypeMutation
)
from .FinanceTransferGQLModel import (
    FinanceTransferGQLModel, FinanceTransferQuery, FinanceTransferMutation
)

@strawberry.type(description="""Type for query root""")
class Mutation(
    FinanceMutation, 
    ProjectMutation,
    ProjectDependencyMutation,
    ProjectTypeMutation,
    FinanceTypeMutation,
    FinanceTransferMutation
):

    pass
