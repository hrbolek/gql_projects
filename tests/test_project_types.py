import pytest
import logging

async def projecttype_insert(SchemaExecutor, projecttype):
    query = """mutation projectTypeInsert(
	$mastertypeId: UUID! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$id: UUID # null, 
	$subtypes: [ProjectTypeInsertGQLModel!] # null
) {
  projectTypeInsert(
	event: {
	mastertypeId: $mastertypeId, 
	name: $name, 
	nameEn: $nameEn, 
	id: $id, 
	subtypes: $subtypes}
  ) {
    ... on ProjectTypeGQLModel { ...ProjectType }
    ... on ProjectTypeGQLModelInsertError { ...ProjectTypeGQLModelInsertError }
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

fragment ProjectType on ProjectTypeGQLModel {
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

fragment ProjectTypeGQLModelInsertError on ProjectTypeGQLModelInsertError {
  __typename
  Entity {
  ...ProjectType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**projecttype}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def projecttype_update(SchemaExecutor, projecttype):
    query = """mutation projectTypeUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null, 
	$nameEn: String # null
) {
  projectTypeUpdate(
	event: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name, 
	nameEn: $nameEn}
  ) {
    ... on ProjectTypeGQLModel { ...ProjectType }
    ... on ProjectTypeGQLModelUpdateError { ...Error }
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

fragment ProjectType on ProjectTypeGQLModel {
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

fragment Error on ProjectTypeGQLModelUpdateError {
  __typename
  Entity {
  ...ProjectType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**projecttype}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def projecttype_delete(SchemaExecutor, projecttype):
    query = """mutation projectTypeDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  projectTypeDelete(
	event: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...ProjectTypeGQLModelDeleteError
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

fragment ProjectType on ProjectTypeGQLModel {
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

fragment ProjectTypeGQLModelDeleteError on ProjectTypeGQLModelDeleteError {
__typename
Entity {
  ...ProjectType
}
msg
code
failed
location
input
}

"""
    variable_values = {
        **projecttype
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

@pytest.mark.asyncio
async def test_projecttype_insert_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "superadmin"}, "valid": True},
    ])

    projecttype = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "projecttype type X"
        }
    result = await projecttype_insert(SchemaExecutor, projecttype)
    assert result.get("errors", None) is None, f"Unexpected errors: {result.get('errors', None)}"
    data = result.get("data", None)
    assert data is not None, f"Missing data: {result}"
    projecttypeInsert = data.get("projectTypeInsert", None)
    assert projecttypeInsert is not None, f"Missing projecttypeInsert: {data}"
    __typename = projecttypeInsert.get("__typename", None)
    assert __typename is not None, f"Missing __typename field in query"
    if "Error" in __typename:
        logging.info(f"op result:\n{projecttypeInsert}")    
    assert projecttypeInsert.get("lastchange", None) is not None, f"Missing lastchange field in query"
    assert "Error" not in __typename, f"Got Error"
    assert projecttypeInsert.get("id", None) == projecttype["id"], f"ID mismatch: expected {projecttype['id']}, got {projecttypeInsert.get('id', None)}"
    assert projecttypeInsert.get("name", None) == projecttype["name"], f"Name mismatch: expected {projecttype['name']}, got {projecttypeInsert.get('name', None)}"

    return projecttypeInsert

@pytest.mark.asyncio
async def test_projecttype_update_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "superadmin"}, "valid": True},
    ])

    projecttype = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "projecttype type X"
        }
    delta = {
        **projecttype,
        "name": "projecttype type Y"
    }
    inserted = await projecttype_insert(SchemaExecutor, projecttype)
    data = inserted.get("data", None)
    projecttypeInsert = data.get("projectTypeInsert", None)
    payload = {
        **projecttypeInsert,
        **delta
    }
    result = await projecttype_update(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    projecttypeUpdate = data.get("projectTypeUpdate", None)
    assert projecttypeUpdate is not None
    logging.info(f"projecttypeUpdate:\n{projecttypeUpdate}")
    assert projecttypeUpdate.get("id", None) is not None
    assert projecttypeUpdate.get("name", None) == delta["name"]

    return projecttypeUpdate

@pytest.mark.asyncio
async def test_projecttype_delete(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "superadmin"}, "valid": True},
    ])

    projecttype = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "projecttype type X"
        }
    inserted = await projecttype_insert(SchemaExecutor, projecttype)
    data = inserted.get("data", None)
    projecttypeInsert = data.get("projectTypeInsert", None)
    payload = {
        **projecttype,
        **projecttypeInsert
    }
    result = await projecttype_delete(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    projecttypeDelete = data.get("projectTypeDelete", None)
    assert projecttypeDelete is None

    return projecttypeDelete
