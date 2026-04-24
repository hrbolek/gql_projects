import typing
import uuid
from uoishelpers.dataloaders.IDLoader import IDLoader

from ..BaseOuterService import BaseOuterService, ServiceContext


query = """
mutation rbacInsert(
    $rbacobjectId: UUID! # null, 
	$mastergroupId: UUID! # null, 
	$name: String! # null, 
	$roles: [RoleInsertGQLModel!] # null
) {
  rbacInsert(
	rbac: {
    id: $rbacobjectId,
	mastergroupId: $mastergroupId, 
	name: $name, 
	# abbreviation: $abbreviation, 
	roles: $roles}
  ) {
    ... on RBACObjectGQLModel { __typename id }
    ... on RBACObjectGQLModelInsertError { ...RBACObjectGQLModelInsertError }
  }

}

fragment RBACObjectGQLModelInsertError on RBACObjectGQLModelInsertError {
  __typename
  
  msg
  failed
  code
  location
  input
  }

"""

class RBACService(BaseOuterService):
    

    @classmethod
    async def Create(cls, ctx, 
        id: uuid.UUID,
        masterrbacobject_id: uuid.UUID,
        name: str,
        roles: typing.List[dict] = None,
    ) -> typing.Any:
        if id is None:
            id = uuid.uuid4()
        # TODO: implement the logic to create a new RBAC entry 

        rbac_json = await RBACService.ug_client(
            ctx=ctx,
            query=query,
            variables={
                "rbacobjectId": str(id),
                "mastergroupId": str(masterrbacobject_id) if masterrbacobject_id else None,
                "name": name,
                "roles": roles or []
            }
        )
        assert "data" in rbac_json, f"Unexpected response from UG: {rbac_json}"
        assert "errors" not in rbac_json, f"Error response from UG: {rbac_json}"
        return rbac_json["data"]["rbacInsert"]
        # raise NotImplementedError("Create method must be implemented")