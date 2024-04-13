# efektivní načítání dat z databáze, třída Loaders obsahuje vlastnosti pro načítací funkce pro jednotlivé modely, 
# a tyto načítací funkce jsou optimalizovány pro efektivní práci s databází a snižují počet dotazů na databázi.
import datetime
import aiohttp
import asyncio
import logging
from sqlalchemy import select
from functools import cache
import os

from aiodataloader import DataLoader

from src.DBDefinitions import ProjectCategoryModel, ProjectTypeModel, ProjectModel, MilestoneModel, MilestoneLinkModel, FinanceCategory, FinanceTypeModel, FinanceModel, StatementOfWorkModel
from uoishelpers.dataloaders import createIdLoader
from uoishelpers.dataloaders import createIdLoader as createLoader

dbmodels = {
     "projectcategories": ProjectCategoryModel,
     "projecttypes": ProjectTypeModel,
     "projects": ProjectModel,
     "milestones": MilestoneModel,
     "milestonelinks": MilestoneLinkModel,
     "financecategory": FinanceCategory,
     "financetypes": FinanceTypeModel,
     "finances": FinanceModel,
     "statementofwork": StatementOfWorkModel,
}


@cache
def composeAuthUrl():
    hostname = os.environ.get("AUTHURL", "http://localhost:8088/gql")
    assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
    assert "." not in hostname, "security check failed, change source code"
    return hostname


class AuthorizationLoader(DataLoader):

    query = """query($id: UUID!){result: rbacById(id: $id) {roles {user { id } group { id } roletype { id }}}}"""
            # variables = {"id": rbacobject}

    roleUrlEndpoint=None#composeAuthUrl()
    def __init__(self,
        roleUrlEndpoint=roleUrlEndpoint,
        query=query,
        demo=True):
        super().__init__(cache=True)
        self.roleUrlEndpoint = roleUrlEndpoint if roleUrlEndpoint else composeAuthUrl()
        self.query = query
        self.demo = demo
        self.authorizationToken = ""

    def setTokenByInfo(self, info):
        self.authorizationToken = ""
     
    # async def _load(self, id):
    #     variables = {"id": f"{id}"}
    #     if self.authorizationToken != "":
    #         headers = {"authorization": f"Bearer {self.authorizationToken}"}
    #     else:
    #         headers = {}
    #     json = {
    #         "query": self.query,
    #         "variables": variables
    #     }
    #     roleUrlEndpoint=self.roleUrlEndpoint
    #     async with aiohttp.ClientSession() as session:
    #         print(f"query {roleUrlEndpoint} for json={json}")
    #         async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
    #             print(resp.status)
    #             if resp.status != 200:
    #                 text = await resp.text()
    #                 print(text)
    #                 return []
    #             else:
    #                 respJson = await resp.json()

    #     # print(20*"respJson")
    #     # print(respJson)
        
    #     assert respJson.get("errors", None) is None, respJson["errors"]
    #     respdata = respJson.get("data", None)
    #     assert respdata is not None, "missing data response"
    #     result = respdata.get("result", None)
    #     assert result is not None, "missing result"
    #     roles = result.get("roles", None)
    #     assert roles is not None, "missing roles"
        
    #     # print(30*"=")
    #     # print(roles)
    #     # print(30*"=")
    #     return [*roles]


    # async def batch_load_fn(self, keys):
    #     #print('batch_load_fn', keys, flush=True)
    #     reducedkeys = set(keys)
    #     awaitables = (self._load(key) for key in reducedkeys)
    #     results = await asyncio.gather(*awaitables)
    #     indexedResult = {key:result for key, result in zip(reducedkeys, results)}
    #     results = [indexedResult[key] for key in keys]
    #     return results

# def update(destination, source=None, extraValues={}):
#     """Updates destination's attributes with source's attributes.
#     Attributes with value None are not updated."""
#     if source is not None:
#         for name in dir(source):
#             if name.startswith("_"):
#                 continue
#             value = getattr(source, name)
#             if value is not None:
#                 setattr(destination, name, value)

#     for name, value in extraValues.items():
#         setattr(destination, name, value)

#     return destination


class Loaders:
    authorizations = None
    requests = None
    histories = None
    forms = None
    formtypes = None
    formcategories = None
    sections = None
    parts = None
    items = None
    itemtypes = None
    itemcategories = None
    pass

def createLoaders(asyncSessionMaker):
    class Loaders:
        
        @property
        @cache
        def projects(self):
            return createLoader(asyncSessionMaker, ProjectModel)
        
        @property
        @cache
        def finances(self):
            return createLoader(asyncSessionMaker, FinanceModel)
        
        @property
        @cache
        def financetypes(self):
            return createLoader(asyncSessionMaker, FinanceTypeModel)
        
        @property
        @cache
        def milestones(self):
            return createLoader(asyncSessionMaker, MilestoneModel)
        
        @property
        @cache
        def projecttypes(self):
            return createLoader(asyncSessionMaker, ProjectTypeModel)
        
        @property
        @cache
        def financecategory(self):
            return createLoader(asyncSessionMaker, FinanceCategory)
        
        @property
        @cache
        def projectcategories(self):
            return createLoader(asyncSessionMaker, ProjectCategoryModel)
        
        @property
        @cache
        def milestonelinks(self):
            return createLoader(asyncSessionMaker, MilestoneLinkModel)
        
        @property
        @cache
        def statementofwork(self):
            return createLoader(asyncSessionMaker, StatementOfWorkModel)
        
        @property
        @cache
        def authorizations(self):
            return AuthorizationLoader()

    return Loaders()

def getLoadersFromInfo(info) -> Loaders:
     context = info.context
     loaders = context["loaders"]
     return loaders
    #return info.context['all']

demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}

def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    user = context.get("user", None)
    if user is None:
        request = context.get("request", None)
        assert request is not None, "request is missing in context :("
        user = request.scope.get("user", None)
        assert user is not None, "missing user in context or in request.scope"
    logging.debug("getUserFromInfo", user)
    return user

def getAuthorizationToken(info):
    context = info.context
    request = context.get("request", None)
    assert request is not None, "trying to get authtoken from None request"

def createUgConnectionContext(request):
    from .gql_ug_proxy import get_ug_connection
    connection = get_ug_connection(request=request)
    return {
        "ug_connection": connection
    }

def getUgConnection(info):
    context = info.context
    print("getUgConnection.context", context)
    connection = context.get("ug_connection", None)
    return connection

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }


# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

# from src.DBDefinitions import (
#     ProjectCategoryModel,
#     ProjectTypeModel,
#     ProjectModel,
#     MilestoneModel,
#     MilestoneLinkModel,
#     FinanceCategory,
#     FinanceTypeModel,
#     FinanceModel
# )




# async def createLoaders(asyncSessionMaker, models=dbmodels):
#     def createLambda(loaderName, DBModel):
#         return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
#     attrs = {}
#     for key, DBModel in models.items():
#         attrs[key] = property(cache(createLambda(key, DBModel)))
    
#     Loaders = type('Loaders', (), attrs)   
#     return Loaders()

# from functools import cache