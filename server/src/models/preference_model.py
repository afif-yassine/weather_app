from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from server.src.db.base import Base

class Ballot(Base):
    __tablename__ = "ballots"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "session_id", name="uq_user_session"),)

    user = relationship("User", back_populates="ballots")
    ranks = relationship("PreferenceRank", back_populates="ballot", cascade="all, delete-orphan")


class PreferenceRank(Base):
    __tablename__ = "preference_ranks"

    id = Column(Integer, primary_key=True)
    ballot_id = Column(Integer, ForeignKey("ballots.id", ondelete="CASCADE"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activity.id", ondelete="CASCADE"), nullable=False)
    rank = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("ballot_id", "activity_id", name="uq_ballot_activity"),
        UniqueConstraint("ballot_id", "rank", name="uq_ballot_rank"),
    )

    ballot = relationship("Ballot", back_populates="ranks")
    activity = relationship("Activity")
