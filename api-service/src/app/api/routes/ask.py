import logging
from typing import Any
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.deps import RagDep
from app.schemas.ask import AskRequest, AskResponse

router = APIRouter(prefix="/ask", tags=["ask"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=AskResponse)
async def ask(request: AskRequest, rag: RagDep) -> Any:
    try:
        if not request.stream:
            response, contexts = await rag.run_rag_pipeline(request, "mmr")
            return AskResponse(answer=response, contexts=contexts)
        else:
            return StreamingResponse(
                rag.run_rag_pipeline_stream(request, "mmr"),  # type:ignore
                media_type="text/plain",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
