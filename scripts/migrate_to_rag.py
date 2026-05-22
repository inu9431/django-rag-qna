import asyncio
import os
import sys

import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.core.embeddings import get_embedding
from app.models import QADocument

# bot_db 연결 (동기)
# BOT_DB_URL = "postgresql://bot_user:실제비밀번호@localhost:5433/bot_db"


async def migrate():
    # bot_db에서 데이터 읽기
    conn = await asyncpg.connect(
        host="localhost", port=5433, user="bot_user", password="Murter!67", database="bot_db"
    )
    rows = await conn.fetch("""
        SELECT question_text, ai_answer FROM archiver_qnalog
        WHERE is_verified = true
    """)
    await conn.close()

    # ragdb에 임베딩 변환해서 저장
    engine = create_async_engine(settings.database_url)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as db:
        for row in rows:
            print(f"처리중: {row['question_text'][:30]}...")
            embedding = await get_embedding(row["question_text"])
            doc = QADocument(
                question=row["question_text"],
                answer=row["ai_answer"],
                embedding=embedding,
            )
            db.add(doc)
        await db.commit()
        print(f"완료: {len(rows)}개 마이그레이션")


if __name__ == "__main__":
    asyncio.run(migrate())
