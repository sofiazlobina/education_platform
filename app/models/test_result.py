from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime, func
from app.core.database import Base

class UserTestResult(Base):
    __tablename__ = "user_test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now())