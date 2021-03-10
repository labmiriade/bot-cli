"""
Class for interacting with BOT APIs

This class is used for interacting with BOT's API.
"""
import json
import os
from functools import cached_property
from pathlib import Path
from typing import TypedDict, Union, Optional, List

import requests
from fcache.cache import FileCache

from . import USERNAME_ENV_VAR, PASSWORD_ENV_VAR
from .cli_utils import envorconfig

# the location of the cache dir
CACHE_DIR = os.path.join(Path.home(), ".mirbot-cache")


class Commessa(TypedDict):
    customer: str
    customerId: str
    jobId: Union[str, int]
    description: str
    flagPrepayed: bool
    flagAllowHalfhour: bool
    toBePay: bool


class Activity(TypedDict):
    jobId: Union[str, int]
    taskId: str
    description: str


class MissingRapportino(TypedDict):
    date: int
    oreGiornoRegistrate: float


class DeletedRapportino(TypedDict):
    rapportinoId: str
    customerId: str
    description: str
    jobId: str
    jobTaskId: str
    note: str
    date: int


class Rapportino(TypedDict):
    rapportinoId: int
    commessa: str
    jobId: int
    attivita: str
    jobTaskId: int
    customerId: int
    customerName: str
    date: int
    description: str
    note: str
    quantityHours: int
    quantityMinutes: int
    tecnicoId: int
    officeId: str
    flagTransfert: bool
    flagPrepay: bool
    flagPay: bool
    flagExtraHour: bool


class Bot(object):
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, use_cache: bool = True):
        self.username = username or envorconfig(USERNAME_ENV_VAR, ("creds", "username"))
        self.password = password or envorconfig(PASSWORD_ENV_VAR, ("creds", "password"))
        self.auth = (self.username, self.password)
        self.use_cache = use_cache
        self.cache = FileCache("mirbot", app_cache_dir=CACHE_DIR, flag="cs")
        self.s = requests.Session()
        self.base_url = "https://bot.miriade.it/api/jsonws"

    @cached_property
    def commesse(self) -> List[Commessa]:
        key = f"{self.user_id}~commesse"
        if self.use_cache:
            if (aux := self.cache.get(key)) is not None:
                return aux
        params = {
            "jobId": self.res_id,
        }
        url = f"{self.base_url}/rapportini.rapportino/find-active-commessa-with-residuo-by-res-id"
        res = self.s.get(url, params=params, auth=self.auth)
        aux = res.json()
        self.cache[key] = aux
        return aux

    def get_commessa(self, job_id: Union[int, str]) -> Optional[Commessa]:
        commessa = list(filter(lambda x: str(x["jobId"]) == str(job_id), self.commesse))
        return commessa[0] if len(commessa) == 1 else None

    def activities(self, job_id) -> List[Activity]:
        key = f"{self.user_id}~activities~{job_id}"
        if self.use_cache:
            if (aux := self.cache.get(key)) is not None:
                return aux
        url = f"{self.base_url}/anagrafichecore.attivita/find-by-job-id"
        params = {
            "jobId": job_id,
        }
        res = self.s.get(url, params=params, auth=self.auth)
        aux = res.json()
        self.cache[key] = aux
        return aux

    @cached_property
    def user_id(self) -> str:
        key = f"username~{self.username}~user_id"
        if self.use_cache:
            if (aux := self.cache.get(key)) is not None:
                return aux
        res = self.s.get(f"{self.base_url}/user/get-current-user", auth=self.auth).json()
        user_id = res["userId"]
        self.cache[key] = user_id
        return user_id

    @cached_property
    def res_id(self) -> str:
        key = f"{self.user_id}~res_id"
        if self.use_cache:
            if (aux := self.cache.get(key)) is not None:
                return aux
        params = {
            "userId": self.user_id,
        }
        res_id = self.s.get(
            f"{self.base_url}/anagrafichecore.tecnico/find-by-user", params=params, auth=self.auth
        ).json()["resId"]
        self.cache[key] = res_id
        return res_id

    def add_rapportino(
        self,
        job_id,
        task_id,
        descrizione: str,
        note: str,
        hours: int,
        minutes: int,
        date: int,
        office_id: str,
        flag_transfert: bool,
        flag_prepay: bool,
        flag_pay: bool,
        flag_extrahour: bool,
    ):
        commessa = list(filter(lambda x: str(x["jobId"]) == str(job_id), self.commesse))
        if len(commessa) != 1:
            print(f"{commessa=}")
            raise Exception(f"Too many commessa for {job_id=}")
        rapportino = {
            "cmd": "add",
            "quantityMinutes": minutes,
            "note": note,
            "description": descrizione,
            "flagPay": flag_pay,
            "quantityHours": hours,
            "flagTransfert": flag_transfert,
            "rapportinoDate": date,
            "flagExtraHour": flag_extrahour,
            "taskId": str(task_id),
            "jobId": str(job_id),
            "flagStatus": "",
            "tecnicoId": str(self.res_id),
            "flagPrepay": flag_prepay,
            "jobRegistered": False,
            "officeId": str(office_id),
            "entityType": "rapportino",
        }
        request_body = json.dumps({"data": [rapportino]})
        user_id = self.user_id
        url = f"{self.base_url}/rapportini.rapportino/save-rapportino-nota-spese"
        payload = {
            "requestBody": request_body,
            "userId": user_id,
        }
        self.s.post(url, data=payload, auth=self.auth)

    def get_missing(self) -> List[MissingRapportino]:
        params = {
            "resId": self.res_id,
        }
        url = f"{self.base_url}/rapportini.rapportino/get-rapportini-mancanti"
        aux = self.s.get(url, params=params, auth=self.auth)
        return aux.json()

    def get_rapportini(self, date: int) -> List[Rapportino]:
        params = {
            "tecnicoId": self.res_id,
            "date": date,
        }
        url = f"{self.base_url}/rapportini.rapportino/find-by-tecnico-date-json"
        aux = self.s.get(url, params=params, auth=self.auth)
        return aux.json()

    def delete_rapportino(self, rapportinoId: Union[str, int]) -> Optional[DeletedRapportino]:
        params = {
            "rapportinoId": rapportinoId,
        }
        url = f"{self.base_url}/rapportini.rapportino/delete-rapportino"
        res = self.s.post(url, data=params, auth=self.auth)
        aux = res.json()
        if aux == {}:
            aux = None
        return aux
