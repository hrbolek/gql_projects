import pytest
import logging


from .asserts import assert_insert, assert_update, assert_delete, assert_same, assert_read

async def finance_type_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeTypeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_type_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeTypeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_type_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeTypeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_type_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("financeTypeById")
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
async def test_finance_type_insert_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance_type = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "finance_type type X"
        }
    result = await finance_type_insert(SchemaExecutor, CreateMutation, finance_type)
    finance_type_inserted = assert_insert(result)

    result = await finance_type_delete(SchemaExecutor, CreateMutation, finance_type_inserted)    
    finance_type_deleted = assert_delete(result)

@pytest.mark.asyncio
async def test_finance_type_update_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance_type = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "finance_type type X"
        }
    delta = {
        "name": "finance_type type Y"
    }
    result = await finance_type_insert(SchemaExecutor, CreateMutation, finance_type)
    finance_type_inserted = assert_insert(result)

    payload = {
        **finance_type_inserted,
        **delta
    }
    result = await finance_type_update(SchemaExecutor, CreateMutation, payload)
    finance_type_updated = assert_update(result)
    assert_same(delta, finance_type_updated)

    result = await finance_type_delete(SchemaExecutor, CreateMutation, finance_type_updated)
    finance_type_deleted = assert_delete(result)



@pytest.mark.asyncio
async def test_finance_type_delete(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance_type = {
        "id": "527f6169-a788-4757-8ad0-79f7348e0174", 
        "mastertypeId": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "name": "finance_type type X"
        }
    result = await finance_type_insert(SchemaExecutor, CreateMutation, finance_type)
    finance_type_inserted = assert_insert(result)

    result = await finance_type_delete(SchemaExecutor, CreateMutation, finance_type_inserted)    
    finance_type_deleted = assert_delete(result)
