from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QTextEdit, QPushButton, QLabel,
                           QComboBox, QTableWidget, QTableWidgetItem,
                           QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import sqlite3
import os

class QueryEditor(QWidget):
    def __init__(self, ai_service=None):
        super().__init__()
        self.ai_service = ai_service
        self.current_db = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Database connection section
        db_layout = QHBoxLayout()
        self.db_label = QLabel("Database:")
        self.db_combo = QComboBox()
        self.db_combo.addItem("Create New Database")
        self.refresh_btn = QPushButton("Refresh")
        self.create_db_btn = QPushButton("Create/Open Database")
        db_layout.addWidget(self.db_label)
        db_layout.addWidget(self.db_combo)
        db_layout.addWidget(self.create_db_btn)
        db_layout.addWidget(self.refresh_btn)
        db_layout.addStretch()
        
        # Query editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter your SQL query here...")
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Query")
        self.clear_btn = QPushButton("Clear")
        self.ai_help_btn = QPushButton("AI Help")
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.ai_help_btn)
        btn_layout.addStretch()
        
        # Results table
        self.results_table = QTableWidget()
        
        # Add all components to main layout
        layout.addLayout(db_layout)
        layout.addWidget(self.editor)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.results_table)
        
        self.setLayout(layout)
        
        # Connect signals
        self.run_btn.clicked.connect(self.run_query)
        self.clear_btn.clicked.connect(self.clear_editor)
        self.ai_help_btn.clicked.connect(self.get_ai_help)
        self.create_db_btn.clicked.connect(self.create_or_open_database)
        self.refresh_btn.clicked.connect(self.refresh_databases)
        
    def create_or_open_database(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Create/Open Database",
            "",
            "SQLite Database (*.db);;All Files (*)"
        )
        
        if file_name:
            try:
                self.current_db = sqlite3.connect(file_name)
                self.refresh_databases()
                QMessageBox.information(self, "Success", "Database connected successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not connect to database: {str(e)}")
        
    def refresh_databases(self):
        self.db_combo.clear()
        self.db_combo.addItem("Create New Database")
        
        # Add existing database files from the current directory
        for file in os.listdir('.'):
            if file.endswith('.db'):
                self.db_combo.addItem(file)
        
    def run_query(self):
        if not self.current_db:
            QMessageBox.warning(self, "Warning", "Please connect to a database first!")
            return
            
        query = self.editor.toPlainText()
        if not query.strip():
            return
            
        try:
            cursor = self.current_db.cursor()
            cursor.execute(query)
            
            # Get the results
            results = cursor.fetchall()
            
            # Get column names
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Update the table
            self.results_table.setRowCount(len(results))
            self.results_table.setColumnCount(len(columns))
            self.results_table.setHorizontalHeaderLabels(columns)
            
            # Fill the table
            for i, row in enumerate(results):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.results_table.setItem(i, j, item)
                    
            self.current_db.commit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error executing query: {str(e)}")
        
    def clear_editor(self):
        self.editor.clear()
        
    def get_ai_help(self):
        if not self.ai_service:
            QMessageBox.warning(self, "Warning", "AI service not available!")
            return
            
        current_query = self.editor.toPlainText()
        if current_query.strip():
            suggestion = self.ai_service.analyze_query(current_query)
        else:
            suggestion = self.ai_service.get_sql_suggestion("I need help writing a SQL query.")
            
        QMessageBox.information(self, "AI Suggestion", suggestion)
