import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same, assert_read

async def project_type_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectTypeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_type_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectTypeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_type_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("projectTypeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def project_type_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("projectTypeById")
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
async def test_projecttype_insert_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)


    project_type = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "projecttype type X"
        }
    result = await project_type_insert(SchemaExecutor, CreateMutation, project_type)
    project_type_inserted = assert_insert(result)

    result = await project_type_delete(SchemaExecutor, CreateMutation, project_type_inserted)    
    project_type_deleted = assert_delete(result)


@pytest.mark.asyncio
async def test_projecttype_update_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)


    project_type = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "projecttype type X"
        }
    delta = {
        **project_type,
        "name": "projecttype type Y"
    }
    result = await project_type_insert(SchemaExecutor, CreateMutation, project_type)
    project_type_inserted = assert_insert(result)

    payload = {
        **project_type_inserted,
        **delta
    }
    result = await project_type_update(SchemaExecutor, CreateMutation, payload)
    project_type_updated = assert_update(result)
    assert_same(delta, project_type_updated)

    result = await project_type_delete(SchemaExecutor, CreateMutation, project_type_updated)
    project_type_deleted = assert_delete(result)



@pytest.mark.asyncio
async def test_projecttype_delete(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)


    project_type = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "projecttype type X"
        }
    result = await project_type_insert(SchemaExecutor, CreateMutation, project_type)
    project_type_inserted = assert_insert(result)

    result = await project_type_delete(SchemaExecutor, CreateMutation, project_type_inserted)    
    project_type_deleted = assert_delete(result)
