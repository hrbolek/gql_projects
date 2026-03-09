import pytest
import logging

async def project_insert(SchemaExecutor, project):
    query = """mutation projectInsert(
	$masterprojectId: UUID! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$description: String # null, 
	$done: Boolean # null, 
	$id: UUID # null, 
	$subprojects: [ProjectInsertGQLModel!] # null, 
	$projectTypeId: UUID # null
) {
  projectInsert(
	project: {
	masterprojectId: $masterprojectId, 
	name: $name, 
	nameEn: $nameEn, 
	description: $description, 
	done: $done, 
	id: $id, 
	subprojects: $subprojects, 
	projectTypeId: $projectTypeId}
  ) {
    ... on ProjectGQLModel { ...Project }
    ... on ProjectGQLModelInsertError { ...ProjectGQLModelInsertError }
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

fragment Project on ProjectGQLModel {
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
  done
  startdate
  enddate
  description
  masterprojectId
  masterproject { __typename }
  subprojects { __typename }
  }

fragment ProjectGQLModelInsertError on ProjectGQLModelInsertError {
  __typename
  Entity {
  ...Project
}
  msg
  failed
  code
  location
  input
  }
"""
    variable_values = {**project}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def project_update(SchemaExecutor, project):
    query = """mutation projectUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$description: String # null
) {
  projectUpdate(
	project: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name, 
	nameEn: $nameEn, 
	description: $description}
  ) {
    ... on ProjectGQLModel { ...Project }
    ... on ProjectGQLModelUpdateError { ...Error }
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

fragment Project on ProjectGQLModel {
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
  done
  startdate
  enddate
  description
  masterprojectId
  masterproject { __typename }
  subprojects { __typename }
  }

fragment Error on ProjectGQLModelUpdateError {
  __typename
  Entity {
  ...Project
}
  msg
  failed
  code
  location
  input
  }
"""
    variable_values = {**project}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def project_delete(SchemaExecutor, project):
    query = """mutation projectDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  projectDelete(
	project: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...ProjectGQLModelDeleteError
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

fragment Project on ProjectGQLModel {
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
  done
  startdate
  enddate
  description
  masterprojectId
  masterproject { __typename }
  subprojects { __typename }
  }

fragment ProjectGQLModelDeleteError on ProjectGQLModelDeleteError {
__typename
Entity {
  ...Project
}
msg
code
failed
location
input
}

"""
    variable_values = {
        **project
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

@pytest.mark.asyncio
async def test_project_insert_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ])

    project = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterprojectId": "ad43f501-ffc7-40e1-b6a2-a0199021e86b",
        "name": "project type X"
        }
    result = await project_insert(SchemaExecutor, project)
    assert result.get("errors", None) is None, f"Unexpected errors: {result.get('errors', None)}"
    data = result.get("data", None)
    assert data is not None, f"Missing data: {result}"
    projectInsert = data.get("projectInsert", None)
    assert projectInsert is not None, f"Missing projectInsert: {data}"
    __typename = projectInsert.get("__typename", None)
    assert __typename is not None, f"Missing __typename field in query"
    if "Error" in __typename:
        logging.info(f"op result:\n{projectInsert}")    
    assert projectInsert.get("lastchange", None) is not None, f"Missing lastchange field in query"
    assert "Error" not in __typename, f"Got Error"
    assert projectInsert.get("id", None) == project["id"], f"ID mismatch: expected {project['id']}, got {projectInsert.get('id', None)}"
    assert projectInsert.get("name", None) == project["name"], f"Name mismatch: expected {project['name']}, got {projectInsert.get('name', None)}"

    return projectInsert

@pytest.mark.asyncio
async def test_project_update_success(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ])

    project = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterprojectId": "ad43f501-ffc7-40e1-b6a2-a0199021e86b",
        "name": "project type X"
        }
    delta = {
        **project,
        "name": "project type Y"
    }
    inserted = await project_insert(SchemaExecutor, project)
    data = inserted.get("data", None)
    projectInsert = data.get("projectInsert", None)
    payload = {
        **projectInsert,
        **delta
    }
    result = await project_update(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    projectUpdate = data.get("projectUpdate", None)
    assert projectUpdate is not None
    logging.info(f"projectUpdate:\n{projectUpdate}")
    assert projectUpdate.get("id", None) is not None
    assert projectUpdate.get("name", None) == delta["name"]

    return projectUpdate

@pytest.mark.asyncio
async def test_project_delete(SchemaExecutor, FullContext):
    userRolesForRBACQuery_patch = FullContext["userRolesForRBACQuery_patch"]
    userRolesForRBACQuery_patch([
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ])

    project = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterprojectId": "ad43f501-ffc7-40e1-b6a2-a0199021e86b",
        "name": "project type X"
        }
    inserted = await project_insert(SchemaExecutor, project)
    data = inserted.get("data", None)
    projectInsert = data.get("projectInsert", None)
    payload = {
        **project,
        **projectInsert
    }
    result = await project_delete(SchemaExecutor, payload)
    assert result.get("errors", None) is None
    data = result.get("data", None)
    assert data is not None
    projectDelete = data.get("projectDelete", None)
    assert projectDelete is None

    return projectDelete
