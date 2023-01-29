from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import match_engine
from ..match_engine import MatchEngine

router = APIRouter()


@router.get("/")
async def match(p: str = "", match_engine: MatchEngine = Depends(match_engine)):
    if not p:
        raise HTTPException(status_code=400, detail="Query parameter `p` is required")
    return {"matches": match_engine.matches(p)}
