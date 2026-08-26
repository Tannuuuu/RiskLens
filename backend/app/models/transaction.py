from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
from app.models.database import Base
import enum

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(50), unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    card_number = Column(String(20), nullable=False)
    merchant_id = Column(String(50), nullable=False)
    merchant_category = Column(String(50))
    location = Column(String(100))
    is_fraud = Column(Boolean, default=False)
    fraud_score = Column(Float, default=0.0)
    is_flagged = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(50), index=True, nullable=False)
    severity = Column(
    Enum(AlertSeverity, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
    nullable=False
)
    message = Column(Text, nullable=False)
    fraud_score = Column(Float, nullable=False)
    is_resolved = Column(Boolean, default=False)
    resolved_by = Column(String(100))
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(50), nullable=False)
    precision_score = Column(Float)
    recall_score = Column(Float)
    f1_score = Column(Float)
    auc_roc = Column(Float)
    trained_at = Column(DateTime(timezone=True), server_default=func.now())
    training_samples = Column(Integer)
    fraud_ratio = Column(Float)
