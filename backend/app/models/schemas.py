from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount")
    card_number: str = Field(..., min_length=16, max_length=19)
    merchant_id: str = Field(..., min_length=1)
    merchant_category: Optional[str] = None
    location: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    transaction_id: str
    timestamp: datetime
    is_fraud: bool
    fraud_score: float
    is_flagged: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionBatch(BaseModel):
    transactions: List[TransactionCreate]

class TransactionBatchResponse(BaseModel):
    total: int
    flagged: int
    transactions: List[TransactionResponse]

class AlertResponse(BaseModel):
    id: int
    transaction_id: str
    severity: AlertSeverity
    message: str
    fraud_score: float
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AlertResolve(BaseModel):
    resolved_by: str

class ModelMetricsResponse(BaseModel):
    model_config = {"protected_namespaces": (), "from_attributes": True}

    id: int
    model_version: str
    precision_score: Optional[float]
    recall_score: Optional[float]
    f1_score: Optional[float]
    auc_roc: Optional[float]
    trained_at: datetime
    training_samples: Optional[int]
    fraud_ratio: Optional[float]

class DashboardStats(BaseModel):
    total_transactions: int
    total_fraud: int
    fraud_rate: float
    total_alerts: int
    unresolved_alerts: int
    average_fraud_score: float

class TrainRequest(BaseModel):
    data_path: Optional[str] = "data/creditcard.csv"
