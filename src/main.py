import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from query_editor import QueryEditor
from ai_service import AIService

class DataLensApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ai_service()
        self.init_ui()
        
    def init_ai_service(self):
        self.ai_service = AIService()
        try:
            self.ai_service.initialize_model()
        except Exception as e:
            QMessageBox.warning(
                self,
                "AI Service Warning",
                "AI service initialization failed. Some features may be limited.\nError: " + str(e)
            )
        
    def init_ui(self):
        self.setWindowTitle("DataLens - AI Data Analytics Assistant")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Initialize tabs
        self.query_editor = QueryEditor(ai_service=self.ai_service)
        self.visualization_tab = QWidget()
        self.ai_assistant_tab = QWidget()
        
        tabs.addTab(self.query_editor, "SQL Query Editor")
        tabs.addTab(self.visualization_tab, "Data Visualization")
        tabs.addTab(self.ai_assistant_tab, "AI Assistant")
        
        layout.addWidget(tabs)

def main():
    app = QApplication(sys.argv)
    window = DataLensApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
