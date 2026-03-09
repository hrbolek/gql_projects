# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from src.DBDefinitions import BaseDBModel
from src.DBDefinitions import (
    ProjectDBModel,
    FinanceDBModel,
    ProjectTypeDBModel,
    FinanceTypeDBModel,
    ProjectDependencyDBModel,
    FinanceTransferDBModel
    
)

# def createLoaders(asyncSessionMaker):

#     def createLambda(loaderName, DBModel):
#         return lambda self: createIdLoader(asyncSessionMaker, DBModel)

#     attrs = {}

#     for DBModel in BaseModel.registry.mappers:
#         cls = DBModel.class_
#         attrs[cls.__tablename__] = property(cache(createLambda(asyncSessionMaker, cls)))
#         attrs[cls.__name__] = attrs[cls.__tablename__]
#     # attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
#     Loaders = type('Loaders', (), attrs)   
#     return Loaders()

# def createLoadersContext(asyncSessionMaker):
#     return {
#         "loaders": createLoaders(asyncSessionMaker)
#     }

from uoishelpers.dataloaders import createIdLoader
from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
from functools import cache
import src.DBDefinitions


# import time
# from typing import Any, Hashable, MutableMapping
# from collections.abc import MutableMapping as ABCMutableMapping

# class TTLFutureCache:
#     """
#     Dict-like TTL cache kompatibilní s aiodataloader interním použitím.
#     Ukládá: key -> (expires_at, value)

#     Podporuje: get/set/delete/clear, __getitem__/__setitem__/__delitem__, pop.
#     """

#     def __init__(self, ttl: float, maxsize: int = 100_000, drop_failed_futures: bool = True):
#         self.ttl = float(ttl)
#         self.maxsize = int(maxsize)
#         self.drop_failed_futures = bool(drop_failed_futures)
#         self._data = {}

#     def _now(self) -> float:
#         return time.time()

#     def _expired(self, expires_at: float) -> bool:
#         return expires_at <= self._now()

#     def _ensure_capacity(self):
#         if len(self._data) <= self.maxsize:
#             return
#         # sweep expirovaných
#         now = self._now()
#         expired = [k for k, (exp, _v) in self._data.items() if exp <= now]
#         for k in expired:
#             self._data.pop(k, None)
#         # fallback
#         if len(self._data) > self.maxsize:
#             self._data.clear()

#     def _get_live_value(self, key):
#         entry = self._data.get(key)
#         if entry is None:
#             return None
#         exp, value = entry
#         if self._expired(exp):
#             self._data.pop(key, None)
#             return None

#         if self.drop_failed_futures:
#             done = getattr(value, "done", None)
#             try:
#                 if callable(done) and done():
#                     cancelled = getattr(value, "cancelled", None)
#                     if callable(cancelled) and cancelled():
#                         self._data.pop(key, None)
#                         return None
#                     exception = getattr(value, "exception", None)
#                     if callable(exception) and exception() is not None:
#                         self._data.pop(key, None)
#                         return None
#             except Exception:
#                 pass

#         return value

#     # --- dict-like API ---
#     def __getitem__(self, key):
#         value = self._get_live_value(key)
#         if value is None:
#             raise KeyError(key)
#         return value

#     def __setitem__(self, key, value):
#         self._ensure_capacity()
#         self._data[key] = (self._now() + self.ttl, value)

#     def __delitem__(self, key):
#         self._data.pop(key, None)

#     def __contains__(self, key):
#         return self._get_live_value(key) is not None

#     # --- aiodataloader-like API ---
#     def get(self, key, default=None):
#         value = self._get_live_value(key)
#         return default if value is None else value

#     def set(self, key, value):
#         self.__setitem__(key, value)

#     def delete(self, key):
#         self.__delitem__(key)

#     def clear(self):
#         self._data.clear()

#     # --- tohle ti chybělo ---
#     def pop(self, key, default=None):
#         """
#         aiodataloader používá pop() pro odebrání z cache.
#         Chová se jako dict.pop: vrátí value (nebo default), položku odstraní.
#         Pokud je položka expirovaná, vrátí default a odstraní ji.
#         """
#         value = self._get_live_value(key)
#         # _get_live_value může sám expirované odstranit, ale když je live, musíme odstranit teď:
#         self._data.pop(key, None)
#         return default if value is None else value

# shared_cache = None # TTLFutureCache(10, maxsize=100_000)
# # shared_cache = TTLFutureCache(10, maxsize=100_000)

class LoaderMap(LoaderMapBase[BaseDBModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseDBModel

    ProjectDBModel: IDLoader[src.DBDefinitions.ProjectDBModel] = None
    FinanceDBModel: IDLoader[src.DBDefinitions.FinanceDBModel] = None
    ProjectTypeDBModel: IDLoader[src.DBDefinitions.ProjectTypeDBModel] = None
    FinanceTypeDBModel: IDLoader[src.DBDefinitions.FinanceTypeDBModel] = None
    ProjectDependencyDBModel: IDLoader[src.DBDefinitions.ProjectDependencyDBModel] = None
    FinanceTransferDBModel: IDLoader[src.DBDefinitions.FinanceTransferDBModel] = None
    
    def __init__(self, session):
        super().__init__(session)
        self.ProjectDBModel = self.get(ProjectDBModel)
        self.FinanceDBModel = self.get(FinanceDBModel)
        self.ProjectTypeDBModel = self.get(ProjectTypeDBModel)
        self.FinanceTypeDBModel = self.get(FinanceTypeDBModel)
        self.ProjectDependencyDBModel = self.get(ProjectDependencyDBModel)
        self.FinanceTransferDBModel = self.get(FinanceTransferDBModel)
        
        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }

def getLoadersFromInfo(info) -> LoaderMap:
    return info.context["loaders"]