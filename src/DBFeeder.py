from src.DBDefinitions import (
    ProjectDBModel,
    ProjectTypeDBModel,
    FinanceDBModel,
    FinanceTypeDBModel,
    ProjectDependencyDBModel,
    FinanceTransferDBModel
)

import uuid
import random
import itertools

from functools import cache


# from sqlalchemy.future import select


# def singleCall(asyncFunc):
#     """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
#     Dekorovana funkce je asynchronni.
#     """
#     resultCache = {}

#     async def result():
#         if resultCache.get("result", None) is None:
#             resultCache["result"] = await asyncFunc()
#         return resultCache["result"]

#     return result


# ###########################################################################################################################
# #
# # zde definujte sve funkce, ktere naplni random data do vasich tabulek
# #
# ###########################################################################################################################
# def get_demodata(asyncSessionMaker):
#     pass


# def determineProjectTypes():
#     """Definuje zakladni typy roli"""
#     projectTypes = [
#         {"name": "shortTerm"},
#         {"name": "mediumTerm"},
#         {"name": "longTerm"},
#     ]
#     return projectTypes


# def determineFinanceTypes():
#     """Definuje zakladni typy financi"""
#     financeTypes = [
#         {"name": "travel_expenses"},
#         {"name": "accomodation_expenses"},
#         {"name": "other_expenses"},
#     ]
#     return financeTypes


# def randomProject(name):
#     """Náhodný projekt"""
#     result = {
#         "id": f"{uuid.uuid1()}",
#         "name": f"{name}",
#         #'startDate': randomDate()
#         #'endDate': randomDate()
#         "milestones": [
#             # randomMilestone(i+1) for i in range(random.randint(3, 5))
#         ],
#     }
#     return result


# def randomMilestone(index):
#     """Náhodný milestone"""
#     result = {
#         "name": f"Milestone {index}"
#         #'startDate': randomDate(),
#         #'endDAte' :  randomDate(),
#     }
#     return result


# def randomFinance():
#     """Náhodné finance"""
#     result = {
#         "name": "",
#         "amount": random.randint(100, 20000),
#     }
#     return result


# ###########################################################################################################################
# #
# # zde definujte sve funkce, ktere naplni random data do vasich tabulek
# #
# ###########################################################################################################################


# def randomUUID(limit):
#     userIDs = [uuid.uuid4() for _ in range(limit)]
#     return userIDs


# def randomStartDate():
#     base = date(2020, 1, 1)
#     return base + timedelta(days=random.randint(1, 50))


# def randomEndDate(startDate):
#     return startDate + timedelta(days=random.randint(50, 100))


# def randomProjectName():
#     names = ["Informacni system", "Lesaci", "Wow grind", "SPZ", "Vault of Incarnates"]
#     return random.choice(names)


# projectTypesIDs = randomUUID(3)
# financeTypesIDs = randomUUID(3)
# projectIDs = randomUUID(2)
# financeIDs = randomUUID(10)
# milestoneIDs = randomUUID(10)
# groupIDs = randomUUID(1)


# def determineProjectTypes():
#     """Definuje zakladni typy roli"""
#     projectTypes = [
#         {"id": projectTypesIDs[0], "name": "shortTerm"},
#         {"id": projectTypesIDs[1], "name": "mediumTerm"},
#         {"id": projectTypesIDs[2], "name": "longTerm"},
#     ]
#     return projectTypes


# def determineFinanceTypes():
#     """Definuje zakladni typy financi"""
#     financeTypes = [
#         {"id": financeTypesIDs[0], "name": "travelExpenses"},
#         {"id": financeTypesIDs[1], "name": "accomodationExpenses"},
#         {"id": financeTypesIDs[2], "name": "otherExpenses"},
#     ]
#     return financeTypes


# def randomProject(id):
#     """Nahodny projekt"""
#     startDate = randomStartDate()
#     return {
#         "id": id,
#         "name": randomProjectName(),
#         "startDate": startDate,
#         "endDate": randomEndDate(startDate),
#         "projectType_id": random.choice(projectTypesIDs),
#         "group_id": random.choice(groupIDs),
#     }


# def randomFinance(id, index):
#     """Nahodne finance"""
#     return {
#         "id": id,
#         "name": f"Finance {index}",
#         "amount": random.randint(100, 20000),
#         "project_id": random.choice(projectIDs),
#         "financeType_id": random.choice(financeTypesIDs),
#     }


# def randomMilestone(id, index):
#     """Nahodny milestone"""
#     return {
#         "id": id,
#         "name": f"Milestone {index}",
#         "date": randomStartDate(),
#         "project_id": random.choice(projectIDs),
#     }


# def randomGroup(id):
#     """Nahodna group"""
#     return {"id": id}


# def createDataStructureProjectTypes():
#     projectTypes = determineProjectTypes()
#     return projectTypes


# def createDataStructureFinanceTypes():
#     financeTypes = determineFinanceTypes()
#     return financeTypes


# def createDataStructureProjects():
#     projects = [randomProject(id) for id in projectIDs]
#     return projects


# def createDataStructureFinances():
#     index = 1
#     finances = []
#     for id in financeIDs:
#         finances.append(randomFinance(id, index))
#         index = index + 1

#     return finances


# def createDataStructureMilestones():
#     index = 1
#     milestones = []
#     for id in milestoneIDs:
#         milestones.append(randomMilestone(id, index))
#         index = index + 1

#     return milestones


# def createDataStructureGroups():
#     groups = [randomGroup(id) for id in groupIDs]
#     return groups


# async def randomDataStructure(session):

#     projectTypes = createDataStructureProjectTypes()
#     projectTypesToAdd = [ProjectTypeModel(**record) for record in projectTypes]
#     async with session.begin():
#         session.add_all(projectTypesToAdd)
#     await session.commit()

#     financeTypes = createDataStructureFinanceTypes()
#     financeTypesToAdd = [FinanceTypeModel(**record) for record in financeTypes]
#     async with session.begin():
#         session.add_all(financeTypesToAdd)
#     await session.commit()

#     projects = createDataStructureProjects()
#     projectsToAdd = [ProjectModel(**record) for record in projects]
#     async with session.begin():
#         session.add_all(projectsToAdd)
#     await session.commit()

#     finances = createDataStructureFinances()
#     financesToAdd = [FinanceModel(**record) for record in finances]
#     async with session.begin():
#         session.add_all(financesToAdd)
#     await session.commit()

#     milestones = createDataStructureMilestones()
#     milestonesToAdd = [MilestoneModel(**record) for record in milestones]
#     async with session.begin():
#         session.add_all(milestonesToAdd)
#     await session.commit()

#     # groups = createDataStructureGroups()
#     # groupsToAdd = [GroupModel(**record) for record in groups]
#     # async with session.begin():
#     #     session.add_all(groupsToAdd)
#     # await session.commit()



import os
import json
from uoishelpers.feeders import ImportModels
from uoishelpers.dataloaders import readJsonFile
import datetime

# def get_demodata(filename="./systemdata.json"):
#     def datetime_parser(json_dict):
#         for (key, value) in json_dict.items():
#             if key in ["startdate", "enddate", "lastchange", "created"]:
#                 if value is None:
#                     dateValueWOtzinfo = None
#                 else:
#                     try:
#                         dateValue = datetime.datetime.fromisoformat(value)
#                         dateValueWOtzinfo = dateValue.replace(tzinfo=None)
#                     except:
#                         print("jsonconvert Error", key, value, flush=True)
#                         dateValueWOtzinfo = None
                
#                 json_dict[key] = dateValueWOtzinfo
            
#             if (key in ["id", "changedby", "createdby"]) or ("_id" in key):
                
#                 if key == "outer_id":
#                     json_dict[key] = value
#                 elif value not in ["", None]:
#                     json_dict[key] = uuid.UUID(value)
#                 else:
#                     print(key, value)

#         return json_dict


#     with open(filename, "r", encoding="utf-8") as f:
#         jsonData = json.load(f, object_hook=datetime_parser)

#     return jsonData
get_demodata = lambda :readJsonFile(jsonFileName="./systemdata.json")

async def initDB(asyncSessionMaker, filename="./systemdata.json"):
    isDemo =  os.environ.get("DEMODATA", None) in ["True", "true"]
    if not isDemo:
        dbModels = [
            ProjectTypeDBModel,
            FinanceTypeDBModel,
        ]
    else:
        dbModels = [
            ProjectTypeDBModel,
            FinanceTypeDBModel,
            FinanceDBModel,
            ProjectDBModel,
            ProjectDependencyDBModel,
            FinanceTransferDBModel
        ]

    jsonData = readJsonFile(filename)
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass

async def backupDB(asyncSessionMaker, filename="./systemdata.backup.json"):
    import sqlalchemy
    import dataclasses
    import json
    # from .DBDefinitions.BaseDBModel import IDType

    dbModels = [
        ProjectTypeDBModel,
        FinanceTypeDBModel,
        ProjectDBModel,
        FinanceDBModel,
        ProjectDependencyDBModel,
        FinanceTransferDBModel
    ]
    data = []
    async with asyncSessionMaker() as session:
        for model in dbModels:
            sqlquery = sqlalchemy.select(model)
            rows = await session.execute(sqlquery)
            # vsechny radky do dict
            rowsdict = {}
            for row in rows:
                # print(row)
                asdict = dataclasses.asdict(row[0])
                id = asdict.get("id", None)
                if id is None: continue
                rowsdict[id] = asdict
            # vsechny primarní klice do ids
            ids = set(rowsdict.keys())
            todo = set()
            done = set()
            chunk_id = 0
            while len(done) < len(ids):
                for row in rowsdict.values():
                    id = row.get("id", None)
                    if id in done: continue
                    skip_this_id = False
                    for key, value in row.items():
                        if key == "id": continue
                        # if not isinstance(value, IDType): continue
                        if value is None: continue
                        if value not in ids: continue
                        if value not in done: 
                            # print(row, key, value)
                            skip_this_id = True
                            break
                            # primarni klic je zpracovatelny, nemame zavislost na nezpracovanych klicich
                    if skip_this_id: continue
                    row["_chunk"] = chunk_id
                    todo.add(id)
                print(f"{model.__tablename__} chunk {chunk_id} todo/done/all {len(todo)}/{len(done)}/{len(ids)}")
                if len(todo) == 0: break
                done = done.union(todo)
                todo = set()
                chunk_id += 1
            data.append({
                model.__tablename__: list(rowsdict.values())
            })
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=str)
    
    print("backup done", flush=True)