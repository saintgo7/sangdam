#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import datetime, timedelta
import uuid
import json
import os

app = Flask(__name__)
app.secret_key = 'counseling-system-secret-key-2024-independent'

# Enhanced Mock Database with more features
class CounselingDatabase:
    def __init__(self):
        self.users = [
            {
                'id': 'user-1',
                'username': 'student1',
                'password': 'password123',
                'email': 'student1@university.edu',
                'name': '김학생',
                'role': 'student',
                'department': '컴퓨터공학과',
                'student_id': '20210001',
                'created_at': datetime.now().isoformat(),
                'last_login': None
            },
            {
                'id': 'user-2',
                'username': 'student2',
                'password': 'password123',
                'email': 'student2@university.edu',
                'name': '이학생',
                'role': 'student',
                'department': '컴퓨터공학과',
                'student_id': '20210002',
                'created_at': datetime.now().isoformat(),
                'last_login': None
            },
            {
                'id': 'user-3',
                'username': 'professor1',
                'password': 'password123',
                'email': 'professor1@university.edu',
                'name': '박교수',
                'role': 'professor',
                'department': '컴퓨터공학과',
                'office': '공학관 301호',
                'created_at': datetime.now().isoformat(),
                'last_login': None
            },
            {
                'id': 'user-4',
                'username': 'professor2',
                'password': 'password123',
                'email': 'professor2@university.edu',
                'name': '최교수',
                'role': 'professor',
                'department': '컴퓨터공학과',
                'office': '공학관 302호',
                'created_at': datetime.now().isoformat(),
                'last_login': None
            }
        ]
        
        self.counselings = [
            {
                'id': 'counseling-1',
                'title': '졸업 요건 문의',
                'content': '졸업에 필요한 학점과 필수 과목에 대해 알고 싶습니다.',
                'student_id': 'user-1',
                'professor_id': None,
                'status': 'pending',
                'priority': 'normal',
                'category': '학업',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': 'counseling-2',
                'title': '진로 상담 요청',
                'content': '졸업 후 진로에 대해 고민이 많습니다. 상담을 요청드립니다.',
                'student_id': 'user-2',
                'professor_id': 'user-3',
                'status': 'in_progress',
                'priority': 'high',
                'category': '진로',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]
        
        self.feedbacks = [
            {
                'id': 'feedback-1',
                'counseling_id': 'counseling-2',
                'professor_id': 'user-3',
                'content': '진로에 대한 구체적인 계획을 세워보시고 다시 상담 요청해주세요.',
                'created_at': datetime.now().isoformat()
            }
        ]
        
        self.notifications = []
    
    def find_user_by_username(self, username):
        return next((user for user in self.users if user['username'] == username), None)
    
    def find_user_by_id(self, user_id):
        return next((user for user in self.users if user['id'] == user_id), None)
    
    def authenticate_user(self, username, password):
        user = self.find_user_by_username(username)
        if user and user['password'] == password:
            user['last_login'] = datetime.now().isoformat()
            return user
        return None
    
    def add_counseling(self, counseling_data):
        counseling = {
            'id': f'counseling-{len(self.counselings) + 1}',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'pending',
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
    
    def get_all_counselings(self):
        return self.counselings
    
    def update_counseling(self, counseling_id, update_data):
        for counseling in self.counselings:
            if counseling['id'] == counseling_id:
                counseling.update(update_data)
                counseling['updated_at'] = datetime.now().isoformat()
                return counseling
        return None
    
    def get_counseling_by_id(self, counseling_id):
        return next((c for c in self.counselings if c['id'] == counseling_id), None)
    
    def add_feedback(self, feedback_data):
        feedback = {
            'id': f'feedback-{len(self.feedbacks) + 1}',
            'created_at': datetime.now().isoformat(),
            **feedback_data
        }
        self.feedbacks.append(feedback)
        return feedback
    
    def get_feedbacks_by_counseling(self, counseling_id):
        return [f for f in self.feedbacks if f['counseling_id'] == counseling_id]
    
    def get_statistics(self):
        total_counselings = len(self.counselings)
        pending_counselings = len([c for c in self.counselings if c['status'] == 'pending'])
        in_progress_counselings = len([c for c in self.counselings if c['status'] == 'in_progress'])
        completed_counselings = len([c for c in self.counselings if c['status'] == 'completed'])
        
        return {
            'total_users': len(self.users),
            'total_counselings': total_counselings,
            'pending_counselings': pending_counselings,
            'in_progress_counselings': in_progress_counselings,
            'completed_counselings': completed_counselings,
            'students': len([u for u in self.users if u['role'] == 'student']),
            'professors': len([u for u in self.users if u['role'] == 'professor'])
        }

# Initialize database
db = CounselingDatabase()

# Helper functions
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def role_required(role):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or session.get('role') != role:
                flash('접근 권한이 없습니다.', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

# Routes
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
        
        user = db.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['name'] = user['name']
            
            flash(f'{user["name"]}님, 환영합니다!', 'success')
            
            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user['role'] == 'professor':
                return redirect(url_for('professor_dashboard'))
        
        flash('잘못된 사용자명 또는 비밀번호입니다.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('index'))

@app.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    user = db.find_user_by_id(session['user_id'])
    counselings = db.get_counselings_by_user(session['user_id'], 'student')
    stats = db.get_statistics()
    
    return render_template('student_dashboard.html', 
                         user=user, 
                         counselings=counselings,
                         stats=stats)

@app.route('/professor/dashboard')
@login_required
@role_required('professor')
def professor_dashboard():
    user = db.find_user_by_id(session['user_id'])
    counselings = db.get_counselings_by_user(session['user_id'], 'professor')
    stats = db.get_statistics()
    
    return render_template('professor_dashboard.html', 
                         user=user, 
                         counselings=counselings,
                         stats=stats)

@app.route('/counseling/create', methods=['GET', 'POST'])
@login_required
@role_required('student')
def create_counseling():
    if request.method == 'POST':
        counseling_data = {
            'title': request.form['title'],
            'content': request.form['content'],
            'student_id': session['user_id'],
            'professor_id': None,
            'priority': request.form.get('priority', 'normal'),
            'category': request.form.get('category', '기타')
        }
        
        counseling = db.add_counseling(counseling_data)
        flash('상담 요청이 성공적으로 제출되었습니다.', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('create_counseling.html')

@app.route('/counseling/<counseling_id>')
@login_required
def view_counseling(counseling_id):
    counseling = db.get_counseling_by_id(counseling_id)
    if not counseling:
        flash('존재하지 않는 상담입니다.', 'error')
        return redirect(url_for('student_dashboard' if session['role'] == 'student' else 'professor_dashboard'))
    
    # 권한 확인
    if session['role'] == 'student' and counseling['student_id'] != session['user_id']:
        flash('접근 권한이 없습니다.', 'error')
        return redirect(url_for('student_dashboard'))
    
    student = db.find_user_by_id(counseling['student_id'])
    professor = db.find_user_by_id(counseling['professor_id']) if counseling['professor_id'] else None
    feedbacks = db.get_feedbacks_by_counseling(counseling_id)
    
    return render_template('view_counseling.html', 
                         counseling=counseling,
                         student=student,
                         professor=professor,
                         feedbacks=feedbacks)

@app.route('/counseling/<counseling_id>/assign', methods=['GET', 'POST'])
@login_required
@role_required('professor')
def assign_counseling(counseling_id):
    if request.method == 'GET':
        # GET 요청시 professor_dashboard로 리다이렉트
        return redirect(url_for('professor_dashboard'))
    
    # POST 요청 처리
    update_data = {
        'professor_id': session['user_id'],
        'status': 'in_progress'
    }
    
    counseling = db.update_counseling(counseling_id, update_data)
    if counseling:
        flash('상담을 담당하게 되었습니다.', 'success')
    else:
        flash('상담 배정에 실패했습니다.', 'error')
    
    return redirect(url_for('professor_dashboard'))

@app.route('/counseling/<counseling_id>/complete', methods=['GET', 'POST'])
@login_required
@role_required('professor')
def complete_counseling(counseling_id):
    if request.method == 'GET':
        # GET 요청시 상담 상세보기로 리다이렉트
        return redirect(url_for('view_counseling', counseling_id=counseling_id))
    
    # POST 요청 처리
    feedback_content = request.form.get('feedback')
    
    # 피드백 추가
    if feedback_content:
        feedback_data = {
            'counseling_id': counseling_id,
            'professor_id': session['user_id'],
            'content': feedback_content
        }
        db.add_feedback(feedback_data)
    
    # 상담 완료 처리
    update_data = {'status': 'completed'}
    counseling = db.update_counseling(counseling_id, update_data)
    
    if counseling:
        flash('상담이 완료 처리되었습니다.', 'success')
    else:
        flash('상담 완료 처리에 실패했습니다.', 'error')
    
    return redirect(url_for('professor_dashboard'))

@app.route('/api/stats')
@login_required
def api_stats():
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/api/counselings')
@login_required
def api_counselings():
    if session['role'] == 'student':
        counselings = db.get_counselings_by_user(session['user_id'], 'student')
    elif session['role'] == 'professor':
        counselings = db.get_counselings_by_user(session['user_id'], 'professor')
    else:
        counselings = []
    
    return jsonify(counselings)

if __name__ == '__main__':
    print("🚀 상담 관리 시스템 시작")
    print("📱 접속 주소: http://localhost:9000")
    print("👤 테스트 계정:")
    print("   학생: student1 / password123")
    print("   교수: professor1 / password123")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=9000)