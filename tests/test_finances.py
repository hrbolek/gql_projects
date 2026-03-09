import pytest
import logging

async def finance_insert(SchemaExecutor, finance):
    query = """mutation financeInsert(
	$masterfinanceId: UUID! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$description: String # null, 
	$value: Float # null, 
	$id: UUID # null, 
	$financeTypeId: UUID # null
) {
  financeInsert(
	finance: {
	masterfinanceId: $masterfinanceId, 
	name: $name, 
	nameEn: $nameEn, 
	description: $description, 
	value: $value, 
	id: $id, 
	financeTypeId: $financeTypeId}
  ) {
    ... on FinanceGQLModel { ...Finance }
    ... on FinanceGQLModelInsertError { ...FinanceGQLModelInsertError }
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

fragment Finance on FinanceGQLModel {
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
  path
  name
  nameEn
  description
  masterfinanceId
  masterfinance { __typename }
  subfinances { __typename }
  }

fragment FinanceGQLModelInsertError on FinanceGQLModelInsertError {
  __typename
  Entity {
  ...Finance
}
  msg
  failed
  code
  location
  input
  }"""
    variable_values = {**finance}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def finance_update(SchemaExecutor, finance):
    query = """mutation financeUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$description: String # null
) {
  financeUpdate(
	finance: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name, 
	nameEn: $nameEn, 
	description: $description}
  ) {
    ... on FinanceGQLModel { ...Finance }
    ... on FinanceGQLModelUpdateError { ...Error }
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

fragment Finance on FinanceGQLModel {
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
  path
  name
  nameEn
  description
  masterfinanceId
  masterfinance { __typename }
  subfinances { __typename }
  }

fragment Error on FinanceGQLModelUpdateError {
  __typename
  Entity {
  ...Finance
}
  msg
  failed
  code
  location
  input
  }"""
    variable_values = {**finance}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def finance_delete(SchemaExecutor, finance):
    query = """mutation financeDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  financeDelete(
	finance: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...FinanceGQLModelDeleteError
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

fragment Finance on FinanceGQLModel {
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
  path
  name
  nameEn
  description
  masterfinanceId
  masterfinance { __typename }
  subfinances { __typename }
  }

fragment FinanceGQLModelDeleteError on FinanceGQLModelDeleteError {
__typename
Entity {
  ...Finance
}
msg
code
failed
location
input
}
"""
    variable_values = {
        **finance
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

@pytest.mark.asyncio
async def test_finance_insert_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ])

    finance = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterfinanceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "finance type X"
        }
    result = await finance_insert(SchemaExecutor, finance)
    assert result.get("errors", None) is None, f"Unexpected errors: {result.get('errors', None)}"
    data = result.get("data", None)
    assert data is not None, f"Missing data: {result}"
    financeInsert = data.get("financeInsert", None)
    assert financeInsert is not None, f"Missing financeInsert: {data}"
    __typename = financeInsert.get("__typename", None)
    assert __typename is not None, f"Missing __typename field in query"
    assert financeInsert.get("lastchange", None) is not None, f"Missing lastchange field in query"
    if "Error" in __typename:
        logging.info(f"op result:\n{financeInsert}")    
    assert "Error" not in __typename, f"Got Error"
    assert financeInsert.get("id", None) == finance["id"], f"ID mismatch: expected {finance['id']}, got {financeInsert.get('id', None)}"
    assert financeInsert.get("name", None) == finance["name"], f"Name mismatch: expected {finance['name']}, got {financeInsert.get('name', None)}"

    return financeInsert

@pytest.mark.asyncio
async def test_finance_update_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ])

    finance = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterfinanceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "finance type X"
        }
    delta = {
        **finance,
        "name": "finance type Y"
    }
    inserted = await finance_insert(SchemaExecutor, finance)
    data = inserted.get("data", None)
    financeInsert = data.get("financeInsert", None)
    payload = {
        **financeInsert,
        **delta
    }
    result = await finance_update(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    financeUpdate = data.get("financeUpdate", None)
    assert financeUpdate is not None
    logging.info(f"financeUpdate:\n{financeUpdate}")
    assert financeUpdate.get("id", None) is not None
    assert financeUpdate.get("name", None) == delta["name"]

    return financeUpdate

@pytest.mark.asyncio
async def test_finance_delete(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ])

    finance = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterfinanceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "finance type X"
        }
    inserted = await finance_insert(SchemaExecutor, finance)
    data = inserted.get("data", None)
    financeInsert = data.get("financeInsert", None)
    payload = {
        **finance,
        **financeInsert
    }
    result = await finance_delete(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    financeDelete = data.get("financeDelete", None)
    assert financeDelete is None

    return financeDelete
