import uuid
from typing import Union

import strawberry

from .BaseGQLModel import Relation, IDType
from .UserGQLModel import UserGQLModel

from .FinanceGQLModel import (
    FinanceGQLModel
)
from .ProjectGQLModel import (
    ProjectGQLModel
)
from .ProjectDependencyGQLModel import (
    ProjectDependencyGQLModel
)
from .ProjectTypeGQLModel import (
    ProjectTypeGQLModel
)
from .FinanceTypeGQLModel import (  
    FinanceTypeGQLModel
)
from .FinanceTransferGQLModel import (
    FinanceTransferGQLModel
)


from .query import Query
from .mutation import Mutation

schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=(UserGQLModel, ),
    extensions=[],
    schema_directives=[Relation]    
)


from uoishelpers.schema import WhoAmIExtension, ProfilingExtension, PrometheusExtension
schema.extensions.append(WhoAmIExtension)
# schema.extensions.append(ProfilingExtension())        
# schema.extensions.append(PyInstrument())
# schema.extensions.append(PrometheusExtension(prefix="gql_facilities"))

from uoishelpers.gqlpermissions.RolePermissionSchemaExtension import RolePermissionSchemaExtension, GraphQLBatchLoader
schema.extensions.append(RolePermissionSchemaExtension)

from strawberry.extensions import ParserCache, ValidationCache

# from uoishelpers.schema.PyInstrumentHtmlExtension import PyInstrumentHtmlExtension
# schema.extensions.append(PyInstrumentHtmlExtension(enabled=True))
schema.extensions.append(ParserCache(1000))
schema.extensions.append(ValidationCache(1000))