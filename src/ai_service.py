from gpt4all import GPT4All
import os
from pathlib import Path

class AIService:
    def __init__(self):
        self.model = None
        self.model_name = "orca-mini-3b-gguf2-q4_0"
        # Get the default model directory from GPT4All
        self.model_path = os.path.join(str(Path.home()), ".cache", "gpt4all")
        self.download_progress = 0
        self.loading_progress = 0

    def progress_callback(self, progress):
        """Callback function to track download/loading progress"""
        self.download_progress = progress
        print(f"Model download progress: {progress:.2f}%")
        return True  # Return True to continue downloading

    def loading_callback(self, progress):
        """Callback function to track model loading progress"""
        self.loading_progress = progress
        print(f"Model loading progress: {progress:.2f}%")
        return True  # Return True to continue loading

    def check_model_exists(self):
        """Check if the model file exists locally"""
        model_files = os.listdir(self.model_path) if os.path.exists(self.model_path) else []
        return any(self.model_name in file for file in model_files)

    def download_model(self):
        """Download the model if it doesn't exist"""
        try:
            print(f"Downloading model {self.model_name}...")
            # GPT4All will automatically download the model if it doesn't exist
            # when we pass the download_callback parameter
            return True
        except Exception as e:
            print(f"Error downloading model: {e}")
            return False

    def initialize_model(self):
        try:
            # Check if model exists, download if needed
            if not self.check_model_exists():
                print(f"Model {self.model_name} not found. Starting download...")
                if not self.download_model():
                    return False

            print(f"Loading model {self.model_name}...")
            # Initialize with a small, efficient model
            self.model = GPT4All(
                model_name=self.model_name,
                download_callback=self.progress_callback,
                model_path=self.model_path,
                allow_download=True,
                verbose=True
            )
            print(f"Model {self.model_name} loaded successfully!")
            return True
        except FileNotFoundError:
            print(f"Error: Model file for {self.model_name} not found and could not be downloaded.")
            return False
        except PermissionError:
            print(f"Error: Permission denied when trying to access model directory {self.model_path}.")
            return False
        except Exception as e:
            print(f"Error initializing AI model: {e}")
            return False

    def get_sql_suggestion(self, context):
        if not self.model:
            print("AI model not initialized, attempting to initialize...")
            if not self.initialize_model():
                return "Error: Could not initialize AI model. Please check the logs for details."

        prompt = f"""
        You are a SQL expert. Help write or improve the following SQL query request:
        
        {context}
        
        Provide the SQL query and a brief explanation.
        """

        try:
            response = self.model.generate(
                prompt=prompt, 
                max_tokens=200,
                temp=0.7,
                top_k=40,
                top_p=0.4,
                repeat_penalty=1.18
            )
            return response
        except RuntimeError as e:
            error_msg = str(e)
            if "context window" in error_msg.lower():
                return "Error: The prompt is too long for the model's context window. Please provide a shorter query."
            return f"Error generating suggestion: {e}"
        except Exception as e:
            return f"Error generating suggestion: {e}"

    def analyze_query(self, query):
        if not self.model:
            print("AI model not initialized, attempting to initialize...")
            if not self.initialize_model():
                return "Error: Could not initialize AI model. Please check the logs for details."

        prompt = f"""
        Analyze this SQL query and suggest improvements or point out potential issues:
        
        {query}
        """

        try:
            response = self.model.generate(
                prompt=prompt, 
                max_tokens=200,
                temp=0.7,
                top_k=40,
                top_p=0.4,
                repeat_penalty=1.18
            )
            return response
        except RuntimeError as e:
            error_msg = str(e)
            if "context window" in error_msg.lower():
                return "Error: The prompt is too long for the model's context window. Please provide a shorter query."
            return f"Error analyzing query: {e}"
        except Exception as e:
            return f"Error analyzing query: {e}"
51|
52|    def get_model_status(self):
53|        """Return the current status of the model"""
54|        if self.model:
55|            return {"status": "loaded", "model_name": self.model_name}
56|        else:
57|            if self.download_progress > 0 and self.download_progress < 100:
58|                return {"status": "downloading", "progress": self.download_progress}
59|            elif self.loading_progress > 0 and self.loading_progress < 100:
60|                return {"status": "loading", "progress": self.loading_progress}
61|            else:
62|                return {"status": "not_loaded"}
