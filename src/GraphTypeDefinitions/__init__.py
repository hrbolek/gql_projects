import uuid
from typing import Union

import strawberry

from .BaseGQLModel import Relation, IDType
from src.GraphTypeDefinitions.Domain_UG.UserGQLModel import UserGQLModel
from src.GraphTypeDefinitions.Domain_UG.GroupGQLModel import GroupGQLModel

from .Domain_Projects import Query_Domain_Projects, Mutation_Domain_Projects

@strawberry.type(description="""Type for query root""")
class Query(
    Query_Domain_Projects
):
    pass

@strawberry.type(description="""Type for query root""")
class Mutation(
    Mutation_Domain_Projects
):
    pass


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=(UserGQLModel, GroupGQLModel, ),
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