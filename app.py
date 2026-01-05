"""
Daily Habit Tracker - Flask Backend
A full-stack habit tracking application with REST API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///habits.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# ==================== Database Models ====================

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    habits = db.relationship('Habit', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Habit(db.Model):
    """Habit model"""
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(10), default='🎯')
    category = db.Column(db.String(50), default='general')
    color = db.Column(db.String(7), default='#3498db')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs = db.relationship('DailyLog', backref='habit', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'color': self.color,
            'created_at': self.created_at.isoformat()
        }


class DailyLog(db.Model):
    """Daily habit completion log"""
    __tablename__ = 'daily_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'date': self.date.isoformat(),
            'completed': self.completed,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }


# ==================== API Routes ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'message': 'Daily Habit Tracker API is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ==================== Habits Routes ====================

@app.route('/api/habits', methods=['GET'])
def get_habits():
    """Get all habits for authenticated user"""
    try:
        user_id = request.args.get('user_id', 1)  # Default user for demo
        habits = Habit.query.filter_by(user_id=user_id).all()
        return jsonify([habit.to_dict() for habit in habits]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/habits', methods=['POST'])
def create_habit():
    """Create a new habit"""
    try:
        data = request.get_json()
        
        habit = Habit(
            user_id=data.get('user_id', 1),
            name=data.get('name'),
            description=data.get('description', ''),
            icon=data.get('icon', '🎯'),
            category=data.get('category', 'general'),
            color=data.get('color', '#3498db')
        )
        
        db.session.add(habit)
        db.session.commit()
        
        return jsonify(habit.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/habits/<int:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    """Update a habit"""
    try:
        habit = Habit.query.get_or_404(habit_id)
        data = request.get_json()
        
        habit.name = data.get('name', habit.name)
        habit.description = data.get('description', habit.description)
        habit.icon = data.get('icon', habit.icon)
        habit.category = data.get('category', habit.category)
        habit.color = data.get('color', habit.color)
        
        db.session.commit()
        return jsonify(habit.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    """Delete a habit"""
    try:
        habit = Habit.query.get_or_404(habit_id)
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'message': 'Habit deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ==================== Daily Logs Routes ====================

@app.route('/api/logs', methods=['POST'])
def log_habit():
    """Log habit completion for a day"""
    try:
        data = request.get_json()
        
        log = DailyLog(
            habit_id=data.get('habit_id'),
            date=datetime.fromisoformat(data.get('date', datetime.now().date().isoformat())).date(),
            completed=data.get('completed', True),
            notes=data.get('notes', '')
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify(log.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/logs/<int:habit_id>', methods=['GET'])
def get_habit_logs(habit_id):
    """Get all logs for a specific habit"""
    try:
        logs = DailyLog.query.filter_by(habit_id=habit_id).all()
        return jsonify([log.to_dict() for log in logs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/logs/date/<date_str>', methods=['GET'])
def get_logs_by_date(date_str):
    """Get all logs for a specific date"""
    try:
        target_date = datetime.fromisoformat(date_str).date()
        logs = DailyLog.query.filter_by(date=target_date).all()
        return jsonify([log.to_dict() for log in logs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ==================== Analytics Routes ====================

@app.route('/api/analytics/completion/<int:habit_id>', methods=['GET'])
def get_completion_rate(habit_id):
    """Get completion rate for a habit"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.now().date() - timedelta(days=days)
        
        logs = DailyLog.query.filter(
            DailyLog.habit_id == habit_id,
            DailyLog.date >= start_date
        ).all()
        
        completed = sum(1 for log in logs if log.completed)
        total = len(logs) if logs else 1
        rate = (completed / total * 100) if total > 0 else 0
        
        return jsonify({
            'habit_id': habit_id,
            'days': days,
            'completed': completed,
            'total': total,
            'completion_rate': round(rate, 2)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/analytics/streak/<int:habit_id>', methods=['GET'])
def get_streak(habit_id):
    """Get current streak for a habit"""
    try:
        logs = DailyLog.query.filter_by(
            habit_id=habit_id,
            completed=True
        ).order_by(DailyLog.date.desc()).all()
        
        if not logs:
            return jsonify({'habit_id': habit_id, 'streak': 0}), 200
        
        streak = 0
        today = datetime.now().date()
        
        for log in logs:
            if log.date == today or log.date == today - timedelta(days=streak):
                streak += 1
            else:
                break
        
        return jsonify({
            'habit_id': habit_id,
            'streak': streak
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ==================== Database Initialization ====================

@app.before_request
def create_tables():
    """Create tables if they don't exist"""
    db.create_all()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
