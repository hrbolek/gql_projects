import strawberry

from .ProjectGQLModel import ProjectQuery, ProjectMutation
from .FinanceGQLModel import FinanceQuery,  FinanceMutation
from .FinanceTransferGQLModel import FinanceTransferQuery, FinanceTransferMutation
from .FinanceTypeGQLModel import FinanceTypeQuery, FinanceTypeMutation
from .ProjectTypeGQLModel import ProjectTypeQuery, ProjectTypeMutation
from .ProjectDependencyGQLModel import ProjectDependencyQuery, ProjectDependencyMutation

@strawberry.interface(description="")
class Query_Domain_Projects(
    ProjectQuery,
    FinanceQuery,
    FinanceTransferQuery,
    FinanceTypeQuery,
    ProjectTypeQuery,
    ProjectDependencyQuery,
):
    pass

@strawberry.interface(description="")
class Mutation_Domain_Projects(
    ProjectMutation,
    FinanceMutation,
    FinanceTransferMutation,
    FinanceTypeMutation,
    ProjectTypeMutation,
    ProjectDependencyMutation
):
    pass
