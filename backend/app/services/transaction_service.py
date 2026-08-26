import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, AlertSeverity
from app.models.schemas import TransactionCreate, TransactionResponse

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_transaction(self, transaction_data: TransactionCreate) -> Transaction:
        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        db_transaction = Transaction(
            transaction_id=transaction_id,
            amount=transaction_data.amount,
            card_number=transaction_data.card_number,
            merchant_id=transaction_data.merchant_id,
            merchant_category=transaction_data.merchant_category,
            location=transaction_data.location,
            timestamp=datetime.utcnow()
        )
        
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        
        return db_transaction
    
    def create_batch_transactions(self, transactions: List[TransactionCreate]) -> List[Transaction]:
        db_transactions = []
        for t in transactions:
            transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            db_transaction = Transaction(
                transaction_id=transaction_id,
                amount=t.amount,
                card_number=t.card_number,
                merchant_id=t.merchant_id,
                merchant_category=t.merchant_category,
                location=t.location,
                timestamp=datetime.utcnow()
            )
            self.db.add(db_transaction)
            db_transactions.append(db_transaction)
        
        self.db.commit()
        for t in db_transactions:
            self.db.refresh(t)
        
        return db_transactions
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).first()
    
    def get_transactions(self, skip: int = 0, limit: int = 100) -> List[Transaction]:
        return self.db.query(Transaction).offset(skip).limit(limit).all()
    
    def update_transaction_score(
        self, 
        transaction_id: str, 
        fraud_score: float, 
        is_fraud: bool,
        is_flagged: bool
    ) -> Optional[Transaction]:
        transaction = self.get_transaction(transaction_id)
        if transaction:
            transaction.fraud_score = fraud_score
            transaction.is_fraud = is_fraud
            transaction.is_flagged = is_flagged
            self.db.commit()
            self.db.refresh(transaction)
        return transaction
    
    def get_transaction_stats(self) -> dict:
        total = self.db.query(Transaction).count()
        fraud = self.db.query(Transaction).filter(Transaction.is_fraud == True).count()
        flagged = self.db.query(Transaction).filter(Transaction.is_flagged == True).count()
        
        return {
            'total_transactions': total,
            'total_fraud': fraud,
            'fraud_rate': fraud / total if total > 0 else 0,
            'flagged_transactions': flagged
        }
