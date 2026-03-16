
import strawberry

from .Domain_Projects.FinanceGQLModel import (
    FinanceGQLModel, FinanceQuery, FinanceMutation
)
from .Domain_Projects.ProjectGQLModel import (
    ProjectGQLModel, ProjectQuery, ProjectMutation
)
from .Domain_Projects.ProjectDependencyGQLModel import (
    ProjectDependencyGQLModel, ProjectDependencyQuery, ProjectDependencyMutation
)
from .Domain_Projects.ProjectTypeGQLModel import (
    ProjectTypeGQLModel, ProjectTypeQuery, ProjectTypeMutation
)
from .Domain_Projects.FinanceTypeGQLModel import (  
    FinanceTypeGQLModel, FinanceTypeQuery, FinanceTypeMutation
)
from .Domain_Projects.FinanceTransferGQLModel import (
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
