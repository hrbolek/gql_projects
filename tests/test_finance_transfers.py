import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same, assert_read, assert_typename_with_error

async def finance_transfer_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeTransferInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_transfer_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeTransferUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_transfer_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("financeTransferDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def finance_transfer_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("financeTransferById")
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

    finance_transfer = {
        "financeSourceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "financeDestinationId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "Finance Transfer"
    }
    result = await finance_transfer_insert(SchemaExecutor, CreateMutation, finance_transfer)
    finance_transfer_inserted = assert_insert(result)

    result = await finance_transfer_delete(SchemaExecutor, CreateMutation, finance_transfer_inserted)    
    finance_transfer_deleted = assert_delete(result)

@pytest.mark.asyncio
async def test_finance_type_insert_failed_amount(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance_transfer = {
        "financeSourceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "financeDestinationId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "Finance Transfer",
        "amount": 1_000_000
    }
    result = await finance_transfer_insert(SchemaExecutor, CreateMutation, finance_transfer)
    finance_transfer_inserted = assert_typename_with_error(result, code="46084b9a-324d-4751-b2fd-a5f4a8740a99")


@pytest.mark.asyncio
async def test_finance_transfer_update_success(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance_transfer = {
        "financeSourceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "financeDestinationId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "Finance Transfer"
    }
    delta = {
        "name": "Finance Transfer Updated"
    }
    result = await finance_transfer_insert(SchemaExecutor, CreateMutation, finance_transfer)
    finance_transfer_inserted = assert_insert(result)

    payload = {
        **finance_transfer_inserted,
        **delta
    }
    result = await finance_transfer_update(SchemaExecutor, CreateMutation, payload)
    finance_transfer_updated = assert_update(result)
    assert_same(delta, finance_transfer_updated)

    result = await finance_transfer_delete(SchemaExecutor, CreateMutation, finance_transfer_updated)
    finance_transfer_deleted = assert_delete(result)


@pytest.mark.asyncio
async def test_finance_transfer_delete(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    finance_transfer = {
        "financeSourceId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "financeDestinationId": "5f542217-59b6-4a73-afa5-8df74b7a1399",
        "name": "Finance Transfer"
    }
    result = await finance_transfer_insert(SchemaExecutor, CreateMutation, finance_transfer)
    finance_transfer_inserted = assert_insert(result)

    result = await finance_transfer_delete(SchemaExecutor, CreateMutation, finance_transfer_inserted)    
    finance_transfer_deleted = assert_delete(result)
