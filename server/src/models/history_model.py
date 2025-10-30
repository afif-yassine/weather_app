# models/history_model.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from server.src.db.base import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activity.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relations
    user = relationship("User", back_populates="history")
    activity = relationship("Activity", back_populates="history")
