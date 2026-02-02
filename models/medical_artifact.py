from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base


class MedicalArtifact(Base):
    __tablename__ = "medical_artifacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    source = Column(String, default="manual")
    event_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="medical_artifacts")
