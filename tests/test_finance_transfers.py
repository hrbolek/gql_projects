import pytest
import logging

async def financetransfer_insert(SchemaExecutor, financetransfer):
    query = """mutation financeTransferInsert(
	$financeSourceId: UUID! # null, 
	$financeDestinationId: UUID! # null, 
	$name: String # null, 
	$amount: Float # null, 
	$id: UUID # null
) {
  financeTransferInsert(
	financeTransfer: {
	financeSourceId: $financeSourceId, 
	financeDestinationId: $financeDestinationId, 
	name: $name, 
	amount: $amount, 
	id: $id}
  ) {
    ... on FinanceTransferGQLModel { ...FinanceTransfer }
    ... on FinanceTransferGQLModelInsertError { ...FinanceTransferGQLModelInsertError }
  }
}

fragment User on UserGQLModel {
    __typename
    id
    }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
    }

fragment FinanceTransfer on FinanceTransferGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby {
  ...User
}
  changedby {
  ...User
}
  rbacobject {
  ...RBACObject
}
  name
  financeSourceId
  financeDestinationId
  amount
  financeSource {__typename id}
  financeDestination {__typename id}
  }

fragment FinanceTransferGQLModelInsertError on FinanceTransferGQLModelInsertError {
  __typename
  Entity {
  ...FinanceTransfer
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**financetransfer}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def financetransfer_update(SchemaExecutor, financetransfer):
    query = """mutation financeTransferUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null
) {
  financeTransferUpdate(
	financeTransfer: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name}
  ) {
    ... on FinanceTransferGQLModel { ...FinanceTransfer }
    ... on FinanceTransferGQLModelUpdateError { ...Error }
  }
}

fragment User on UserGQLModel {
    __typename
    id
    }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
    }

fragment FinanceTransfer on FinanceTransferGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby {
  ...User
}
  changedby {
  ...User
}
  rbacobject {
  ...RBACObject
}
  name
  financeSourceId
  financeDestinationId
  amount
  financeSource {__typename id}
  financeDestination {__typename id}
  }

fragment Error on FinanceTransferGQLModelUpdateError {
  __typename
  Entity {
  ...FinanceTransfer
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**financetransfer}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def financetransfer_delete(SchemaExecutor, financetransfer):
    query = """mutation financeTransferDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  financeTransferDelete(
	financeTransfer: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...FinanceTransferGQLModelDeleteError
}
}

fragment User on UserGQLModel {
    __typename
    id
    }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
    }

fragment FinanceTransfer on FinanceTransferGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby {
  ...User
}
  changedby {
  ...User
}
  rbacobject {
  ...RBACObject
}
  name
  financeSourceId
  financeDestinationId
  amount
  financeSource {__typename id}
  financeDestination {__typename id}
  }

fragment FinanceTransferGQLModelDeleteError on FinanceTransferGQLModelDeleteError {
__typename
Entity {
  ...FinanceTransfer
}
msg
code
failed
location
input
}

"""
    variable_values = {
        **financetransfer
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

@pytest.mark.asyncio
async def test_financetransfer_insert_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
    ])

    financetransfer = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "name": "financetransfer transfer X",
        "financeSourceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "financeDestinationId": "d00b9e04-6a63-484d-84be-ce16745ad3b1",
        "amount": 23000
        }
    result = await financetransfer_insert(SchemaExecutor, financetransfer)
    assert result.get("errors", None) is None, f"Unexpected errors: {result.get('errors', None)}"
    data = result.get("data", None)
    assert data is not None, f"Missing data: {result}"
    financetransferInsert = data.get("financeTransferInsert", None)
    assert financetransferInsert is not None, f"Missing financetransferInsert: {data}"
    __typename = financetransferInsert.get("__typename", None)
    assert __typename is not None, f"Missing __typename field in query"
    if "Error" in __typename:
        logging.info(f"op result:\n{financetransferInsert}")    
    assert financetransferInsert.get("lastchange", None) is not None, f"Missing lastchange field in query"
    assert "Error" not in __typename, f"Got Error"
    assert financetransferInsert.get("id", None) == financetransfer["id"], f"ID mismatch: expected {financetransfer['id']}, got {financetransferInsert.get('id', None)}"
    assert financetransferInsert.get("name", None) == financetransfer["name"], f"Name mismatch: expected {financetransfer['name']}, got {financetransferInsert.get('name', None)}"

    return financetransferInsert

@pytest.mark.asyncio
async def test_financetransfer_update_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
    ])

    financetransfer = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "name": "financetransfer transfer X",
        "financeSourceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "financeDestinationId": "d00b9e04-6a63-484d-84be-ce16745ad3b1",
        "amount": 23000
        }
    delta = {
        **financetransfer,
        "name": "financetransfer transfer Y"
    }
    inserted = await financetransfer_insert(SchemaExecutor, financetransfer)
    data = inserted.get("data", None)
    financetransferInsert = data.get("financeTransferInsert", None)
    payload = {
        **financetransferInsert,
        **delta
    }
    result = await financetransfer_update(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    financetransferUpdate = data.get("financeTransferUpdate", None)
    assert financetransferUpdate is not None
    logging.info(f"financetransferUpdate:\n{financetransferUpdate}")
    assert financetransferUpdate.get("id", None) is not None
    assert financetransferUpdate.get("name", None) == delta["name"]

    return financetransferUpdate

@pytest.mark.asyncio
async def test_financetransfer_delete(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
    ])

    financetransfer = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "name": "financetransfer transfer X",
        "financeSourceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "financeDestinationId": "d00b9e04-6a63-484d-84be-ce16745ad3b1",
        "amount": 23000
        }
    inserted = await financetransfer_insert(SchemaExecutor, financetransfer)
    data = inserted.get("data", None)
    financetransferInsert = data.get("financeTransferInsert", None)
    payload = {
        **financetransfer,
        **financetransferInsert
    }
    result = await financetransfer_delete(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    financetransferDelete = data.get("financeTransferDelete", None)
    assert financetransferDelete is None

    return financetransferDelete
