from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """User account model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    stats = db.relationship('UserStats', backref='user', uselist=False, cascade='all, delete-orphan')
    daily_reviews = db.relationship('DailyReview', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Hadith(db.Model):
    """Hadith model for storing the 40 hadiths"""
    __tablename__ = 'hadiths'
    
    id = db.Column(db.Integer, primary_key=True)
    hadith_number = db.Column(db.Integer, unique=True, nullable=False, index=True)
    arabic_text = db.Column(db.Text, nullable=False)
    narrator = db.Column(db.String(255))
    english_text = db.Column(db.Text, nullable=False)
    book_reference = db.Column(db.String(255), default='Book 15: Forty Hadith of al-Nawawi')
    source_url = db.Column(db.String(500), default='https://sunnah.com')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('UserProgress', backref='hadith', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Hadith {self.hadith_number}>'

class UserProgress(db.Model):
    """User progress tracking for each hadith"""
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    hadith_id = db.Column(db.Integer, db.ForeignKey('hadiths.id', ondelete='CASCADE'), nullable=False, index=True)
    is_memorized = db.Column(db.Boolean, default=False)
    is_reviewed_today = db.Column(db.Boolean, default=False)
    last_reviewed_at = db.Column(db.DateTime)
    reflection_text = db.Column(db.Text)
    reviewed_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one record per user per hadith
    __table_args__ = (db.UniqueConstraint('user_id', 'hadith_id', name='uq_user_hadith'),)
    
    def __repr__(self):
        return f'<UserProgress user_id={self.user_id}, hadith_id={self.hadith_id}>'

class UserStats(db.Model):
    """Denormalized user statistics for fast queries"""
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    total_memorized = db.Column(db.Integer, default=0)
    total_reviewed = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_review_date = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserStats user_id={self.user_id}>'

class DailyReview(db.Model):
    """Daily review log for streak tracking"""
    __tablename__ = 'daily_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    review_date = db.Column(db.Date, nullable=False)
    hadith_ids_reviewed = db.Column(db.Text)  # JSON array or comma-separated IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: one review log per user per day
    __table_args__ = (db.UniqueConstraint('user_id', 'review_date', name='uq_user_date'),)
    
    def __repr__(self):
        return f'<DailyReview user_id={self.user_id}, date={self.review_date}>'
