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

class ProfessorAdminSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Professor Administration System")
        self.root.geometry("1024x768")
        
        # UTF-8 encoding setup
        try:
            self.root.tk.call('encoding', 'system', 'utf-8')
            self.root.tk.call('tk', 'scaling', 1.0)
        except:
            pass
        
        # Font setup
        self.setup_fonts()
        
        # Local data initialization
        self.professors = {}
        
        # Department and position options
        self.departments = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", "Engineering", "Business", "Literature"]
        self.positions = ["Professor", "Associate Professor", "Assistant Professor", "Lecturer", "Emeritus Professor"]
        self.specializations = ["AI/Machine Learning", "Software Engineering", "Database Systems", "Network Security", "Web Development", "Data Science", "Computer Graphics", "Systems Programming"]
        
        # Initialize MongoDB-related attributes
        self.client = None
        self.db = None
        self.professors_collection = None
        self.use_mongodb = False
        
        # Create GUI widgets first
        self.create_widgets()
        
        # MongoDB connection setup
        self.root.after(100, self.setup_mongodb)
        
        # Update professor list after a delay
        self.root.after(200, self.update_professor_list)
    
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
        self.professors_collection = None
        self.use_mongodb = False
        
        try:
            from pymongo import MongoClient
            
            self.client = MongoClient(
                'mongodb://localhost:27017/',
                serverSelectionTimeoutMS=50,
                connectTimeoutMS=50,
                socketTimeoutMS=50,
                connect=False
            )
            
            self.client.admin.command('ping')
            
            self.db = self.client['professor_admin_db']
            self.professors_collection = self.db['professors']
            
            try:
                self.professors_collection.create_index("professor_id", unique=True)
                self.professors_collection.create_index([("department", 1), ("position", 1)])
            except:
                pass
            
            self.use_mongodb = True
            
        except:
            self._cleanup_mongodb()
        
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
        self.professors_collection = None
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
        
        # Professor Management Tab
        self.create_professor_tab()
        
        # Search & Sort Tab
        self.create_search_tab()
        
        # Reports Tab
        self.create_reports_tab()
        
        # Statistics Tab
        self.create_statistics_tab()
        
    def create_professor_tab(self):
        professor_frame = ttk.Frame(self.notebook)
        self.notebook.add(professor_frame, text="Professor Management")
        
        # Input frame
        input_frame = ttk.LabelFrame(professor_frame, text="Add/Edit Professor", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Professor ID
        ttk.Label(input_frame, text="Professor ID:", font=self.title_font).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.professor_id_entry = ttk.Entry(input_frame, width=30, font=self.title_font)
        self.professor_id_entry.grid(row=0, column=1, padx=8, pady=8, ipady=8)
        
        # Professor Name
        ttk.Label(input_frame, text="Name:", font=self.title_font).grid(row=0, column=2, sticky="w", padx=8, pady=8)
        self.professor_name_entry = ttk.Entry(input_frame, width=40, font=self.title_font)
        self.professor_name_entry.grid(row=0, column=3, padx=8, pady=8, ipady=8)
        
        # Email
        ttk.Label(input_frame, text="Email:", font=self.title_font).grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.professor_email_entry = ttk.Entry(input_frame, width=30, font=self.title_font)
        self.professor_email_entry.grid(row=1, column=1, padx=8, pady=8, ipady=8)
        
        # Phone
        ttk.Label(input_frame, text="Phone:", font=self.title_font).grid(row=1, column=2, sticky="w", padx=8, pady=8)
        self.professor_phone_entry = ttk.Entry(input_frame, width=40, font=self.title_font)
        self.professor_phone_entry.grid(row=1, column=3, padx=8, pady=8, ipady=8)
        
        # Department
        ttk.Label(input_frame, text="Department:", font=self.title_font).grid(row=2, column=0, sticky="w", padx=8, pady=8)
        self.professor_dept_var = tk.StringVar()
        self.professor_dept_combo = ttk.Combobox(input_frame, textvariable=self.professor_dept_var, 
                                               values=self.departments, width=28, font=self.title_font)
        self.professor_dept_combo.grid(row=2, column=1, padx=8, pady=8, ipady=8)
        
        # Position
        ttk.Label(input_frame, text="Position:", font=self.title_font).grid(row=2, column=2, sticky="w", padx=8, pady=8)
        self.professor_pos_var = tk.StringVar()
        self.professor_pos_combo = ttk.Combobox(input_frame, textvariable=self.professor_pos_var, 
                                              values=self.positions, width=38, font=self.title_font)
        self.professor_pos_combo.grid(row=2, column=3, padx=8, pady=8, ipady=8)
        
        # Specialization
        ttk.Label(input_frame, text="Specialization:", font=self.title_font).grid(row=3, column=0, sticky="w", padx=8, pady=8)
        self.professor_spec_var = tk.StringVar()
        self.professor_spec_combo = ttk.Combobox(input_frame, textvariable=self.professor_spec_var, 
                                               values=self.specializations, width=28, font=self.title_font)
        self.professor_spec_combo.grid(row=3, column=1, padx=8, pady=8, ipady=8)
        
        # Office Location
        ttk.Label(input_frame, text="Office:", font=self.title_font).grid(row=3, column=2, sticky="w", padx=8, pady=8)
        self.professor_office_entry = ttk.Entry(input_frame, width=40, font=self.title_font)
        self.professor_office_entry.grid(row=3, column=3, padx=8, pady=8, ipady=8)
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Add Professor", command=self.add_professor).pack(side="left", padx=5, ipady=8)
        ttk.Button(btn_frame, text="Update Professor", command=self.update_professor).pack(side="left", padx=5, ipady=8)
        ttk.Button(btn_frame, text="Delete Professor", command=self.delete_professor).pack(side="left", padx=5, ipady=8)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_professor_fields).pack(side="left", padx=5, ipady=8)
        
        # Professor list
        list_frame = ttk.LabelFrame(professor_frame, text="Professors", padding="10")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for professor list
        columns = ("ID", "Name", "Department", "Position", "Email", "Phone", "Office")
        self.professor_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.professor_tree.heading(col, text=col)
            if col == "Name":
                self.professor_tree.column(col, width=150)
            elif col in ["Email", "Phone"]:
                self.professor_tree.column(col, width=120)
            else:
                self.professor_tree.column(col, width=100)
        
        scrollbar_professor = ttk.Scrollbar(list_frame, orient="vertical", command=self.professor_tree.yview)
        self.professor_tree.configure(yscrollcommand=scrollbar_professor.set)
        
        self.professor_tree.pack(side="left", fill="both", expand=True)
        scrollbar_professor.pack(side="right", fill="y")
        
        self.professor_tree.bind("<ButtonRelease-1>", self.on_professor_select)
        
    def create_search_tab(self):
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search & Sort")
        
        # Search controls
        search_control_frame = ttk.LabelFrame(search_frame, text="Search Options", padding="10")
        search_control_frame.pack(fill="x", padx=10, pady=5)
        
        # Search by name
        ttk.Label(search_control_frame, text="Search by Name:", font=self.title_font).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.search_name_entry = ttk.Entry(search_control_frame, width=30, font=self.title_font)
        self.search_name_entry.grid(row=0, column=1, padx=8, pady=8, ipady=8)
        self.search_name_entry.bind("<KeyRelease>", self.on_search_change)
        
        # Filter by department
        ttk.Label(search_control_frame, text="Filter by Department:", font=self.title_font).grid(row=0, column=2, sticky="w", padx=8, pady=8)
        self.filter_dept_var = tk.StringVar()
        filter_dept_values = ["All"] + self.departments
        self.filter_dept_combo = ttk.Combobox(search_control_frame, textvariable=self.filter_dept_var, 
                                            values=filter_dept_values, width=28, font=self.title_font)
        self.filter_dept_combo.grid(row=0, column=3, padx=8, pady=8, ipady=8)
        self.filter_dept_combo.set("All")
        self.filter_dept_combo.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # Filter by position
        ttk.Label(search_control_frame, text="Filter by Position:", font=self.title_font).grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.filter_pos_var = tk.StringVar()
        filter_pos_values = ["All"] + self.positions
        self.filter_pos_combo = ttk.Combobox(search_control_frame, textvariable=self.filter_pos_var, 
                                           values=filter_pos_values, width=28, font=self.title_font)
        self.filter_pos_combo.grid(row=1, column=1, padx=8, pady=8, ipady=8)
        self.filter_pos_combo.set("All")
        self.filter_pos_combo.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # Sort options
        ttk.Label(search_control_frame, text="Sort by:", font=self.title_font).grid(row=1, column=2, sticky="w", padx=8, pady=8)
        self.sort_var = tk.StringVar()
        sort_options = ["Name", "Department", "Position", "ID"]
        self.sort_combo = ttk.Combobox(search_control_frame, textvariable=self.sort_var, 
                                     values=sort_options, width=28, font=self.title_font)
        self.sort_combo.grid(row=1, column=3, padx=8, pady=8, ipady=8)
        self.sort_combo.set("Name")
        self.sort_combo.bind("<<ComboboxSelected>>", self.on_sort_change)
        
        # Action buttons
        action_frame = ttk.Frame(search_control_frame)
        action_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(action_frame, text="Clear Filters", command=self.clear_filters).pack(side="left", padx=5, ipady=8)
        ttk.Button(action_frame, text="Refresh List", command=self.update_professor_list).pack(side="left", padx=5, ipady=8)
        
        # Filtered results
        results_frame = ttk.LabelFrame(search_frame, text="Search Results", padding="10")
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for search results
        search_columns = ("ID", "Name", "Department", "Position", "Specialization", "Email", "Office")
        self.search_tree = ttk.Treeview(results_frame, columns=search_columns, show="headings", height=15)
        
        for col in search_columns:
            self.search_tree.heading(col, text=col)
            if col == "Name":
                self.search_tree.column(col, width=150)
            elif col in ["Email", "Specialization"]:
                self.search_tree.column(col, width=120)
            else:
                self.search_tree.column(col, width=100)
        
        scrollbar_search = ttk.Scrollbar(results_frame, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar_search.set)
        
        self.search_tree.pack(side="left", fill="both", expand=True)
        scrollbar_search.pack(side="right", fill="y")
        
    def create_reports_tab(self):
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Report generation
        gen_frame = ttk.LabelFrame(reports_frame, text="Generate Reports", padding="10")
        gen_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(gen_frame, text="Department Report", command=self.generate_department_report).pack(side="left", padx=5, ipady=8)
        ttk.Button(gen_frame, text="Position Report", command=self.generate_position_report).pack(side="left", padx=5, ipady=8)
        ttk.Button(gen_frame, text="Contact List", command=self.generate_contact_report).pack(side="left", padx=5, ipady=8)
        ttk.Button(gen_frame, text="Export to CSV", command=self.export_to_csv).pack(side="left", padx=5, ipady=8)
        
        # CSV Import section
        import_frame = ttk.LabelFrame(reports_frame, text="Import Data", padding="10")
        import_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(import_frame, text="Import from CSV", command=self.import_from_csv).pack(side="left", padx=5, ipady=8)
        ttk.Button(import_frame, text="Download CSV Template", command=self.download_csv_template).pack(side="left", padx=5, ipady=8)
        
        # Import instructions
        instructions = tk.Label(import_frame, 
            text="CSV Format: Professor ID, Name, Department, Position, Specialization, Email, Phone, Office", 
            font=self.default_font, fg="blue", wraplength=800)
        instructions.pack(pady=5)
        
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
    
    def add_professor(self):
        professor_id = self.professor_id_entry.get().strip()
        name = self.professor_name_entry.get().strip()
        email = self.professor_email_entry.get().strip()
        phone = self.professor_phone_entry.get().strip()
        department = self.professor_dept_var.get().strip()
        position = self.professor_pos_var.get().strip()
        specialization = self.professor_spec_var.get().strip()
        office = self.professor_office_entry.get().strip()
        
        if not all([professor_id, name, email, department, position]):
            messagebox.showerror("Error", "Please fill required fields (ID, Name, Email, Department, Position)")
            return
        
        # Check for duplicate professor ID
        if self.use_mongodb and self.professors_collection is not None:
            try:
                if self.professors_collection.find_one({"professor_id": professor_id}):
                    messagebox.showerror("Error", "Professor ID already exists")
                    return
            except:
                self._fallback_to_local()
        
        if not self.use_mongodb and professor_id in self.professors:
            messagebox.showerror("Error", "Professor ID already exists")
            return
        
        # Add professor
        operation_successful = False
        
        if self.use_mongodb and self.professors_collection is not None:
            try:
                professor_data = {
                    "professor_id": professor_id,
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "position": position,
                    "specialization": specialization,
                    "office": office,
                    "created_at": datetime.now()
                }
                self.professors_collection.insert_one(professor_data)
                operation_successful = True
            except:
                self._fallback_to_local()
        
        # Local mode
        if not operation_successful:
            self.professors[professor_id] = {
                "name": name,
                "email": email,
                "phone": phone,
                "department": department,
                "position": position,
                "specialization": specialization,
                "office": office
            }
            operation_successful = True
        
        if operation_successful:
            self.update_professor_list()
            self.clear_professor_fields()
            mode_text = "in database" if self.use_mongodb else "locally"
            messagebox.showinfo("Success", f"Professor added successfully {mode_text}")
    
    def update_professor_list(self):
        # Clear both trees
        for item in self.professor_tree.get_children():
            self.professor_tree.delete(item)
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Load professors
        professors_loaded = False
        
        if self.use_mongodb and self.professors_collection is not None:
            try:
                professors = list(self.professors_collection.find({}, {"_id": 0}))
                
                for professor in professors:
                    self.professor_tree.insert("", "end", values=(
                        professor["professor_id"], professor["name"], professor["department"], 
                        professor["position"], professor.get("email", ""), 
                        professor.get("phone", ""), professor.get("office", "")
                    ))
                
                professors_loaded = True
                
            except:
                self._fallback_to_local()
        
        # Local mode
        if not professors_loaded:
            for professor_id, data in self.professors.items():
                self.professor_tree.insert("", "end", values=(
                    professor_id, data["name"], data["department"], data["position"],
                    data.get("email", ""), data.get("phone", ""), data.get("office", "")
                ))
        
        # Update search results
        self.update_search_results()
    
    def on_professor_select(self, event):
        selection = self.professor_tree.selection()
        if selection:
            item = self.professor_tree.item(selection[0])
            values = item['values']
            
            self.professor_id_entry.delete(0, tk.END)
            self.professor_id_entry.insert(0, values[0])
            self.professor_name_entry.delete(0, tk.END)
            self.professor_name_entry.insert(0, values[1])
            self.professor_dept_var.set(values[2])
            self.professor_pos_var.set(values[3])
            self.professor_email_entry.delete(0, tk.END)
            self.professor_email_entry.insert(0, values[4])
            self.professor_phone_entry.delete(0, tk.END)
            self.professor_phone_entry.insert(0, values[5])
            self.professor_office_entry.delete(0, tk.END)
            self.professor_office_entry.insert(0, values[6])
    
    def update_professor(self):
        professor_id = self.professor_id_entry.get().strip()
        name = self.professor_name_entry.get().strip()
        email = self.professor_email_entry.get().strip()
        phone = self.professor_phone_entry.get().strip()
        department = self.professor_dept_var.get().strip()
        position = self.professor_pos_var.get().strip()
        specialization = self.professor_spec_var.get().strip()
        office = self.professor_office_entry.get().strip()
        
        if not all([professor_id, name, email, department, position]):
            messagebox.showerror("Error", "Please fill required fields")
            return
        
        operation_successful = False
        
        if self.use_mongodb and self.professors_collection is not None:
            try:
                result = self.professors_collection.update_one(
                    {"professor_id": professor_id},
                    {"$set": {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "department": department,
                        "position": position,
                        "specialization": specialization,
                        "office": office,
                        "updated_at": datetime.now()
                    }}
                )
                
                if result.matched_count == 0:
                    messagebox.showerror("Error", "Professor ID not found")
                    return
                
                operation_successful = True
                
            except:
                self._fallback_to_local()
        
        # Local mode
        if not operation_successful:
            if professor_id not in self.professors:
                messagebox.showerror("Error", "Professor ID not found")
                return
            
            self.professors[professor_id].update({
                "name": name,
                "email": email,
                "phone": phone,
                "department": department,
                "position": position,
                "specialization": specialization,
                "office": office
            })
            operation_successful = True
        
        if operation_successful:
            self.update_professor_list()
            self.clear_professor_fields()
            mode_text = "in database" if self.use_mongodb else "locally"
            messagebox.showinfo("Success", f"Professor updated successfully {mode_text}")
    
    def delete_professor(self):
        professor_id = self.professor_id_entry.get().strip()
        
        if not professor_id:
            messagebox.showerror("Error", "Please enter Professor ID")
            return
        
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete professor {professor_id}?")
        if not result:
            return
        
        operation_successful = False
        
        if self.use_mongodb and self.professors_collection is not None:
            try:
                professor = self.professors_collection.find_one({"professor_id": professor_id})
                if not professor:
                    messagebox.showerror("Error", "Professor ID not found")
                    return
                
                self.professors_collection.delete_one({"professor_id": professor_id})
                operation_successful = True
                
            except:
                self._fallback_to_local()
        
        # Local mode
        if not operation_successful:
            if professor_id not in self.professors:
                messagebox.showerror("Error", "Professor ID not found")
                return
            
            del self.professors[professor_id]
            operation_successful = True
        
        if operation_successful:
            self.update_professor_list()
            self.clear_professor_fields()
            mode_text = "from database" if self.use_mongodb else "locally"
            messagebox.showinfo("Success", f"Professor deleted successfully {mode_text}")
    
    def clear_professor_fields(self):
        self.professor_id_entry.delete(0, tk.END)
        self.professor_name_entry.delete(0, tk.END)
        self.professor_email_entry.delete(0, tk.END)
        self.professor_phone_entry.delete(0, tk.END)
        self.professor_dept_var.set("")
        self.professor_pos_var.set("")
        self.professor_spec_var.set("")
        self.professor_office_entry.delete(0, tk.END)
    
    def on_search_change(self, event):
        self.update_search_results()
    
    def on_filter_change(self, event):
        self.update_search_results()
    
    def on_sort_change(self, event):
        self.update_search_results()
    
    def clear_filters(self):
        self.search_name_entry.delete(0, tk.END)
        self.filter_dept_var.set("All")
        self.filter_pos_var.set("All")
        self.sort_var.set("Name")
        self.update_search_results()
    
    def update_search_results(self):
        # Clear search tree
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Get search criteria
        search_name = self.search_name_entry.get().strip().lower()
        filter_dept = self.filter_dept_var.get()
        filter_pos = self.filter_pos_var.get()
        sort_by = self.sort_var.get()
        
        # Get professor data
        professor_data = []
        
        if self.use_mongodb and self.professors_collection is not None:
            try:
                professors = list(self.professors_collection.find({}, {"_id": 0}))
                for professor in professors:
                    professor_data.append({
                        "id": professor["professor_id"],
                        "name": professor["name"],
                        "department": professor["department"],
                        "position": professor["position"],
                        "specialization": professor.get("specialization", ""),
                        "email": professor.get("email", ""),
                        "office": professor.get("office", "")
                    })
            except:
                self._fallback_to_local()
        
        if not self.use_mongodb:
            for professor_id, data in self.professors.items():
                professor_data.append({
                    "id": professor_id,
                    "name": data["name"],
                    "department": data["department"],
                    "position": data["position"],
                    "specialization": data.get("specialization", ""),
                    "email": data.get("email", ""),
                    "office": data.get("office", "")
                })
        
        # Filter data
        filtered_data = []
        for prof in professor_data:
            # Name search
            if search_name and search_name not in prof["name"].lower():
                continue
            
            # Department filter
            if filter_dept != "All" and prof["department"] != filter_dept:
                continue
            
            # Position filter
            if filter_pos != "All" and prof["position"] != filter_pos:
                continue
            
            filtered_data.append(prof)
        
        # Sort data
        if sort_by == "Name":
            filtered_data.sort(key=lambda x: x["name"])
        elif sort_by == "Department":
            filtered_data.sort(key=lambda x: x["department"])
        elif sort_by == "Position":
            filtered_data.sort(key=lambda x: x["position"])
        elif sort_by == "ID":
            filtered_data.sort(key=lambda x: x["id"])
        
        # Populate search tree
        for prof in filtered_data:
            self.search_tree.insert("", "end", values=(
                prof["id"], prof["name"], prof["department"], prof["position"],
                prof["specialization"], prof["email"], prof["office"]
            ))
    
    def generate_department_report(self):
        professor_data = self.get_all_professor_data()
        
        if not professor_data:
            messagebox.showerror("Error", "No professor data available")
            return
        
        departments = {}
        for prof in professor_data:
            dept = prof["department"]
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(prof)
        
        report = "DEPARTMENT REPORT\n"
        report += "=" * 50 + "\n\n"
        
        for dept_name, professors in sorted(departments.items()):
            report += f"DEPARTMENT: {dept_name}\n"
            report += "-" * 30 + "\n"
            report += f"Total Professors: {len(professors)}\n\n"
            
            # Group by position
            positions = {}
            for prof in professors:
                pos = prof["position"]
                if pos not in positions:
                    positions[pos] = []
                positions[pos].append(prof)
            
            for pos_name, pos_profs in sorted(positions.items()):
                report += f"  {pos_name}: {len(pos_profs)}\n"
                for prof in sorted(pos_profs, key=lambda x: x["name"]):
                    report += f"    - {prof['name']} (ID: {prof['id']})\n"
                    if prof.get("office"):
                        report += f"      Office: {prof['office']}\n"
                report += "\n"
            
            report += "\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def generate_position_report(self):
        professor_data = self.get_all_professor_data()
        
        if not professor_data:
            messagebox.showerror("Error", "No professor data available")
            return
        
        positions = {}
        for prof in professor_data:
            pos = prof["position"]
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(prof)
        
        report = "POSITION REPORT\n"
        report += "=" * 50 + "\n\n"
        
        for pos_name, professors in sorted(positions.items()):
            report += f"POSITION: {pos_name}\n"
            report += "-" * 30 + "\n"
            report += f"Total: {len(professors)}\n\n"
            
            # Group by department
            departments = {}
            for prof in professors:
                dept = prof["department"]
                if dept not in departments:
                    departments[dept] = []
                departments[dept].append(prof)
            
            for dept_name, dept_profs in sorted(departments.items()):
                report += f"  {dept_name}: {len(dept_profs)}\n"
                for prof in sorted(dept_profs, key=lambda x: x["name"]):
                    report += f"    - {prof['name']} (ID: {prof['id']})\n"
                    if prof.get("email"):
                        report += f"      Email: {prof['email']}\n"
                report += "\n"
            
            report += "\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def generate_contact_report(self):
        professor_data = self.get_all_professor_data()
        
        if not professor_data:
            messagebox.showerror("Error", "No professor data available")
            return
        
        report = "PROFESSOR CONTACT LIST\n"
        report += "=" * 50 + "\n\n"
        
        for prof in sorted(professor_data, key=lambda x: x["name"]):
            report += f"Name: {prof['name']}\n"
            report += f"ID: {prof['id']}\n"
            report += f"Department: {prof['department']}\n"
            report += f"Position: {prof['position']}\n"
            if prof.get("email"):
                report += f"Email: {prof['email']}\n"
            if prof.get("phone"):
                report += f"Phone: {prof['phone']}\n"
            if prof.get("office"):
                report += f"Office: {prof['office']}\n"
            if prof.get("specialization"):
                report += f"Specialization: {prof['specialization']}\n"
            report += "-" * 40 + "\n\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def get_all_professor_data(self):
        professor_data = []
        
        if self.use_mongodb and self.professors_collection is not None:
            try:
                professors = list(self.professors_collection.find({}, {"_id": 0}))
                for professor in professors:
                    professor_data.append({
                        "id": professor["professor_id"],
                        "name": professor["name"],
                        "department": professor["department"],
                        "position": professor["position"],
                        "specialization": professor.get("specialization", ""),
                        "email": professor.get("email", ""),
                        "phone": professor.get("phone", ""),
                        "office": professor.get("office", "")
                    })
            except:
                self._fallback_to_local()
        
        if not self.use_mongodb:
            for professor_id, data in self.professors.items():
                professor_data.append({
                    "id": professor_id,
                    "name": data["name"],
                    "department": data["department"],
                    "position": data["position"],
                    "specialization": data.get("specialization", ""),
                    "email": data.get("email", ""),
                    "phone": data.get("phone", ""),
                    "office": data.get("office", "")
                })
        
        return professor_data
    
    def update_statistics(self):
        professor_data = self.get_all_professor_data()
        
        if not professor_data:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, "No professor data available")
            return
        
        stats = "PROFESSOR SYSTEM STATISTICS\n"
        stats += "=" * 40 + "\n\n"
        
        # Basic stats
        stats += f"Total Professors: {len(professor_data)}\n\n"
        
        # Department distribution
        departments = {}
        positions = {}
        specializations = {}
        
        for prof in professor_data:
            dept = prof["department"]
            pos = prof["position"]
            spec = prof.get("specialization", "Not Specified")
            
            departments[dept] = departments.get(dept, 0) + 1
            positions[pos] = positions.get(pos, 0) + 1
            specializations[spec] = specializations.get(spec, 0) + 1
        
        stats += "DEPARTMENT DISTRIBUTION:\n"
        for dept, count in sorted(departments.items()):
            percentage = (count / len(professor_data)) * 100
            stats += f"  {dept}: {count} ({percentage:.1f}%)\n"
        
        stats += "\nPOSITION DISTRIBUTION:\n"
        for pos, count in sorted(positions.items()):
            percentage = (count / len(professor_data)) * 100
            stats += f"  {pos}: {count} ({percentage:.1f}%)\n"
        
        stats += "\nSPECIALIZATION DISTRIBUTION:\n"
        for spec, count in sorted(specializations.items()):
            if count > 0:
                percentage = (count / len(professor_data)) * 100
                stats += f"  {spec}: {count} ({percentage:.1f}%)\n"
        
        # Contact info completeness
        email_count = sum(1 for prof in professor_data if prof.get("email"))
        phone_count = sum(1 for prof in professor_data if prof.get("phone"))
        office_count = sum(1 for prof in professor_data if prof.get("office"))
        
        stats += "\nCONTACT INFORMATION COMPLETENESS:\n"
        stats += f"  Email addresses: {email_count}/{len(professor_data)} ({(email_count/len(professor_data)*100):.1f}%)\n"
        stats += f"  Phone numbers: {phone_count}/{len(professor_data)} ({(phone_count/len(professor_data)*100):.1f}%)\n"
        stats += f"  Office locations: {office_count}/{len(professor_data)} ({(office_count/len(professor_data)*100):.1f}%)\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def export_to_csv(self):
        professor_data = self.get_all_professor_data()
        
        if not professor_data:
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
                    header = ["Professor ID", "Name", "Department", "Position", "Specialization", "Email", "Phone", "Office"]
                    writer.writerow(header)
                    
                    # Data
                    for prof in professor_data:
                        row = [
                            prof["id"], prof["name"], prof["department"], prof["position"],
                            prof.get("specialization", ""), prof.get("email", ""),
                            prof.get("phone", ""), prof.get("office", "")
                        ]
                        writer.writerow(row)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def download_csv_template(self):
        """Download a CSV template file for importing professor data"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialvalue="professor_template.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Header
                    header = ["Professor ID", "Name", "Department", "Position", "Specialization", "Email", "Phone", "Office"]
                    writer.writerow(header)
                    
                    # Sample data
                    sample_data = [
                        ["PROF001", "Dr. John Smith", "Computer Science", "Professor", "AI/Machine Learning", "john.smith@university.edu", "555-0123", "CS Building 301"],
                        ["PROF002", "Dr. Jane Doe", "Mathematics", "Associate Professor", "Statistics", "jane.doe@university.edu", "555-0124", "Math Building 205"],
                        ["PROF003", "Dr. Bob Johnson", "Physics", "Assistant Professor", "Quantum Physics", "bob.johnson@university.edu", "555-0125", "Physics Building 105"]
                    ]
                    
                    for row in sample_data:
                        writer.writerow(row)
                
                messagebox.showinfo("Success", f"CSV template downloaded to {filename}\nThe template includes sample data for reference.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create template: {str(e)}")
    
    def import_from_csv(self):
        """Import professor data from CSV file"""
        filename = filedialog.askopenfilename(
            title="Select CSV file to import",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            # Read and validate CSV file
            imported_data = []
            duplicate_ids = []
            invalid_rows = []
            
            with open(filename, 'r', encoding='utf-8-sig') as csvfile:
                # Try to detect if file has header
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                has_header = sniffer.has_header(sample)
                
                reader = csv.reader(csvfile)
                
                # Skip header if present
                if has_header:
                    next(reader)
                
                row_number = 1 if has_header else 0
                
                for row in reader:
                    row_number += 1
                    
                    # Skip empty rows
                    if not any(cell.strip() for cell in row):
                        continue
                    
                    # Ensure row has enough columns (pad with empty strings if needed)
                    while len(row) < 8:
                        row.append("")
                    
                    professor_id = row[0].strip()
                    name = row[1].strip()
                    department = row[2].strip()
                    position = row[3].strip()
                    specialization = row[4].strip()
                    email = row[5].strip()
                    phone = row[6].strip()
                    office = row[7].strip()
                    
                    # Validate required fields
                    if not all([professor_id, name, department, position]):
                        invalid_rows.append(f"Row {row_number}: Missing required fields (ID, Name, Department, Position)")
                        continue
                    
                    # Check for duplicate IDs in current import
                    if professor_id in [data['professor_id'] for data in imported_data]:
                        duplicate_ids.append(f"Row {row_number}: Duplicate ID '{professor_id}' in import file")
                        continue
                    
                    # Check if professor already exists in database
                    if self.professor_exists(professor_id):
                        duplicate_ids.append(f"Row {row_number}: Professor ID '{professor_id}' already exists in database")
                        continue
                    
                    # Validate department and position
                    if department not in self.departments:
                        response = messagebox.askyesno("Unknown Department", 
                            f"Department '{department}' is not in the predefined list.\nDo you want to add it?")
                        if response:
                            self.departments.append(department)
                    
                    if position not in self.positions:
                        response = messagebox.askyesno("Unknown Position", 
                            f"Position '{position}' is not in the predefined list.\nDo you want to add it?")
                        if response:
                            self.positions.append(position)
                    
                    imported_data.append({
                        'professor_id': professor_id,
                        'name': name,
                        'department': department,
                        'position': position,
                        'specialization': specialization,
                        'email': email,
                        'phone': phone,
                        'office': office
                    })
            
            # Show validation results
            validation_report = f"CSV Import Validation Results:\n\n"
            validation_report += f"Valid records found: {len(imported_data)}\n"
            validation_report += f"Invalid rows: {len(invalid_rows)}\n"
            validation_report += f"Duplicate IDs: {len(duplicate_ids)}\n\n"
            
            if invalid_rows:
                validation_report += "Invalid Rows:\n"
                for error in invalid_rows:
                    validation_report += f"  - {error}\n"
                validation_report += "\n"
            
            if duplicate_ids:
                validation_report += "Duplicate IDs:\n"
                for error in duplicate_ids:
                    validation_report += f"  - {error}\n"
                validation_report += "\n"
            
            if not imported_data:
                validation_report += "No valid data to import."
                messagebox.showerror("Import Failed", validation_report)
                return
            
            # Ask user to confirm import
            validation_report += f"Do you want to import {len(imported_data)} valid records?"
            
            if not messagebox.askyesno("Confirm Import", validation_report):
                return
            
            # Import the data
            success_count = 0
            failed_imports = []
            
            for data in imported_data:
                try:
                    if self.import_single_professor(data):
                        success_count += 1
                    else:
                        failed_imports.append(f"Failed to import: {data['name']} (ID: {data['professor_id']})")
                except Exception as e:
                    failed_imports.append(f"Error importing {data['name']}: {str(e)}")
            
            # Update the professor list
            self.update_professor_list()
            
            # Show final results
            result_message = f"Import completed!\n\n"
            result_message += f"Successfully imported: {success_count} professors\n"
            result_message += f"Failed imports: {len(failed_imports)}\n"
            
            if failed_imports:
                result_message += "\nFailed imports:\n"
                for error in failed_imports[:5]:  # Show first 5 errors
                    result_message += f"  - {error}\n"
                if len(failed_imports) > 5:
                    result_message += f"  ... and {len(failed_imports) - 5} more errors"
            
            if success_count > 0:
                messagebox.showinfo("Import Completed", result_message)
            else:
                messagebox.showerror("Import Failed", result_message)
                
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to read CSV file: {str(e)}")
    
    def professor_exists(self, professor_id):
        """Check if professor ID already exists"""
        if self.use_mongodb and self.professors_collection is not None:
            try:
                return self.professors_collection.find_one({"professor_id": professor_id}) is not None
            except:
                pass
        
        return professor_id in self.professors
    
    def import_single_professor(self, data):
        """Import a single professor record"""
        try:
            # Try MongoDB first
            if self.use_mongodb and self.professors_collection is not None:
                try:
                    professor_data = {
                        "professor_id": data['professor_id'],
                        "name": data['name'],
                        "email": data['email'],
                        "phone": data['phone'],
                        "department": data['department'],
                        "position": data['position'],
                        "specialization": data['specialization'],
                        "office": data['office'],
                        "created_at": datetime.now(),
                        "imported": True
                    }
                    self.professors_collection.insert_one(professor_data)
                    return True
                except:
                    self._fallback_to_local()
            
            # Local mode
            if not self.use_mongodb:
                self.professors[data['professor_id']] = {
                    "name": data['name'],
                    "email": data['email'],
                    "phone": data['phone'],
                    "department": data['department'],
                    "position": data['position'],
                    "specialization": data['specialization'],
                    "office": data['office']
                }
                return True
            
            return False
            
        except Exception as e:
            print(f"Error importing professor {data['professor_id']}: {e}")
            return False
    
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
        app = ProfessorAdminSystem(root)
        
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
            root.title("Professor Administration System (Local Mode)")
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