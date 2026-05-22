from pgvector.sqlalchemy import Vector
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import TimeStampMixin


class QADocument(TimeStampMixin):
    __tablename__ = "qa_document"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list] = mapped_column(Vector(1536))
