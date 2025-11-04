from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from server.src.db.base import Base

class Ballot(Base):
    __tablename__ = "ballots"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    # 🆕 Identifiant de la session de vote
    session_id = Column(String, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Un seul vote par utilisateur et par session
    __table_args__ = (
        UniqueConstraint("user_id", "session_id", name="uq_ballot_user_session"),
    )

    user = relationship("User", back_populates="ballots")
    ranks = relationship("PreferenceRank", back_populates="ballot", cascade="all, delete-orphan")


class PreferenceRank(Base):
    __tablename__ = "preference_ranks"

    id = Column(Integer, primary_key=True)
    ballot_id = Column(Integer, ForeignKey("ballots.id", ondelete="CASCADE"), index=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activity.id", ondelete="CASCADE"), index=True, nullable=False)
    rank = Column(Integer, nullable=False)  # 1 = préféré, 2 = second, etc.

    __table_args__ = (
        UniqueConstraint("ballot_id", "activity_id", name="uq_rank_ballot_activity"),
        UniqueConstraint("ballot_id", "rank", name="uq_rank_ballot_rank"),
    )

    ballot = relationship("Ballot", back_populates="ranks")
    activity = relationship("Activity")
