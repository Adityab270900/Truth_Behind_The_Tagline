from app import db
from datetime import datetime

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(100), nullable=False)
    tagline = db.Column(db.String(200), nullable=False)
    claim_text = db.Column(db.Text, nullable=False)
    verdict = db.Column(db.String(20), nullable=True)  # Substantiated, Partially True, Misleading
    score = db.Column(db.Float, nullable=True)
    explanation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Claim {self.brand_name}: {self.tagline}>'

class Evidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.id'), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    relevance_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    claim = db.relationship('Claim', backref=db.backref('evidences', lazy=True))
    
    def __repr__(self):
        return f'<Evidence for Claim {self.claim_id} from {self.source}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.id'), nullable=False)
    user_rating = db.Column(db.Integer, nullable=False)  # 1-5 rating
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    claim = db.relationship('Claim', backref=db.backref('feedbacks', lazy=True))
    
    def __repr__(self):
        return f'<Feedback for Claim {self.claim_id}: {self.user_rating}/5>'
