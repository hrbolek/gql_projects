import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same, assert_read

async def finance_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("financeById")
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
async def test_finance_insert_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterfinanceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "finance type X"
        }
    result = await finance_insert(SchemaExecutor, CreateMutation, finance)
    finance_inserted = assert_insert(result)

    result = await finance_delete(SchemaExecutor, CreateMutation, finance_inserted)    
    finance_deleted = assert_delete(result)

@pytest.mark.asyncio
async def test_finance_update_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)
    finance = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterfinanceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "finance type X"
        }
    delta = {
        "name": "finance type Y"
    }
    result = await finance_insert(SchemaExecutor, CreateMutation, finance)
    finance_inserted = assert_insert(result)

    payload = {
        **finance_inserted,
        **delta
    }
    result = await finance_update(SchemaExecutor, CreateMutation, payload)
    finance_updated = assert_update(result)
    assert_same(delta, finance_updated)

    result = await finance_delete(SchemaExecutor, CreateMutation, finance_updated)
    finance_deleted = assert_delete(result)

@pytest.mark.asyncio
async def test_finance_delete(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "masterfinanceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "finance type X"
        }
    result = await finance_insert(SchemaExecutor, CreateMutation, finance)
    finance_inserted = assert_insert(result)

    result = await finance_delete(SchemaExecutor, CreateMutation, finance_inserted)    
    finance_deleted = assert_delete(result)
