# models/preference.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from server.src.db.base import Base

class Ballot(Base):
    __tablename__ = "ballots"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    context_date = Column(DateTime, nullable=True)  # optionnel: date de la recherche
    created_at = Column(DateTime, default=datetime.utcnow)

    # 1 bulletin par "session" ou contexte : si tu veux limiter, ajoute unicity (user_id + context_date)
    __table_args__ = (UniqueConstraint("user_id", "context_date", name="uq_ballot_user_date"),)

    user = relationship("User", back_populates="ballots")
    ranks = relationship("PreferenceRank", back_populates="ballot", cascade="all, delete-orphan")

class PreferenceRank(Base):
    __tablename__ = "preference_ranks"
    id = Column(Integer, primary_key=True)
    ballot_id = Column(Integer, ForeignKey("ballots.id", ondelete="CASCADE"), index=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activity.id", ondelete="CASCADE"), index=True, nullable=False)
    rank = Column(Integer, nullable=False)  # 1 = préféré, 2 = second, ...

    __table_args__ = (
        UniqueConstraint("ballot_id", "activity_id", name="uq_rank_ballot_activity"),
        UniqueConstraint("ballot_id", "rank", name="uq_rank_ballot_rank"),  # pas deux activités au même rang
    )

    ballot = relationship("Ballot", back_populates="ranks")
    activity = relationship("Activity")
