from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rag import ask
from app.database import get_db

router = APIRouter()


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(request: AskRequest, db: AsyncSession = Depends(get_db)):
    answer, cache_hit = await ask(request.question, db)
    return {"answer": answer, "cache_hit": cache_hit}
