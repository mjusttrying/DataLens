from gpt4all import GPT4All

class AIService:
    def __init__(self):
        self.model = None

    def initialize_model(self):
        try:
            # Initialize with a small, efficient model
            self.model = GPT4All("orca-mini-3b-gguf2-q4_0")
            return True
        except Exception as e:
            print(f"Error initializing AI model: {e}")
            return False

    def get_sql_suggestion(self, context):
        if not self.model:
            if not self.initialize_model():
                return "Error: Could not initialize AI model"

        prompt = f"""
        You are a SQL expert. Help write or improve the following SQL query request:
        
        {context}
        
        Provide the SQL query and a brief explanation.
        """

        try:
            response = self.model.generate(prompt, max_tokens=200)
            return response
        except Exception as e:
            return f"Error generating suggestion: {e}"

    def analyze_query(self, query):
        if not self.model:
            if not self.initialize_model():
                return "Error: Could not initialize AI model"

        prompt = f"""
        Analyze this SQL query and suggest improvements or point out potential issues:
        
        {query}
        """

        try:
            response = self.model.generate(prompt, max_tokens=200)
            return response
        except Exception as e:
            return f"Error analyzing query: {e}"
