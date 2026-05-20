from pgvector.sqlalchemy import Vector
from sqlalchemy import Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import TimeStampMixin


class QADocument(TimeStampMixin):
    __tablename__ = "qa_document"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[int] = mapped_column(Text)
    answer: Mapped[int] = mapped_column(Text)
    embedding: Mapped[int] = mapped_column(Vector(1536))
    