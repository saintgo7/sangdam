# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
from pymongo import MongoClient
import sys
import os

# UTF-8 encoding setup
import locale
try:
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        print("Locale setup failed, using default settings")

class StudentScoreSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Score Management System")
        self.root.geometry("1024x768")
        
        # UTF-8 encoding setup
        try:
            self.root.tk.call('encoding', 'system', 'utf-8')
            # IME settings for input
            self.root.tk.call('tk', 'scaling', 1.0)
        except:
            pass
        
        # Font setup
        self.setup_fonts()
        
        # Local data initialization (used when MongoDB connection fails)
        self.students = {}
        
        self.subjects = ["Introduction to Computers", "IoT Emb", "Capston Design"]
        
        # Initialize MongoDB-related attributes
        self.client = None
        self.db = None
        self.students_collection = None
        self.scores_collection = None
        self.use_mongodb = False
        
        # Create GUI widgets first
        self.create_widgets()
        
        # MongoDB connection setup (after GUI creation)
        self.root.after(100, self.setup_mongodb)
        
        # Update student list after a delay to allow MongoDB setup
        self.root.after(200, self.update_student_list)
    
    def setup_fonts(self):
        """Font setup for the application"""
        try:
            self.default_font = ('Arial', 18, 'bold')
            self.title_font = ('Arial', 18, 'bold')
            self.button_font = ('Arial', 18, 'bold')
                
        except Exception as e:
            print(f"Font setup error: {e}")
            # Safe default fonts
            self.default_font = ('TkDefaultFont', 18, 'bold')
            self.title_font = ('TkDefaultFont', 18, 'bold')
            self.button_font = ('TkDefaultFont', 18, 'bold')
    
    def setup_mongodb(self):
        """MongoDB connection setup (completely silent)"""
        self.client = None
        self.db = None
        self.students_collection = None
        self.scores_collection = None
        self.use_mongodb = False
        
        # Silent MongoDB connection attempt
        try:
            from pymongo import MongoClient
            
            # Extremely short timeout for instant fallback
            self.client = MongoClient(
                'mongodb://localhost:27017/',
                serverSelectionTimeoutMS=50,  # 50ms timeout
                connectTimeoutMS=50,
                socketTimeoutMS=50,
                connect=False
            )
            
            # Quick connection test
            self.client.admin.command('ping')
            
            # Database setup
            self.db = self.client['student_management_db']
            self.students_collection = self.db['students']
            self.scores_collection = self.db['scores']
            
            # Create indexes silently
            try:
                self.students_collection.create_index("student_id", unique=True)
                self.scores_collection.create_index([("student_id", 1), ("subject", 1)])
            except:
                pass
            
            self.use_mongodb = True
            
        except:
            # Silent fallback to local mode
            self._cleanup_mongodb()
        
        # Update status indicator
        self._update_mode_indicator()
            
    def _cleanup_mongodb(self):
        """Clean up MongoDB connection objects"""
        try:
            if hasattr(self, 'client') and self.client:
                self.client.close()
        except:
            pass
        
        self.client = None
        self.db = None
        self.students_collection = None
        self.scores_collection = None
        self.use_mongodb = False
    
    def _fallback_to_local(self, operation_name="Operation"):
        """Silent fallback to local mode when MongoDB fails"""
        if self.use_mongodb:
            self._cleanup_mongodb()
            return True
        return False
    
    def _update_mode_indicator(self):
        """Update the status indicator showing current mode"""
        if hasattr(self, 'mode_label'):
            if self.use_mongodb:
                self.mode_label.config(text="Mode: Database Connected", foreground="green")
            else:
                self.mode_label.config(text="Mode: Local Storage", foreground="orange")
        
    def create_widgets(self):
        # Status frame at the top
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Mode indicator label
        self.mode_label = ttk.Label(status_frame, text="Initializing...", 
                                   font=self.button_font, foreground="blue")
        self.mode_label.pack(side="right")
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure notebook tab style for larger tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10], font=self.title_font)
        
        # Student Management Tab
        self.create_student_tab()
        
        # Score Entry Tab
        self.create_score_tab()
        
        # Reports Tab
        self.create_reports_tab()
        
        # Statistics Tab
        self.create_statistics_tab()
        
    def create_student_tab(self):
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="Student Management")
        
        # Input frame
        input_frame = ttk.LabelFrame(student_frame, text="Add/Edit Student", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Student ID
        ttk.Label(input_frame, text="Student ID:", font=self.title_font).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.student_id_entry = ttk.Entry(input_frame, width=30, font=self.title_font)
        self.student_id_entry.grid(row=0, column=1, padx=8, pady=8, ipady=8)
        
        # Student Name
        ttk.Label(input_frame, text="Name:", font=self.title_font).grid(row=0, column=2, sticky="w", padx=8, pady=8)
        self.student_name_entry = ttk.Entry(input_frame, width=40, font=self.title_font)
        self.student_name_entry.grid(row=0, column=3, padx=8, pady=8, ipady=8)
        
        # Class/Grade
        ttk.Label(input_frame, text="Class:", font=self.title_font).grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.student_class_entry = ttk.Entry(input_frame, width=30, font=self.title_font)
        self.student_class_entry.grid(row=1, column=1, padx=8, pady=8, ipady=8)
        
        # Major
        ttk.Label(input_frame, text="Major:", font=self.title_font).grid(row=1, column=2, sticky="w", padx=8, pady=8)
        self.student_major_entry = ttk.Entry(input_frame, width=40, font=self.title_font)
        self.student_major_entry.grid(row=1, column=3, padx=8, pady=8, ipady=8)
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5, ipady=8)
        ttk.Button(btn_frame, text="Update Student", command=self.update_student).pack(side="left", padx=5, ipady=8)
        ttk.Button(btn_frame, text="Delete Student", command=self.delete_student).pack(side="left", padx=5, ipady=8)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_student_fields).pack(side="left", padx=5, ipady=8)
        
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
        
        ttk.Label(select_frame, text="Student:", font=self.title_font).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.score_student_var = tk.StringVar()
        self.score_student_combo = ttk.Combobox(select_frame, textvariable=self.score_student_var, 
                                              width=60, state="readonly", font=self.title_font)
        self.score_student_combo.grid(row=0, column=1, padx=8, pady=8, ipady=8)
        self.score_student_combo.bind("<<ComboboxSelected>>", self.on_score_student_select)
        
        # Score entry
        entry_frame = ttk.LabelFrame(score_frame, text="Enter Scores", padding="10")
        entry_frame.pack(fill="x", padx=10, pady=5)
        
        self.score_entries = {}
        for i, subject in enumerate(self.subjects):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(entry_frame, text=f"{subject}:", font=self.title_font).grid(row=row, column=col, sticky="w", padx=8, pady=8)
            entry = ttk.Entry(entry_frame, width=20, font=self.title_font)
            entry.grid(row=row, column=col+1, padx=8, pady=8, ipady=8)
            self.score_entries[subject] = entry
        
        # Buttons
        btn_frame = ttk.Frame(entry_frame)
        btn_frame.grid(row=len(self.subjects)//3 + 1, column=0, columnspan=6, pady=10)
        
        ttk.Button(btn_frame, text="Save Scores", command=self.save_scores).pack(side="left", padx=5, ipady=8)
        ttk.Button(btn_frame, text="Clear Scores", command=self.clear_score_fields).pack(side="left", padx=5, ipady=8)
        
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
        
        ttk.Button(gen_frame, text="Individual Report", command=self.generate_individual_report).pack(side="left", padx=5, ipady=8)
        ttk.Button(gen_frame, text="Class Report", command=self.generate_class_report).pack(side="left", padx=5, ipady=8)
        ttk.Button(gen_frame, text="Subject Analysis", command=self.generate_subject_report).pack(side="left", padx=5, ipady=8)
        ttk.Button(gen_frame, text="Export to CSV", command=self.export_to_csv).pack(side="left", padx=5, ipady=8)
        
        # Report display
        display_frame = ttk.LabelFrame(reports_frame, text="Report", padding="10")
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.report_text = tk.Text(display_frame, wrap="word", font=self.default_font)
        scrollbar_report = ttk.Scrollbar(display_frame, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar_report.set)
        
        self.report_text.pack(side="left", fill="both", expand=True)
        scrollbar_report.pack(side="right", fill="y")
        
    def create_statistics_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")
        
        # Statistics display
        self.stats_text = tk.Text(stats_frame, wrap="word", font=self.default_font)
        scrollbar_stats = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar_stats.set)
        
        self.stats_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar_stats.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Refresh button
        ttk.Button(stats_frame, text="Refresh Statistics", 
                  command=self.update_statistics).pack(pady=10, ipady=8)
    
    def add_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.student_name_entry.get().strip()
        class_name = self.student_class_entry.get().strip()
        major = self.student_major_entry.get().strip()
        
        if not all([student_id, name, class_name, major]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        # Check for duplicate student ID (both modes)
        if self.use_mongodb and self.students_collection is not None:
            try:
                if self.students_collection.find_one({"student_id": student_id}):
                    messagebox.showerror("Error", "Student ID already exists")
                    return
            except:
                self._fallback_to_local()
        
        if not self.use_mongodb and student_id in self.students:
            messagebox.showerror("Error", "Student ID already exists")
            return
        
        # Add student (try MongoDB first, fallback to local)
        operation_successful = False
        
        if self.use_mongodb and self.students_collection is not None:
            try:
                student_data = {
                    "student_id": student_id,
                    "name": name,
                    "class": class_name,
                    "major": major,
                    "created_at": datetime.now()
                }
                self.students_collection.insert_one(student_data)
                operation_successful = True
            except:
                self._fallback_to_local()
        
        # Local mode (either by design or after fallback)
        if not operation_successful:
            self.students[student_id] = {
                "name": name,
                "class": class_name,
                "major": major,
                "scores": {}
            }
            operation_successful = True
        
        if operation_successful:
            self.update_student_list()
            self.clear_student_fields()
            mode_text = "in database" if self.use_mongodb else "locally"
            messagebox.showinfo("Success", f"Student added successfully {mode_text}")
    
    def update_student_list(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        # Load students (try MongoDB first, fallback to local)
        students_loaded = False
        student_list = []
        
        if self.use_mongodb and self.students_collection is not None:
            try:
                students = list(self.students_collection.find({}, {"_id": 0}))
                
                for student in students:
                    student_id = student["student_id"]
                    avg_score = self.calculate_average_score(student_id)
                    self.student_tree.insert("", "end", values=(
                        student_id, student["name"], student["class"], student["major"], f"{avg_score:.1f}"
                    ))
                    student_list.append(f"{student_id} - {student['name']}")
                
                students_loaded = True
                
            except:
                self._fallback_to_local()
        
        # Local mode (either by design or after fallback)
        if not students_loaded:
            for student_id, data in self.students.items():
                avg_score = self.calculate_average_score(student_id)
                self.student_tree.insert("", "end", values=(
                    student_id, data["name"], data["class"], data["major"], f"{avg_score:.1f}"
                ))
                student_list.append(f"{student_id} - {data['name']}")
            
            students_loaded = True
        
        # Update combobox
        if students_loaded:
            self.score_student_combo['values'] = student_list
    
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
    
    def update_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.student_name_entry.get().strip()
        class_name = self.student_class_entry.get().strip()
        major = self.student_major_entry.get().strip()
        
        if not all([student_id, name, class_name, major]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        # Try MongoDB first, then fallback to local if needed
        operation_successful = False
        
        if self.use_mongodb and self.students_collection is not None:
            try:
                # MongoDB mode
                result = self.students_collection.update_one(
                    {"student_id": student_id},
                    {"$set": {
                        "name": name,
                        "class": class_name,
                        "major": major,
                        "updated_at": datetime.now()
                    }}
                )
                
                if result.matched_count == 0:
                    messagebox.showerror("Error", "Student ID not found")
                    return
                
                operation_successful = True
                
            except Exception as e:
                print(f"MongoDB update_student failed: {e}")
                # Fallback to local mode
                if self._fallback_to_local("Update Student"):
                    # Retry in local mode (will be handled by the local mode block below)
                    pass
                else:
                    messagebox.showerror("Error", f"Failed to update student: {str(e)}")
                    return
        
        # Local mode (either by design or after fallback)
        if not operation_successful:
            try:
                if student_id not in self.students:
                    messagebox.showerror("Error", "Student ID not found")
                    return
                
                self.students[student_id].update({
                    "name": name,
                    "class": class_name,
                    "major": major
                })
                operation_successful = True
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update student locally: {str(e)}")
                return
        
        if operation_successful:
            self.update_student_list()
            self.clear_student_fields()
            mode_text = "in database" if self.use_mongodb else "locally"
            messagebox.showinfo("Success", f"Student updated successfully {mode_text}")
    
    def delete_student(self):
        student_id = self.student_id_entry.get().strip()
        
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID")
            return
        
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete student {student_id} and all their scores?")
        if not result:
            return
        
        # Try MongoDB first, then fallback to local if needed
        operation_successful = False
        
        if self.use_mongodb and self.students_collection is not None:
            try:
                # MongoDB mode - check student exists
                student = self.students_collection.find_one({"student_id": student_id})
                if not student:
                    messagebox.showerror("Error", "Student ID not found")
                    return
                
                # Delete scores first, then student
                self.scores_collection.delete_many({"student_id": student_id})
                self.students_collection.delete_one({"student_id": student_id})
                operation_successful = True
                
            except Exception as e:
                print(f"MongoDB delete_student failed: {e}")
                # Fallback to local mode
                if self._fallback_to_local("Delete Student"):
                    # Retry in local mode (will be handled by the local mode block below)
                    pass
                else:
                    messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
                    return
        
        # Local mode (either by design or after fallback)
        if not operation_successful:
            try:
                if student_id not in self.students:
                    messagebox.showerror("Error", "Student ID not found")
                    return
                
                del self.students[student_id]
                operation_successful = True
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student locally: {str(e)}")
                return
        
        if operation_successful:
            self.update_student_list()
            self.clear_student_fields()
            mode_text = "from database" if self.use_mongodb else "locally"
            messagebox.showinfo("Success", f"Student deleted successfully {mode_text}")
    
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
        current_time = datetime.now()
        
        # Validate scores first
        try:
            scores_to_save = []
            
            for subject, entry in self.score_entries.items():
                score_text = entry.get().strip()
                if score_text:
                    try:
                        score = float(score_text)
                        if 0 <= score <= 100:
                            scores_to_save.append({
                                "student_id": student_id,
                                "subject": subject,
                                "score": score,
                                "date_recorded": current_time
                            })
                        else:
                            messagebox.showerror("Error", f"Score for {subject} must be between 0-100")
                            return
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid score for {subject}")
                        return
            
            if not scores_to_save:
                messagebox.showwarning("Warning", "No scores to save")
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Error validating scores: {str(e)}")
            return
        
        # Check if student exists (both modes)
        if self.use_mongodb and self.students_collection is not None:
            try:
                if not self.students_collection.find_one({"student_id": student_id}):
                    messagebox.showerror("Error", "Student not found")
                    return
            except:
                self._fallback_to_local()
        
        if not self.use_mongodb and student_id not in self.students:
            messagebox.showerror("Error", "Student not found")
            return
        
        # Save scores (try MongoDB first, fallback to local)
        operation_successful = False
        
        if self.use_mongodb and self.scores_collection is not None:
            try:
                self.scores_collection.insert_many(scores_to_save)
                operation_successful = True
            except:
                self._fallback_to_local()
        
        # Local mode (either by design or after fallback)
        if not operation_successful:
            if "scores" not in self.students[student_id]:
                self.students[student_id]["scores"] = {}
            
            for score_data in scores_to_save:
                subject = score_data["subject"]
                if subject not in self.students[student_id]["scores"]:
                    self.students[student_id]["scores"][subject] = []
                
                self.students[student_id]["scores"][subject].append({
                    "score": score_data["score"],
                    "date": score_data["date_recorded"].strftime("%Y-%m-%d")
                })
            
            operation_successful = True
        
        if operation_successful:
            self.update_student_list()
            self.update_score_history()
            self.clear_score_fields()
            mode_text = "to database" if self.use_mongodb else "locally"
            messagebox.showinfo("Success", f"Saved {len(scores_to_save)} scores successfully {mode_text}")
    
    def update_score_history(self):
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        
        selected = self.score_student_var.get()
        if not selected:
            return
        
        student_id = selected.split(" - ")[0]
        
        # Try MongoDB first, then fallback to local if needed
        scores_loaded = False
        
        if self.use_mongodb and self.scores_collection is not None:
            try:
                # MongoDB mode
                scores = list(self.scores_collection.find(
                    {"student_id": student_id},
                    {"_id": 0}
                ).sort("date_recorded", -1))
                
                for score_data in scores:
                    grade = self.get_grade(score_data["score"])
                    date_display = score_data["date_recorded"].strftime("%Y-%m-%d")
                    self.score_tree.insert("", "end", values=(
                        date_display, score_data["subject"], f"{score_data['score']:.1f}", grade
                    ))
                
                scores_loaded = True
                
            except Exception as e:
                print(f"MongoDB update_score_history failed: {e}")
                # Fallback to local mode
                if self._fallback_to_local("Load Score History"):
                    # Retry in local mode (will be handled by the local mode block below)
                    pass
                else:
                    print(f"Failed to load score history: {str(e)}")
                    return
        
        # Local mode (either by design or after fallback)
        if not scores_loaded:
            try:
                if student_id not in self.students:
                    return
                
                scores = self.students[student_id].get("scores", {})
                for subject, score_list in scores.items():
                    for score_data in score_list:
                        grade = self.get_grade(score_data["score"])
                        self.score_tree.insert("", "end", values=(
                            score_data["date"], subject, score_data["score"], grade
                        ))
                
                scores_loaded = True
                
            except Exception as e:
                print(f"Failed to load score history locally: {str(e)}")
                return
    
    def get_grade(self, score):
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "B+"
        elif score >= 80:
            return "B"
        elif score >= 75:
            return "C+"
        elif score >= 70:
            return "C"
        elif score >= 65:
            return "D+"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def calculate_average_score(self, student_id):
        # Try MongoDB first, then fallback to local if needed
        if self.use_mongodb and self.scores_collection is not None:
            try:
                # MongoDB mode - calculate average of latest scores per subject
                pipeline = [
                    {"$match": {"student_id": student_id}},
                    {"$sort": {"date_recorded": -1}},
                    {"$group": {
                        "_id": "$subject",
                        "latest_score": {"$first": "$score"}
                    }},
                    {"$group": {
                        "_id": None,
                        "average": {"$avg": "$latest_score"}
                    }}
                ]
                
                result = list(self.scores_collection.aggregate(pipeline))
                return result[0]["average"] if result else 0
                
            except Exception as e:
                print(f"MongoDB calculate_average_score failed: {e}")
                # Silently fallback to local mode (don't show error dialog for this)
                self._cleanup_mongodb()
        
        # Local mode (either by design or after fallback)
        try:
            if student_id not in self.students:
                return 0
            
            scores = self.students[student_id].get("scores", {})
            total_score = 0
            total_count = 0
            
            for subject_scores in scores.values():
                if subject_scores:
                    latest_score = subject_scores[-1]["score"]
                    total_score += latest_score
                    total_count += 1
            
            return total_score / total_count if total_count > 0 else 0
            
        except Exception as e:
            print(f"Error calculating average score locally: {e}")
            return 0
    
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
        student_data = self.students[student_id]
        
        report = f"INDIVIDUAL STUDENT REPORT\n"
        report += "=" * 50 + "\n\n"
        report += f"Student ID: {student_id}\n"
        report += f"Name: {student_data['name']}\n"
        report += f"Class: {student_data['class']}\n"
        report += f"Major: {student_data['major']}\n\n"
        
        report += "SUBJECT SCORES:\n"
        report += "-" * 30 + "\n"
        
        total_score = 0
        subject_count = 0
        
        for subject in self.subjects:
            if subject in student_data.get("scores", {}):
                scores = student_data["scores"][subject]
                if scores:
                    latest_score = scores[-1]["score"]
                    grade = self.get_grade(latest_score)
                    report += f"{subject:<15}: {latest_score:>6.1f} ({grade})\n"
                    total_score += latest_score
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
    
    def generate_class_report(self):
        if not self.students:
            messagebox.showerror("Error", "No students available")
            return
        
        classes = {}
        for student_id, data in self.students.items():
            class_name = data["class"]
            if class_name not in classes:
                classes[class_name] = []
            classes[class_name].append((student_id, data))
        
        report = "CLASS REPORT\n"
        report += "=" * 50 + "\n\n"
        
        for class_name, students in sorted(classes.items()):
            report += f"CLASS: {class_name}\n"
            report += "-" * 30 + "\n"
            
            total_avg = 0
            student_count = 0
            
            for student_id, data in students:
                avg = self.calculate_average_score(student_id)
                if avg > 0:
                    grade = self.get_grade(avg)
                    report += f"{data['name']:<20} (ID: {student_id}): {avg:>6.1f} ({grade})\n"
                    total_avg += avg
                    student_count += 1
                else:
                    report += f"{data['name']:<20} (ID: {student_id}): {'No Score':>10}\n"
            
            if student_count > 0:
                class_avg = total_avg / student_count
                report += f"\nClass Average: {class_avg:.1f}\n"
            
            report += "\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def generate_subject_report(self):
        if not self.students:
            messagebox.showerror("Error", "No students available")
            return
        
        report = "SUBJECT ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"
        
        for subject in self.subjects:
            report += f"SUBJECT: {subject}\n"
            report += "-" * 30 + "\n"
            
            scores = []
            students_with_scores = []
            
            for student_id, data in self.students.items():
                if subject in data.get("scores", {}):
                    subject_scores = data["scores"][subject]
                    if subject_scores:
                        score = subject_scores[-1]["score"]
                        scores.append(score)
                        students_with_scores.append((data["name"], student_id, score))
            
            if scores:
                avg_score = sum(scores) / len(scores)
                max_score = max(scores)
                min_score = min(scores)
                
                report += f"Students with scores: {len(scores)}\n"
                report += f"Average Score: {avg_score:.1f}\n"
                report += f"Highest Score: {max_score:.1f}\n"
                report += f"Lowest Score: {min_score:.1f}\n\n"
                
                report += "Top performers:\n"
                students_with_scores.sort(key=lambda x: x[2], reverse=True)
                for i, (name, student_id, score) in enumerate(students_with_scores[:5]):
                    grade = self.get_grade(score)
                    report += f"  {i+1}. {name} (ID: {student_id}): {score:.1f} ({grade})\n"
            else:
                report += "No scores recorded for this subject\n"
            
            report += "\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def update_statistics(self):
        if not self.students:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, "No student data available")
            return
        
        stats = "SYSTEM STATISTICS\n"
        stats += "=" * 40 + "\n\n"
        
        # Basic stats
        stats += f"Total Students: {len(self.students)}\n\n"
        
        # Class distribution
        classes = {}
        majors = {}
        for student_data in self.students.values():
            class_name = student_data["class"]
            major = student_data["major"]
            classes[class_name] = classes.get(class_name, 0) + 1
            majors[major] = majors.get(major, 0) + 1
        
        stats += "CLASS DISTRIBUTION:\n"
        for class_name, count in sorted(classes.items()):
            stats += f"  {class_name}: {count} students\n"
        
        stats += "\nMAJOR DISTRIBUTION:\n"
        for major, count in sorted(majors.items()):
            stats += f"  {major}: {count} students\n"
        
        # Subject averages
        stats += "\nSUBJECT AVERAGES:\n"
        for subject in self.subjects:
            scores = []
            for student_data in self.students.values():
                if subject in student_data.get("scores", {}):
                    subject_scores = student_data["scores"][subject]
                    if subject_scores:
                        scores.append(subject_scores[-1]["score"])
            
            if scores:
                avg = sum(scores) / len(scores)
                stats += f"  {subject:<15}: {avg:>6.1f} ({len(scores)} students)\n"
            else:
                stats += f"  {subject:<15}: {'No Data':>10}\n"
        
        # Overall system average
        all_averages = []
        for student_id in self.students:
            avg = self.calculate_average_score(student_id)
            if avg > 0:
                all_averages.append(avg)
        
        if all_averages:
            system_avg = sum(all_averages) / len(all_averages)
            stats += f"\nSYSTEM AVERAGE: {system_avg:.1f}\n"
            stats += f"Students with scores: {len(all_averages)}\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def export_to_csv(self):
        if not self.students:
            messagebox.showerror("Error", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Header
                    header = ["Student ID", "Name", "Class", "Major"] + self.subjects + ["Average"]
                    writer.writerow(header)
                    
                    # Data
                    for student_id, data in self.students.items():
                        row = [student_id, data["name"], data["class"], data["major"]]
                        
                        # Add subject scores
                        for subject in self.subjects:
                            if subject in data.get("scores", {}):
                                scores = data["scores"][subject]
                                if scores:
                                    row.append(scores[-1]["score"])
                                else:
                                    row.append("")
                            else:
                                row.append("")
                        
                        # Add average
                        avg = self.calculate_average_score(student_id)
                        row.append(f"{avg:.1f}" if avg > 0 else "")
                        
                        writer.writerow(row)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    
    def close_connection(self):
        """Close MongoDB connection"""
        try:
            if hasattr(self, 'use_mongodb') and self.use_mongodb:
                if hasattr(self, 'client') and self.client:
                    self.client.close()
                    print("MongoDB connection closed.")
        except Exception as e:
            print(f"Error closing MongoDB connection: {e}")
        finally:
            self.use_mongodb = False

def main():
    try:
        root = tk.Tk()
        app = StudentScoreSystem(root)
        
        # Close MongoDB connection when window is closed
        def on_closing():
            try:
                app.close_connection()
            except Exception as e:
                print(f"Error during connection close: {e}")
            finally:
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"Error occurred during program execution: {e}")
        print("Attempting to run in basic mode...")
        
        # Try again in basic mode
        try:
            root = tk.Tk()
            root.title("Student Score Management System (Local Mode)")
            root.geometry("800x600")
            
            # Display simple error message
            error_label = tk.Label(root, 
                text=f"An error occurred: {str(e)}\nRunning in local mode.", 
                font=("Arial", 12), 
                fg="red")
            error_label.pack(pady=50)
            
            retry_btn = tk.Button(root, text="Retry", command=root.quit, font=("Arial", 10))
            retry_btn.pack(pady=10)
            
            root.mainloop()
            
        except Exception as final_error:
            print(f"Final error: {final_error}")
            print("Exiting program.")

if __name__ == "__main__":
    main()