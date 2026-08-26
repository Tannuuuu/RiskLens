from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.models.database import get_db
from app.models.schemas import (
    TransactionCreate, TransactionResponse, TransactionBatch, TransactionBatchResponse,
    AlertResponse, AlertResolve, ModelMetricsResponse, DashboardStats, TrainRequest
)
from app.models.transaction import Transaction, Alert, ModelMetrics, AlertSeverity
from app.services.transaction_service import TransactionService
from app.services.fraud_scoring_engine import FraudScoringEngine
from app.services.alert_service import AlertService
from app.ml.model import FraudModel
from app.config import get_settings

router = APIRouter()
settings = get_settings()

def get_fraud_model():
    model = FraudModel(settings.MODEL_PATH)
    try:
        model.load_model()
    except:
        pass
    return model

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction_service = TransactionService(db)
    db_transaction = transaction_service.create_transaction(transaction)
    
    fraud_model = get_fraud_model()
    if fraud_model.model:
        scoring_engine = FraudScoringEngine(fraud_model)
        features = {
            'amount': transaction.amount,
            'V1': 0, 'V2': 0, 'V3': 0, 'V4': 0, 'V5': 0,
            'V6': 0, 'V7': 0, 'V8': 0, 'V9': 0, 'V10': 0,
            'V11': 0, 'V12': 0, 'V13': 0, 'V14': 0, 'V15': 0,
            'V16': 0, 'V17': 0, 'V18': 0, 'V19': 0, 'V20': 0,
            'V21': 0, 'V22': 0, 'V23': 0, 'V24': 0, 'V25': 0,
            'V26': 0, 'V27': 0, 'V28': 0
        }
        
        fraud_score, is_fraud, is_flagged = scoring_engine.score_transaction(features)
        
        transaction_service.update_transaction_score(
            db_transaction.transaction_id,
            fraud_score,
            is_fraud,
            is_flagged
        )
        
        if is_flagged:
            alert_service = AlertService(db)
            severity = alert_service.determine_severity(fraud_score)
            alert_service.create_alert(
                db_transaction.transaction_id,
                fraud_score,
                severity,
                f"Transaction flagged with fraud score: {fraud_score:.4f}"
            )
        
        db_transaction.fraud_score = fraud_score
        db_transaction.is_fraud = is_fraud
        db_transaction.is_flagged = is_flagged
    
    return db_transaction

@router.post("/transactions/batch", response_model=TransactionBatchResponse)
async def create_batch_transactions(
    batch: TransactionBatch,
    db: Session = Depends(get_db)
):
    transaction_service = TransactionService(db)
    db_transactions = transaction_service.create_batch_transactions(batch.transactions)
    
    fraud_model = get_fraud_model()
    flagged_count = 0
    
    if fraud_model.model:
        scoring_engine = FraudScoringEngine(fraud_model)
        
        for db_txn in db_transactions:
            features = {
                'amount': db_txn.amount,
                'V1': 0, 'V2': 0, 'V3': 0, 'V4': 0, 'V5': 0,
                'V6': 0, 'V7': 0, 'V8': 0, 'V9': 0, 'V10': 0,
                'V11': 0, 'V12': 0, 'V13': 0, 'V14': 0, 'V15': 0,
                'V16': 0, 'V17': 0, 'V18': 0, 'V19': 0, 'V20': 0,
                'V21': 0, 'V22': 0, 'V23': 0, 'V24': 0, 'V25': 0,
                'V26': 0, 'V27': 0, 'V28': 0
            }
            
            fraud_score, is_fraud, is_flagged = scoring_engine.score_transaction(features)
            
            transaction_service.update_transaction_score(
                db_txn.transaction_id,
                fraud_score,
                is_fraud,
                is_flagged
            )
            
            db_txn.fraud_score = fraud_score
            db_txn.is_fraud = is_fraud
            db_txn.is_flagged = is_flagged
            
            if is_flagged:
                flagged_count += 1
                alert_service = AlertService(db)
                severity = alert_service.determine_severity(fraud_score)
                alert_service.create_alert(
                    db_txn.transaction_id,
                    fraud_score,
                    severity,
                    f"Transaction flagged with fraud score: {fraud_score:.4f}"
                )
    
    return TransactionBatchResponse(
        total=len(db_transactions),
        flagged=flagged_count,
        transactions=db_transactions
    )

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    transaction_service = TransactionService(db)
    return transaction_service.get_transactions(skip, limit)

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    transaction_service = TransactionService(db)
    transaction = transaction_service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    alert_service = AlertService(db)
    severity_enum = AlertSeverity(severity) if severity else None
    return alert_service.get_alerts(skip, limit, severity_enum, resolved)

@router.put("/alerts/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: int,
    resolve_data: AlertResolve,
    db: Session = Depends(get_db)
):
    alert_service = AlertService(db)
    alert = alert_service.resolve_alert(alert_id, resolve_data.resolved_by)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    transaction_service = TransactionService(db)
    alert_service = AlertService(db)
    
    txn_stats = transaction_service.get_transaction_stats()
    alert_stats = alert_service.get_alert_stats()
    
    return DashboardStats(
        total_transactions=txn_stats['total_transactions'],
        total_fraud=txn_stats['total_fraud'],
        fraud_rate=txn_stats['fraud_rate'],
        total_alerts=alert_stats['total_alerts'],
        unresolved_alerts=alert_stats['unresolved_alerts'],
        average_fraud_score=0.0
    )

@router.post("/model/train")
async def train_model(
    request: TrainRequest,
    db: Session = Depends(get_db)
):
    data_path = request.data_path
    if not os.path.exists(data_path):
        raise HTTPException(status_code=400, detail=f"Data file not found: {data_path}")
    
    fraud_model = FraudModel(settings.MODEL_PATH)
    metrics = fraud_model.train(data_path)
    
    model_metrics = ModelMetrics(
        model_version=metrics['model_version'],
        precision_score=metrics.get('precision'),
        recall_score=metrics.get('recall'),
        f1_score=metrics.get('f1'),
        auc_roc=metrics.get('auc_roc'),
        training_samples=metrics.get('training_samples'),
        fraud_ratio=metrics.get('fraud_ratio')
    )
    
    db.add(model_metrics)
    db.commit()
    
    return {"message": "Model trained successfully", "metrics": metrics}

@router.get("/model/metrics", response_model=List[ModelMetricsResponse])
async def get_model_metrics(db: Session = Depends(get_db)):
    return db.query(ModelMetrics).order_by(ModelMetrics.trained_at.desc()).limit(10).all()
