import pytest
import logging

async def financetype_insert(SchemaExecutor, financetype):
    query = """mutation financeTypeInsert(
	$mastertypeId: UUID! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$id: UUID # null, 
	$subtypes: [FinanceTypeInsertGQLModel!] # null
) {
  financeTypeInsert(
	event: {
	mastertypeId: $mastertypeId, 
	name: $name, 
	nameEn: $nameEn, 
	id: $id, 
	subtypes: $subtypes}
  ) {
    ... on FinanceTypeGQLModel { ...FinanceType }
    ... on FinanceTypeGQLModelInsertError { ...FinanceTypeGQLModelInsertError }
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

fragment FinanceType on FinanceTypeGQLModel {
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
  mastertypeId
  mastertype { __typename }
  subtypes { __typename }
  }

fragment FinanceTypeGQLModelInsertError on FinanceTypeGQLModelInsertError {
  __typename
  Entity {
  ...FinanceType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**financetype}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def financetype_update(SchemaExecutor, financetype):
    query = """mutation financeTypeUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null, 
	$nameEn: String # null
) {
  financeTypeUpdate(
	event: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name, 
	nameEn: $nameEn}
  ) {
    ... on FinanceTypeGQLModel { ...FinanceType }
    ... on FinanceTypeGQLModelUpdateError { ...Error }
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

fragment FinanceType on FinanceTypeGQLModel {
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
  mastertypeId
  mastertype { __typename }
  subtypes { __typename }
  }

fragment Error on FinanceTypeGQLModelUpdateError {
  __typename
  Entity {
  ...FinanceType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**financetype}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def financetype_delete(SchemaExecutor, financetype):
    query = """mutation financeTypeDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  financeTypeDelete(
	event: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...FinanceTypeGQLModelDeleteError
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

fragment FinanceType on FinanceTypeGQLModel {
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
  mastertypeId
  mastertype { __typename }
  subtypes { __typename }
  }

fragment FinanceTypeGQLModelDeleteError on FinanceTypeGQLModelDeleteError {
__typename
Entity {
  ...FinanceType
}
msg
code
failed
location
input
}

"""
    variable_values = {
        **financetype
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

@pytest.mark.asyncio
async def test_financetype_insert_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "superadmin"}, "valid": True},
    ])

    financetype = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "financetype type X"
        }
    result = await financetype_insert(SchemaExecutor, financetype)
    assert result.get("errors", None) is None, f"Unexpected errors: {result.get('errors', None)}"
    data = result.get("data", None)
    assert data is not None, f"Missing data: {result}"
    financetypeInsert = data.get("financeTypeInsert", None)
    assert financetypeInsert is not None, f"Missing financetypeInsert: {data}"
    __typename = financetypeInsert.get("__typename", None)
    assert __typename is not None, f"Missing __typename field in query"
    if "Error" in __typename:
        logging.info(f"op result:\n{financetypeInsert}")    
    assert financetypeInsert.get("lastchange", None) is not None, f"Missing lastchange field in query"
    assert "Error" not in __typename, f"Got Error"
    assert financetypeInsert.get("id", None) == financetype["id"], f"ID mismatch: expected {financetype['id']}, got {financetypeInsert.get('id', None)}"
    assert financetypeInsert.get("name", None) == financetype["name"], f"Name mismatch: expected {financetype['name']}, got {financetypeInsert.get('name', None)}"

    return financetypeInsert

@pytest.mark.asyncio
async def test_financetype_update_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "superadmin"}, "valid": True},
    ])

    financetype = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "financetype type X"
        }
    delta = {
        **financetype,
        "name": "financetype type Y"
    }
    inserted = await financetype_insert(SchemaExecutor, financetype)
    data = inserted.get("data", None)
    financetypeInsert = data.get("financeTypeInsert", None)
    payload = {
        **financetypeInsert,
        **delta
    }
    result = await financetype_update(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    financetypeUpdate = data.get("financeTypeUpdate", None)
    assert financetypeUpdate is not None
    logging.info(f"financetypeUpdate:\n{financetypeUpdate}")
    assert financetypeUpdate.get("id", None) is not None
    assert financetypeUpdate.get("name", None) == delta["name"]

    return financetypeUpdate

@pytest.mark.asyncio
async def test_financetype_delete(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "superadmin"}, "valid": True},
    ])

    financetype = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "financetype type X"
        }
    inserted = await financetype_insert(SchemaExecutor, financetype)
    data = inserted.get("data", None)
    financetypeInsert = data.get("financeTypeInsert", None)
    payload = {
        **financetype,
        **financetypeInsert
    }
    result = await financetype_delete(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    financetypeDelete = data.get("financeTypeDelete", None)
    assert financetypeDelete is None

    return financetypeDelete
