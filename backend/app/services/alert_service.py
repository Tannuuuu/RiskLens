from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.transaction import Alert, AlertSeverity
from app.config import get_settings

class AlertService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
    
    def create_alert(
        self, 
        transaction_id: str, 
        fraud_score: float, 
        severity: AlertSeverity,
        message: str
    ) -> Alert:
        alert = Alert(
            transaction_id=transaction_id,
            severity=severity,
            message=message,
            fraud_score=fraud_score,
            is_resolved=False
        )
        
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        
        return alert
    
    def get_alert(self, alert_id: int) -> Optional[Alert]:
        return self.db.query(Alert).filter(Alert.id == alert_id).first()
    
    def get_alerts(
        self, 
        skip: int = 0, 
        limit: int = 100,
        severity: Optional[AlertSeverity] = None,
        resolved: Optional[bool] = None
    ) -> List[Alert]:
        query = self.db.query(Alert)
        
        if severity:
            query = query.filter(Alert.severity == severity)
        if resolved is not None:
            query = query.filter(Alert.is_resolved == resolved)
        
        return query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    def resolve_alert(self, alert_id: int, resolved_by: str) -> Optional[Alert]:
        alert = self.get_alert(alert_id)
        if alert:
            alert.is_resolved = True
            alert.resolved_by = resolved_by
            alert.resolved_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(alert)
        return alert
    
    def get_alert_stats(self) -> dict:
        total = self.db.query(Alert).count()
        unresolved = self.db.query(Alert).filter(Alert.is_resolved == False).count()
        critical = self.db.query(Alert).filter(
            Alert.severity == AlertSeverity.CRITICAL,
            Alert.is_resolved == False
        ).count()
        high = self.db.query(Alert).filter(
            Alert.severity == AlertSeverity.HIGH,
            Alert.is_resolved == False
        ).count()
        
        return {
            'total_alerts': total,
            'unresolved_alerts': unresolved,
            'critical_alerts': critical,
            'high_alerts': high
        }
    
    def determine_severity(self, fraud_score: float) -> AlertSeverity:
        if fraud_score >= 0.9:
            return AlertSeverity.CRITICAL
        elif fraud_score >= 0.7:
            return AlertSeverity.HIGH
        elif fraud_score >= 0.5:
            return AlertSeverity.MEDIUM
        else:
            return AlertSeverity.LOW
