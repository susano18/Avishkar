"""
FilterResult ORM model.

Stores the output of the two-stage Syllabus Filter pipeline — the identified
syllabus topics (Stage 1) and the filtered notes (Stage 2), along with
references to the source documents and the LLM model used.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.database import Base


class FilterResult(Base):
    """
    Represents the output of a Syllabus Filter operation.

    Links back to the source syllabus and notes documents, and stores
    the LLM-generated topic list and filtered notes.

    Attributes:
        id: Unique identifier (UUID).
        user_id: Foreign key to the user who initiated the filter.
        syllabus_doc_id: Foreign key to the syllabus document.
        notes_doc_id: Foreign key to the notes document.
        identified_topics: Stage 1 structured topic list.
        filtered_notes: Stage 2 filtered notes for relevance.
        model_used: Identifier of the LLM model used.
        processing_time_seconds: Total time for filter operation.
        created_at: Timestamp of result creation.
    """

    __tablename__ = "filter_results"

    # Optimization: Composite index for paginated history queries
    # (WHERE user_id = ? ORDER BY created_at DESC)
    # This avoids a separate sort operation in the database.
    __table_args__ = (
        Index("idx_filter_results_user_created", "user_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    syllabus_doc_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True
    )
    notes_doc_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True
    )
    identified_topics: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    filtered_notes: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    model_used: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    processing_time_seconds: Mapped[Optional[float]] = mapped_column(
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    owner = relationship("User", back_populates="filter_results")
    syllabus_document = relationship(
        "Document", foreign_keys=[syllabus_doc_id]
    )
    notes_document = relationship(
        "Document", foreign_keys=[notes_doc_id]
    )

    def __repr__(self) -> str:
        return f"<FilterResult(id={self.id}, model={self.model_used})>"
