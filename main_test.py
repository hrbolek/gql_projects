import os
import json
import html
from fastapi import Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from strawberry.fastapi import GraphQLRouter
from src.GraphTypeDefinitions import schema, IDType

from main_base import app, RunOnceAndReturnSessionMaker

available_users = [
    {
        "id": "51d101a0-81f1-44ca-8366-6cf51432e8d6",
        "fullname": "Zdeňka Šimečková",
        "email": "Zdenka.Simeckova@world.com",
        "roles": [
            {
                "valid": True,
                "group": {
                    "id": "d75d64a4-bf5f-43c5-9c14-8fda7aff6c09",
                    "name": "Univerzita"
                },
                "roletype": {
                    "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                    "name": "administrátor"
                }
            },
            {
                "valid": True,
                "group": {
                    "id": "119086b2-d24d-43fe-89f3-d5365e5ad7e7",
                    "name": "Fakulta vojenské přípravy"
                },
                "roletype": {
                    "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                    "name": "zpracovatel gdpr"
                }
            }
        ]
    },
    {
        "id": "3a448039-ed98-4c43-8168-5d91a84638ac",
        "fullname": "Zdeňka Nikdo",
        "email": "Zdenka.Nikdo@world.com",
        "roles": []
    }
]

current_user = {
    "id": "51d101a0-81f1-44ca-8366-6cf51432e8d6",
    "fullname": "Zdeňka Šimečková",
    "email": "Zdenka.Simeckova@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "d75d64a4-bf5f-43c5-9c14-8fda7aff6c09",
                "name": "Univerzita"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "119086b2-d24d-43fe-89f3-d5365e5ad7e7",
                "name": "Fakulta vojenské přípravy"
            },
            "roletype": {
                "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                "name": "zpracovatel gdpr"
            }
        }
    ]
}

@app.post("/user/{id}")
async def manage_user(id: str, request: Request):
    # TODO read request to overwrite current_user and return new page 
    global current_user
    user = next(filter(lambda u: u.get("id", None) ==id, available_users), None)
    if user:
        current_user = user
    return JSONResponse(content=current_user)

@app.post("/user")
async def manage_user(request: Request):
    return JSONResponse(content=available_users)

@app.get("/user")
async def manage_user():

    path = os.path.realpath("./src/Htmls/user.html")

    with open(path, encoding="utf-8") as f:
        html = f.read()

    html = html.replace(
        "__CURRENT_USER_JSON__",
        json.dumps(current_user, ensure_ascii=False)
    )

    return HTMLResponse(content=html)


from src.GraphTypeDefinitions import WhoAmIExtension, RolePermissionSchemaExtension
class WhoAmIExtension_Debug(WhoAmIExtension):
    async def on_execute(self):
        query = self.execution_context.query
        # print(f"Executing {query}")

        self.execution_context.context["user"] = current_user
        self.execution_context.context["ug_client"] = self.ug_query

        # print("->on_execute", self.execution_context.query, flush=True)
        yield
        # print("on_execute->", whoami, flush=True)

class RolePermissionSchemaExtension_Debug(RolePermissionSchemaExtension):
    async def load(self, key):
        response = {
            "result": current_user.get("roles", [])
        }
        return response

    async def on_execute(self):
        context = self.execution_context
        context.context["userRolesForRBACQuery_loader"] = self

        yield None

schema.extensions = list(
    filter(
        lambda ex: ex not in [WhoAmIExtension, RolePermissionSchemaExtension],
        schema.extensions
    )
)

schema.extensions = [
    WhoAmIExtension_Debug, 
    RolePermissionSchemaExtension_Debug, 
    *schema.extensions
]