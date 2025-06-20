from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import uuid
import json
import os

app = Flask(__name__)
app.secret_key = 'sangdam-counseling-secret-key-2024'

# Mock Database
class MockDatabase:
    def __init__(self):
        self.users = [
            {
                'id': 'user-1',
                'username': 'student1',
                'password': 'password123',
                'email': 'student1@example.com',
                'name': '김학생',
                'role': 'student',
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 'user-2',
                'username': 'professor1',
                'password': 'password123',
                'email': 'professor1@example.com',
                'name': '이교수',
                'role': 'professor',
                'created_at': datetime.now().isoformat()
            }
        ]
        
        self.counselings = [
            {
                'id': 'counseling-1',
                'title': '학업 상담 요청',
                'content': '졸업 요건에 대해 문의드립니다.',
                'student_id': 'user-1',
                'professor_id': None,
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]
        
        self.feedbacks = []
    
    def find_user_by_username(self, username):
        return next((user for user in self.users if user['username'] == username), None)
    
    def find_user_by_id(self, user_id):
        return next((user for user in self.users if user['id'] == user_id), None)
    
    def add_counseling(self, counseling_data):
        counseling = {
            'id': f'counseling-{len(self.counselings) + 1}',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            **counseling_data
        }
        self.counselings.append(counseling)
        return counseling
    
    def get_counselings_by_user(self, user_id, role):
        if role == 'student':
            return [c for c in self.counselings if c['student_id'] == user_id]
        elif role == 'professor':
            return [c for c in self.counselings if c['professor_id'] == user_id or c['professor_id'] is None]
        return []
    
    def update_counseling(self, counseling_id, update_data):
        for counseling in self.counselings:
            if counseling['id'] == counseling_id:
                counseling.update(update_data)
                counseling['updated_at'] = datetime.now().isoformat()
                return counseling
        return None

# Initialize database
db = MockDatabase()

@app.route('/')
def index():
    if 'user_id' in session:
        user = db.find_user_by_id(session['user_id'])
        if user:
            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user['role'] == 'professor':
                return redirect(url_for('professor_dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.find_user_by_username(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user['role'] == 'professor':
                return redirect(url_for('professor_dashboard'))
        
        return render_template('login.html', error='잘못된 사용자명 또는 비밀번호입니다.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    user = db.find_user_by_id(session['user_id'])
    counselings = db.get_counselings_by_user(session['user_id'], 'student')
    
    return render_template('student_dashboard.html', user=user, counselings=counselings)

@app.route('/professor/dashboard')
def professor_dashboard():
    if 'user_id' not in session or session['role'] != 'professor':
        return redirect(url_for('login'))
    
    user = db.find_user_by_id(session['user_id'])
    counselings = db.get_counselings_by_user(session['user_id'], 'professor')
    
    return render_template('professor_dashboard.html', user=user, counselings=counselings)

@app.route('/counseling/create', methods=['GET', 'POST'])
def create_counseling():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        counseling_data = {
            'title': request.form['title'],
            'content': request.form['content'],
            'student_id': session['user_id'],
            'professor_id': None,
            'status': 'pending'
        }
        
        db.add_counseling(counseling_data)
        return redirect(url_for('student_dashboard'))
    
    return render_template('create_counseling.html')

@app.route('/counseling/<counseling_id>/assign', methods=['POST'])
def assign_counseling(counseling_id):
    if 'user_id' not in session or session['role'] != 'professor':
        return redirect(url_for('login'))
    
    update_data = {
        'professor_id': session['user_id'],
        'status': 'in_progress'
    }
    
    db.update_counseling(counseling_id, update_data)
    return redirect(url_for('professor_dashboard'))

@app.route('/api/stats')
def api_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    stats = {
        'total_users': len(db.users),
        'total_counselings': len(db.counselings),
        'pending_counselings': len([c for c in db.counselings if c['status'] == 'pending']),
        'completed_counselings': len([c for c in db.counselings if c['status'] == 'completed'])
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)