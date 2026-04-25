import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same, assert_read, assert_typename_with_error

async def project_dependency_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectDependencyInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_dependency_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectDependencyUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_dependency_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectDependencyDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_dependency_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("projectDependencyById")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


default_user = {
    "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
    "roles": [
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "superadmin"}, "valid": True},
    ]
}
default_roles = {
    "result": [
        {
            "roletype": {
                "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                "name": "procesní administrátor"
            },
            "roletype": {
                "id": "5f9c9b11-496a-4047-ba61-d45e9f1cb6e5",
                "name": "administrátor"
            }
        }
    ]
}

@pytest.mark.asyncio
async def test_project_dependency_insert_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    project_dependency = {
        "nextId": "a3a7613d-f86c-43e3-a2cb-4d725807e5f4",
        "previousId": "360cd2e9-b914-4e56-bc61-19bb7a70ff63"
    }
    result = await project_dependency_insert(SchemaExecutor, CreateMutation, project_dependency)
    project_dependency_inserted = assert_insert(result)

    result = await project_dependency_delete(SchemaExecutor, CreateMutation, project_dependency_inserted)    
    project_dependency_deleted = assert_delete(result)

@pytest.mark.asyncio
async def test_project_dependency_insert_failed(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    project_dependency = {
        "previousId": "a3a7613d-f86c-43e3-a2cb-4d725807e5f4",
        "nextId": "360cd2e9-b914-4e56-bc61-19bb7a70ff63"
    }
    result = await project_dependency_insert(SchemaExecutor, CreateMutation, project_dependency)
    project_dependency_inserted = assert_typename_with_error(
        result, 
        code="3a9b8eb5-88c9-4432-9c0c-a48c53a43179"
    )


@pytest.mark.asyncio
async def test_project_dependency_update_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)


    project_dependency = {
        "nextId": "a3a7613d-f86c-43e3-a2cb-4d725807e5f4",
        "previousId": "360cd2e9-b914-4e56-bc61-19bb7a70ff63"
    }
    delta = {
    }
    result = await project_dependency_insert(SchemaExecutor, CreateMutation, project_dependency)
    project_dependency_inserted = assert_insert(result)

    payload = {
        **project_dependency_inserted,
        **delta
    }
    result = await project_dependency_update(SchemaExecutor, CreateMutation, payload)
    project_dependency_updated = assert_update(result)
    assert_same(delta, project_dependency_updated)

    result = await project_dependency_delete(SchemaExecutor, CreateMutation, project_dependency_updated)
    project_dependency_deleted = assert_delete(result)



@pytest.mark.asyncio
async def test_project_dependency_delete(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    project_dependency = {
        "nextId": "a3a7613d-f86c-43e3-a2cb-4d725807e5f4",
        "previousId": "360cd2e9-b914-4e56-bc61-19bb7a70ff63"
    }

    result = await project_dependency_insert(SchemaExecutor, CreateMutation, project_dependency)
    project_dependency_inserted = assert_insert(result)

    result = await project_dependency_delete(SchemaExecutor, CreateMutation, project_dependency_inserted)    
    project_dependency_deleted = assert_delete(result)
