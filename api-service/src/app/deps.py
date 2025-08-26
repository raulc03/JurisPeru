from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from app.configs.config import Settings, getSettings
from app.services.rag_service import RagService


SettingsDep = Annotated[Settings, Depends(getSettings)]


@lru_cache
def get_rag_service(settings: SettingsDep):
    return RagService(settings)


RagDep = Annotated[RagService, Depends(get_rag_service)]
