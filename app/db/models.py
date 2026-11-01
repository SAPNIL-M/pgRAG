from datetime import datetime,timezone
from sqlalchemy import ForeignKey,String,Text,DateTime
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id:Mapped[int] = mapped_column(primary_key=True)
    filename:Mapped[str] = mapped_column(String(255))
    file_hash:Mapped[str] = mapped_column(String(64),unique=True)
    page_count:Mapped[int] = mapped_column()
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
    chunks:Mapped[list["Chunk"]] = relationship(back_populates="document",cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"

    id:Mapped[int] = mapped_column(primary_key=True)
    document_id:Mapped[int] = mapped_column(ForeignKey("documents.id",ondelete="CASCADE"),index=True)
    chunk_index:Mapped[int] = mapped_column()
    page_number:Mapped[int] = mapped_column()
    text:Mapped[str] = mapped_column(Text)
    embedding:Mapped[list[float]] = mapped_column(Vector(768))
    document:Mapped["Document"] = relationship(back_populates="chunks")