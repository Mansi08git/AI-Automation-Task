﻿# AI-Automation-Task

This tool analyzes Python (.py), JavaScript (.js), and JSX (.jsx) files and provides insights such as function definitions, variable assignments, formatting issues, and best practices.

## Features
- Supports Python, JavaScript, and JSX files.
- Uses Pylint for Python and ESLint for JavaScript/JSX analysis.
- Provides an overall score and a breakdown of different coding aspects.
- Generates recommendations for code improvements

## Prerequisites
Before you run the bot, make sure to have the following dependencies installed:

1. Python 3.7+
2. Node.js (for ESLint support)
3. Pylint (pip install pylint)
4. ESLint (npm install -g eslint) 

## Installation

1. Clone this repository to your local machine:
```
git clone https://github.com/Mansi08git/AI-Automation-Task.git
```

2. Navigate to the project directory:
```
cd <project_directory>
```

3. Install required dependencies:
```
pip install -r requirements.txt
```

4. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows use venv\\Scripts\\activate
```

## Usage
### Running the backend 
1. Start the FastAPI server:
```
uvicorn main:app --reload
```

2. The API will be available at http://127.0.0.1:8000.

### Running the Frontend 
1. Navigate to the frontend directory:
```
cd frontend
```

2. Start the React app:
```
npx dev
```

3. The frontend will run at http://localhost:3000

## API Endpoints 
### Get/
- Description: Health check endpoint.
- Response: { "message": "CORS fixed!" }

### POST /analyze-code
- Description: Analyzes a Python, JavaScript, or JSX file.
- Request: A file upload (.py, .js, .jsx).
- Response:
```
{
  "overall_score": 85,
  "breakdown": {
    "naming": 8,
    "modularity": 18,
    "comments": 20,
    "formatting": 14,
    "reusability": 13,
    "best_practices": 20
  },
  "recommendations": ["Use camelCase for variable names.", "Refactor large functions."]
}
```
