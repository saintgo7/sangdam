import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime
import os

class StudentScoreDBSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Professional Score Management System (Database)")
        self.root.geometry("1000x700")
        
        self.db_path = "student_scores.db"
        self.subjects = ["Mathematics", "Science", "English", "History", "Programming", "Physics", "Chemistry"]
        
        self.init_database()
        self.create_widgets()
        self.update_student_list()
        
    def init_database(self):
        """Initialize SQLite database and create tables"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Create students table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    class_name TEXT NOT NULL,
                    major TEXT NOT NULL,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create scores table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT,
                    subject TEXT NOT NULL,
                    score REAL NOT NULL,
                    date_recorded TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (student_id)
                )
            ''')
            
            self.conn.commit()
            messagebox.showinfo("Database", "Database initialized successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
    
    def create_widgets(self):
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Student Management Tab
        self.create_student_tab()
        
        # Score Entry Tab
        self.create_score_tab()
        
        # Reports Tab
        self.create_reports_tab()
        
        # Statistics Tab
        self.create_statistics_tab()
        
        # Database Management Tab
        self.create_db_tab()
        
    def create_student_tab(self):
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="Student Management")
        
        # Input frame
        input_frame = ttk.LabelFrame(student_frame, text="Add/Edit Student", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Student ID
        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.student_id_entry = ttk.Entry(input_frame, width=20)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Student Name
        ttk.Label(input_frame, text="Name:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.student_name_entry = ttk.Entry(input_frame, width=30)
        self.student_name_entry.grid(row=0, column=3, padx=5, pady=2)
        
        # Class/Grade
        ttk.Label(input_frame, text="Class:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.student_class_entry = ttk.Entry(input_frame, width=20)
        self.student_class_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Major
        ttk.Label(input_frame, text="Major:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.student_major_entry = ttk.Entry(input_frame, width=30)
        self.student_major_entry.grid(row=1, column=3, padx=5, pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Student", command=self.update_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Student", command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_student_fields).pack(side="left", padx=5)
        
        # Student list
        list_frame = ttk.LabelFrame(student_frame, text="Students", padding="10")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for student list
        columns = ("ID", "Name", "Class", "Major", "Average Score")
        self.student_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=120)
        
        scrollbar_student = ttk.Scrollbar(list_frame, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar_student.set)
        
        self.student_tree.pack(side="left", fill="both", expand=True)
        scrollbar_student.pack(side="right", fill="y")
        
        self.student_tree.bind("<ButtonRelease-1>", self.on_student_select)
        
    def create_score_tab(self):
        score_frame = ttk.Frame(self.notebook)
        self.notebook.add(score_frame, text="Score Entry")
        
        # Student selection
        select_frame = ttk.LabelFrame(score_frame, text="Select Student", padding="10")
        select_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(select_frame, text="Student:").grid(row=0, column=0, sticky="w", padx=5)
        self.score_student_var = tk.StringVar()
        self.score_student_combo = ttk.Combobox(select_frame, textvariable=self.score_student_var, 
                                              width=40, state="readonly")
        self.score_student_combo.grid(row=0, column=1, padx=5)
        self.score_student_combo.bind("<<ComboboxSelected>>", self.on_score_student_select)
        
        # Score entry
        entry_frame = ttk.LabelFrame(score_frame, text="Enter Scores", padding="10")
        entry_frame.pack(fill="x", padx=10, pady=5)
        
        self.score_entries = {}
        for i, subject in enumerate(self.subjects):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(entry_frame, text=f"{subject}:").grid(row=row, column=col, sticky="w", padx=5, pady=2)
            entry = ttk.Entry(entry_frame, width=10)
            entry.grid(row=row, column=col+1, padx=5, pady=2)
            self.score_entries[subject] = entry
        
        # Buttons
        btn_frame = ttk.Frame(entry_frame)
        btn_frame.grid(row=len(self.subjects)//3 + 1, column=0, columnspan=6, pady=10)
        
        ttk.Button(btn_frame, text="Save Scores", command=self.save_scores).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Scores", command=self.clear_score_fields).pack(side="left", padx=5)
        
        # Score history
        history_frame = ttk.LabelFrame(score_frame, text="Score History", padding="10")
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        score_columns = ("Date", "Subject", "Score", "Grade")
        self.score_tree = ttk.Treeview(history_frame, columns=score_columns, show="headings", height=10)
        
        for col in score_columns:
            self.score_tree.heading(col, text=col)
            self.score_tree.column(col, width=100)
        
        scrollbar_score = ttk.Scrollbar(history_frame, orient="vertical", command=self.score_tree.yview)
        self.score_tree.configure(yscrollcommand=scrollbar_score.set)
        
        self.score_tree.pack(side="left", fill="both", expand=True)
        scrollbar_score.pack(side="right", fill="y")
        
    def create_reports_tab(self):
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Report generation
        gen_frame = ttk.LabelFrame(reports_frame, text="Generate Reports", padding="10")
        gen_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(gen_frame, text="Individual Report", command=self.generate_individual_report).pack(side="left", padx=5)
        ttk.Button(gen_frame, text="Class Report", command=self.generate_class_report).pack(side="left", padx=5)
        ttk.Button(gen_frame, text="Subject Analysis", command=self.generate_subject_report).pack(side="left", padx=5)
        ttk.Button(gen_frame, text="Export to CSV", command=self.export_to_csv).pack(side="left", padx=5)
        
        # Report display
        display_frame = ttk.LabelFrame(reports_frame, text="Report", padding="10")
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.report_text = tk.Text(display_frame, wrap="word", font=("Courier", 10))
        scrollbar_report = ttk.Scrollbar(display_frame, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar_report.set)
        
        self.report_text.pack(side="left", fill="both", expand=True)
        scrollbar_report.pack(side="right", fill="y")
        
    def create_statistics_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")
        
        # Statistics display
        self.stats_text = tk.Text(stats_frame, wrap="word", font=("Courier", 11))
        scrollbar_stats = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar_stats.set)
        
        self.stats_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar_stats.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Refresh button
        ttk.Button(stats_frame, text="Refresh Statistics", 
                  command=self.update_statistics).pack(pady=10)
    
    def create_db_tab(self):
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="Database Management")
        
        # Database info
        info_frame = ttk.LabelFrame(db_frame, text="Database Information", padding="10")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.db_info_label = ttk.Label(info_frame, text=f"Database: {self.db_path}")
        self.db_info_label.pack(anchor="w")
        
        # Database operations
        ops_frame = ttk.LabelFrame(db_frame, text="Database Operations", padding="10")
        ops_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(ops_frame, text="Backup Database", command=self.backup_database).pack(side="left", padx=5)
        ttk.Button(ops_frame, text="Restore Database", command=self.restore_database).pack(side="left", padx=5)
        ttk.Button(ops_frame, text="Clear All Data", command=self.clear_all_data).pack(side="left", padx=5)
        ttk.Button(ops_frame, text="Check Database", command=self.check_database).pack(side="left", padx=5)
        
        # Database log
        log_frame = ttk.LabelFrame(db_frame, text="Database Log", padding="10")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.db_log_text = tk.Text(log_frame, wrap="word", font=("Courier", 9))
        scrollbar_log = ttk.Scrollbar(log_frame, orient="vertical", command=self.db_log_text.yview)
        self.db_log_text.configure(yscrollcommand=scrollbar_log.set)
        
        self.db_log_text.pack(side="left", fill="both", expand=True)
        scrollbar_log.pack(side="right", fill="y")
    
    def add_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.student_name_entry.get().strip()
        class_name = self.student_class_entry.get().strip()
        major = self.student_major_entry.get().strip()
        
        if not all([student_id, name, class_name, major]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO students (student_id, name, class_name, major)
                VALUES (?, ?, ?, ?)
            ''', (student_id, name, class_name, major))
            
            self.conn.commit()
            self.update_student_list()
            self.clear_student_fields()
            self.log_database_operation(f"Added student: {student_id} - {name}")
            messagebox.showinfo("Success", "Student added successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add student: {e}")
    
    def update_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.student_name_entry.get().strip()
        class_name = self.student_class_entry.get().strip()
        major = self.student_major_entry.get().strip()
        
        if not all([student_id, name, class_name, major]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            self.cursor.execute('''
                UPDATE students 
                SET name = ?, class_name = ?, major = ?
                WHERE student_id = ?
            ''', (name, class_name, major, student_id))
            
            if self.cursor.rowcount == 0:
                messagebox.showerror("Error", "Student ID not found")
                return
            
            self.conn.commit()
            self.update_student_list()
            self.clear_student_fields()
            self.log_database_operation(f"Updated student: {student_id} - {name}")
            messagebox.showinfo("Success", "Student updated successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update student: {e}")
    
    def delete_student(self):
        student_id = self.student_id_entry.get().strip()
        
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID")
            return
        
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete student {student_id} and all their scores?")
        if result:
            try:
                # Delete scores first
                self.cursor.execute('DELETE FROM scores WHERE student_id = ?', (student_id,))
                # Delete student
                self.cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
                
                if self.cursor.rowcount == 0:
                    messagebox.showerror("Error", "Student ID not found")
                    return
                
                self.conn.commit()
                self.update_student_list()
                self.clear_student_fields()
                self.log_database_operation(f"Deleted student: {student_id}")
                messagebox.showinfo("Success", "Student deleted successfully")
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete student: {e}")
    
    def update_student_list(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        try:
            self.cursor.execute('''
                SELECT s.student_id, s.name, s.class_name, s.major,
                       COALESCE(AVG(sc.score), 0) as avg_score
                FROM students s
                LEFT JOIN scores sc ON s.student_id = sc.student_id
                GROUP BY s.student_id, s.name, s.class_name, s.major
                ORDER BY s.student_id
            ''')
            
            students = self.cursor.fetchall()
            
            for student in students:
                student_id, name, class_name, major, avg_score = student
                self.student_tree.insert("", "end", values=(
                    student_id, name, class_name, major, f"{avg_score:.1f}"
                ))
            
            # Update combobox
            student_list = [f"{student[0]} - {student[1]}" for student in students]
            self.score_student_combo['values'] = student_list
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load students: {e}")
    
    def on_student_select(self, event):
        selection = self.student_tree.selection()
        if selection:
            item = self.student_tree.item(selection[0])
            values = item['values']
            
            self.student_id_entry.delete(0, tk.END)
            self.student_id_entry.insert(0, values[0])
            self.student_name_entry.delete(0, tk.END)
            self.student_name_entry.insert(0, values[1])
            self.student_class_entry.delete(0, tk.END)
            self.student_class_entry.insert(0, values[2])
            self.student_major_entry.delete(0, tk.END)
            self.student_major_entry.insert(0, values[3])
    
    def clear_student_fields(self):
        self.student_id_entry.delete(0, tk.END)
        self.student_name_entry.delete(0, tk.END)
        self.student_class_entry.delete(0, tk.END)
        self.student_major_entry.delete(0, tk.END)
    
    def save_scores(self):
        selected = self.score_student_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a student")
            return
        
        student_id = selected.split(" - ")[0]
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            scores_to_save = []
            for subject, entry in self.score_entries.items():
                score_text = entry.get().strip()
                if score_text:
                    try:
                        score = float(score_text)
                        if 0 <= score <= 100:
                            scores_to_save.append((student_id, subject, score, date))
                        else:
                            messagebox.showerror("Error", f"Score for {subject} must be between 0-100")
                            return
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid score for {subject}")
                        return
            
            if not scores_to_save:
                messagebox.showwarning("Warning", "No scores to save")
                return
            
            # Save all scores
            self.cursor.executemany('''
                INSERT INTO scores (student_id, subject, score, date_recorded)
                VALUES (?, ?, ?, ?)
            ''', scores_to_save)
            
            self.conn.commit()
            self.update_student_list()
            self.update_score_history()
            self.clear_score_fields()
            self.log_database_operation(f"Saved {len(scores_to_save)} scores for student: {student_id}")
            messagebox.showinfo("Success", f"Saved {len(scores_to_save)} scores successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save scores: {e}")
    
    def update_score_history(self):
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        
        selected = self.score_student_var.get()
        if not selected:
            return
        
        student_id = selected.split(" - ")[0]
        
        try:
            self.cursor.execute('''
                SELECT date_recorded, subject, score
                FROM scores
                WHERE student_id = ?
                ORDER BY date_recorded DESC
            ''', (student_id,))
            
            scores = self.cursor.fetchall()
            
            for score_data in scores:
                date_recorded, subject, score = score_data
                grade = self.get_grade(score)
                # Format date to show only date part
                date_display = date_recorded.split()[0] if ' ' in date_recorded else date_recorded
                self.score_tree.insert("", "end", values=(
                    date_display, subject, f"{score:.1f}", grade
                ))
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load score history: {e}")
    
    def get_grade(self, score):
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def on_score_student_select(self, event):
        self.update_score_history()
    
    def clear_score_fields(self):
        for entry in self.score_entries.values():
            entry.delete(0, tk.END)
    
    def generate_individual_report(self):
        selected = self.score_student_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a student")
            return
        
        student_id = selected.split(" - ")[0]
        
        try:
            # Get student info
            self.cursor.execute('''
                SELECT name, class_name, major
                FROM students
                WHERE student_id = ?
            ''', (student_id,))
            
            student_info = self.cursor.fetchone()
            if not student_info:
                messagebox.showerror("Error", "Student not found")
                return
            
            name, class_name, major = student_info
            
            # Get latest scores for each subject
            self.cursor.execute('''
                SELECT subject, score, date_recorded
                FROM scores s1
                WHERE student_id = ? AND date_recorded = (
                    SELECT MAX(date_recorded)
                    FROM scores s2
                    WHERE s2.student_id = s1.student_id AND s2.subject = s1.subject
                )
                ORDER BY subject
            ''', (student_id,))
            
            scores = self.cursor.fetchall()
            
            report = f"INDIVIDUAL STUDENT REPORT\n"
            report += "=" * 50 + "\n\n"
            report += f"Student ID: {student_id}\n"
            report += f"Name: {name}\n"
            report += f"Class: {class_name}\n"
            report += f"Major: {major}\n\n"
            
            report += "SUBJECT SCORES:\n"
            report += "-" * 30 + "\n"
            
            total_score = 0
            subject_count = 0
            
            # Create a dict for easy lookup
            score_dict = {subject: (score, date) for subject, score, date in scores}
            
            for subject in self.subjects:
                if subject in score_dict:
                    score, date = score_dict[subject]
                    grade = self.get_grade(score)
                    report += f"{subject:<15}: {score:>6.1f} ({grade}) [{date.split()[0]}]\n"
                    total_score += score
                    subject_count += 1
                else:
                    report += f"{subject:<15}: {'No Score':>10}\n"
            
            if subject_count > 0:
                average = total_score / subject_count
                overall_grade = self.get_grade(average)
                report += "-" * 30 + "\n"
                report += f"{'Overall Average':<15}: {average:>6.1f} ({overall_grade})\n"
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(1.0, report)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to generate report: {e}")
    
    def generate_class_report(self):
        try:
            self.cursor.execute('''
                SELECT s.student_id, s.name, s.class_name, s.major,
                       COALESCE(AVG(sc.score), 0) as avg_score
                FROM students s
                LEFT JOIN scores sc ON s.student_id = sc.student_id
                GROUP BY s.student_id, s.name, s.class_name, s.major
                ORDER BY s.class_name, s.name
            ''')
            
            students = self.cursor.fetchall()
            
            if not students:
                messagebox.showerror("Error", "No students available")
                return
            
            # Group by class
            classes = {}
            for student in students:
                student_id, name, class_name, major, avg_score = student
                if class_name not in classes:
                    classes[class_name] = []
                classes[class_name].append((student_id, name, major, avg_score))
            
            report = "CLASS REPORT\n"
            report += "=" * 50 + "\n\n"
            
            for class_name, students_in_class in sorted(classes.items()):
                report += f"CLASS: {class_name}\n"
                report += "-" * 30 + "\n"
                
                total_avg = 0
                student_count = 0
                
                for student_id, name, major, avg_score in students_in_class:
                    if avg_score > 0:
                        grade = self.get_grade(avg_score)
                        report += f"{name:<20} (ID: {student_id}): {avg_score:>6.1f} ({grade})\n"
                        total_avg += avg_score
                        student_count += 1
                    else:
                        report += f"{name:<20} (ID: {student_id}): {'No Score':>10}\n"
                
                if student_count > 0:
                    class_avg = total_avg / student_count
                    report += f"\nClass Average: {class_avg:.1f}\n"
                
                report += "\n"
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(1.0, report)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to generate class report: {e}")
    
    def generate_subject_report(self):
        try:
            report = "SUBJECT ANALYSIS REPORT\n"
            report += "=" * 50 + "\n\n"
            
            for subject in self.subjects:
                self.cursor.execute('''
                    SELECT s.name, s.student_id, sc.score
                    FROM students s
                    JOIN scores sc ON s.student_id = sc.student_id
                    WHERE sc.subject = ? AND sc.date_recorded = (
                        SELECT MAX(date_recorded)
                        FROM scores sc2
                        WHERE sc2.student_id = s.student_id AND sc2.subject = ?
                    )
                    ORDER BY sc.score DESC
                ''', (subject, subject))
                
                results = self.cursor.fetchall()
                
                report += f"SUBJECT: {subject}\n"
                report += "-" * 30 + "\n"
                
                if results:
                    scores = [result[2] for result in results]
                    avg_score = sum(scores) / len(scores)
                    max_score = max(scores)
                    min_score = min(scores)
                    
                    report += f"Students with scores: {len(scores)}\n"
                    report += f"Average Score: {avg_score:.1f}\n"
                    report += f"Highest Score: {max_score:.1f}\n"
                    report += f"Lowest Score: {min_score:.1f}\n\n"
                    
                    report += "Top performers:\n"
                    for i, (name, student_id, score) in enumerate(results[:5]):
                        grade = self.get_grade(score)
                        report += f"  {i+1}. {name} (ID: {student_id}): {score:.1f} ({grade})\n"
                else:
                    report += "No scores recorded for this subject\n"
                
                report += "\n"
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(1.0, report)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to generate subject report: {e}")
    
    def update_statistics(self):
        try:
            # Get basic counts
            self.cursor.execute('SELECT COUNT(*) FROM students')
            student_count = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM scores')
            score_count = self.cursor.fetchone()[0]
            
            if student_count == 0:
                self.stats_text.delete(1.0, tk.END)
                self.stats_text.insert(1.0, "No student data available")
                return
            
            stats = "SYSTEM STATISTICS\n"
            stats += "=" * 40 + "\n\n"
            
            stats += f"Total Students: {student_count}\n"
            stats += f"Total Score Records: {score_count}\n\n"
            
            # Class distribution
            self.cursor.execute('''
                SELECT class_name, COUNT(*)
                FROM students
                GROUP BY class_name
                ORDER BY class_name
            ''')
            classes = self.cursor.fetchall()
            
            stats += "CLASS DISTRIBUTION:\n"
            for class_name, count in classes:
                stats += f"  {class_name}: {count} students\n"
            
            # Major distribution
            self.cursor.execute('''
                SELECT major, COUNT(*)
                FROM students
                GROUP BY major
                ORDER BY major
            ''')
            majors = self.cursor.fetchall()
            
            stats += "\nMAJOR DISTRIBUTION:\n"
            for major, count in majors:
                stats += f"  {major}: {count} students\n"
            
            # Subject averages
            stats += "\nSUBJECT AVERAGES:\n"
            for subject in self.subjects:
                self.cursor.execute('''
                    SELECT AVG(score), COUNT(DISTINCT student_id)
                    FROM scores
                    WHERE subject = ?
                ''', (subject,))
                
                result = self.cursor.fetchone()
                avg_score, student_count_subject = result
                
                if avg_score is not None:
                    stats += f"  {subject:<15}: {avg_score:>6.1f} ({student_count_subject} students)\n"
                else:
                    stats += f"  {subject:<15}: {'No Data':>10}\n"
            
            # Overall system average
            self.cursor.execute('''
                SELECT AVG(avg_score)
                FROM (
                    SELECT student_id, AVG(score) as avg_score
                    FROM scores
                    GROUP BY student_id
                ) student_averages
            ''')
            
            system_avg = self.cursor.fetchone()[0]
            if system_avg is not None:
                stats += f"\nSYSTEM AVERAGE: {system_avg:.1f}\n"
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load statistics: {e}")
    
    def export_to_csv(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                self.cursor.execute('''
                    SELECT s.student_id, s.name, s.class_name, s.major
                    FROM students s
                    ORDER BY s.student_id
                ''')
                
                students = self.cursor.fetchall()
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Header
                    header = ["Student ID", "Name", "Class", "Major"] + self.subjects + ["Average"]
                    writer.writerow(header)
                    
                    # Data
                    for student in students:
                        student_id, name, class_name, major = student
                        row = [student_id, name, class_name, major]
                        
                        # Get latest scores for each subject
                        subject_scores = []
                        for subject in self.subjects:
                            self.cursor.execute('''
                                SELECT score
                                FROM scores
                                WHERE student_id = ? AND subject = ?
                                ORDER BY date_recorded DESC
                                LIMIT 1
                            ''', (student_id, subject))
                            
                            result = self.cursor.fetchone()
                            if result:
                                subject_scores.append(result[0])
                                row.append(result[0])
                            else:
                                row.append("")
                        
                        # Calculate average
                        if subject_scores:
                            avg = sum(subject_scores) / len(subject_scores)
                            row.append(f"{avg:.1f}")
                        else:
                            row.append("")
                        
                        writer.writerow(row)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                self.log_database_operation(f"Exported data to CSV: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def backup_database(self):
        try:
            backup_filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                initialvalue=f"student_scores_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )
            
            if backup_filename:
                import shutil
                shutil.copy2(self.db_path, backup_filename)
                messagebox.showinfo("Success", f"Database backed up to {backup_filename}")
                self.log_database_operation(f"Database backed up to: {backup_filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup database: {str(e)}")
    
    def restore_database(self):
        result = messagebox.askyesno("Confirm Restore", 
                                   "This will replace the current database. Continue?")
        if result:
            try:
                restore_filename = filedialog.askopenfilename(
                    filetypes=[("Database files", "*.db"), ("All files", "*.*")]
                )
                
                if restore_filename:
                    self.conn.close()
                    import shutil
                    shutil.copy2(restore_filename, self.db_path)
                    self.conn = sqlite3.connect(self.db_path)
                    self.cursor = self.conn.cursor()
                    self.update_student_list()
                    messagebox.showinfo("Success", "Database restored successfully")
                    self.log_database_operation(f"Database restored from: {restore_filename}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore database: {str(e)}")
    
    def clear_all_data(self):
        result = messagebox.askyesno("Confirm Clear", 
                                   "This will delete ALL data permanently. Continue?")
        if result:
            try:
                self.cursor.execute('DELETE FROM scores')
                self.cursor.execute('DELETE FROM students')
                self.conn.commit()
                self.update_student_list()
                messagebox.showinfo("Success", "All data cleared successfully")
                self.log_database_operation("All data cleared from database")
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to clear data: {e}")
    
    def check_database(self):
        try:
            # Check database integrity
            self.cursor.execute('PRAGMA integrity_check')
            integrity = self.cursor.fetchone()[0]
            
            # Get table info
            self.cursor.execute('SELECT COUNT(*) FROM students')
            student_count = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM scores')
            score_count = self.cursor.fetchone()[0]
            
            info = f"Database Check Results:\n"
            info += f"Integrity: {integrity}\n"
            info += f"Students: {student_count}\n"
            info += f"Score Records: {score_count}\n"
            info += f"Database Size: {os.path.getsize(self.db_path)} bytes\n"
            
            messagebox.showinfo("Database Check", info)
            self.log_database_operation("Database integrity check completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Database check failed: {str(e)}")
    
    def log_database_operation(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.db_log_text.insert(tk.END, log_entry)
        self.db_log_text.see(tk.END)
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = StudentScoreDBSystem(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.conn.close(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()