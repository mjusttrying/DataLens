# DataLens

DataLens is an AI-powered data analytics tool that uses locally hosted AI models for privacy-conscious data analysis. It provides a user-friendly interface for SQL query management with AI assistance.

## Features

- Local AI-powered SQL query assistance
- SQLite database management
- Interactive query editor
- Results visualization
- Privacy-focused (all processing done locally)

## Installation

### macOS

1. Download the latest release from the Releases page
2. Extract the downloaded file
3. Move DataLens.app to your Applications folder
4. Right-click the app and select "Open" (required only for first launch)

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/DataLens.git
cd DataLens

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## Usage

1. Launch DataLens
2. Create or open a SQLite database
3. Write SQL queries in the editor
4. Use the AI assistant for query help
5. Execute queries and view results

## Technology Stack

- Python 3.12+
- PyQt6 for GUI
- GPT4All for AI functionality
- SQLite for database management
- Matplotlib & Seaborn for visualization

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
