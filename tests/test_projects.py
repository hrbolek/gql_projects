import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same, assert_read

async def project_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("projectById")
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
async def test_project_insert_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)


    project = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterprojectId": "ad43f501-ffc7-40e1-b6a2-a0199021e86b",
        "name": "project type X"
        }
    result = await project_insert(SchemaExecutor, CreateMutation, project)
    project_inserted = assert_insert(result)

    result = await project_delete(SchemaExecutor, CreateMutation, project_inserted)    
    project_deleted = assert_delete(result)

@pytest.mark.asyncio
async def test_project_update_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)


    project = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterprojectId": "ad43f501-ffc7-40e1-b6a2-a0199021e86b",
        "name": "project type X"
        }
    delta = {
        "name": "project type Y"
    }
    result = await project_insert(SchemaExecutor, CreateMutation, project)
    project_inserted = assert_insert(result)

    payload = {
        **project_inserted,
        **delta
    }
    result = await project_update(SchemaExecutor, CreateMutation, payload)
    project_updated = assert_update(result)
    assert_same(delta, project_updated)

    result = await project_delete(SchemaExecutor, CreateMutation, project_updated)
    project_deleted = assert_delete(result)

@pytest.mark.asyncio
async def test_project_delete(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    project = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterprojectId": "ad43f501-ffc7-40e1-b6a2-a0199021e86b",
        "name": "project type X"
        }
    result = await project_insert(SchemaExecutor, CreateMutation, project)
    project_inserted = assert_insert(result)

    result = await project_delete(SchemaExecutor, CreateMutation, project_inserted)    
    project_deleted = assert_delete(result)
