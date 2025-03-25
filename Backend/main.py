#import libraries 
from fastapi import FastAPI, File, UploadFile
import os
import tempfile
import subprocess
import json
from fastapi.middleware.cors import CORSMiddleware
import shutil

#create instance of fastapi 
app = FastAPI()

#to solve internal server error issues 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#to verify all is working fine 
@app.get("/")
def home():
    return {"message": "CORS fixed!"}

#to analyze python code using python 
def analyze_python_code(file_path: str):
    pylint_result = subprocess.run(["pylint", file_path, "--output-format=json"], capture_output=True, text=True)
    pylint_output = json.loads(pylint_result.stdout) if pylint_result.stdout else []

    recommendations = []
    breakdown = {
        "naming": 10,               #Max 10
        "modularity": 20,           #Max 20
        "comments": 20,             #Max 20
        "formatting": 15,           #Max 15
        "reusability": 15,          #Max 15
        "best_practices": 20        #Max 20
    }
    score = 100  #Start with 100 and deduction on issues

    for issue in pylint_output:
        message = issue.get("message", "Issue detected")
        recommendations.append(message)

        if "naming" in message.lower():
            breakdown["naming"] = max(breakdown["naming"] - 2, 0)
        elif "function is too long" in message.lower() or "too many parameters" in message.lower():
            breakdown["modularity"] = max(breakdown["modularity"] - 2, 0)
        elif "missing docstring" in message.lower():
            breakdown["comments"] = max(breakdown["comments"] - 2, 0)
        elif "indentation" in message.lower() or "formatting" in message.lower():
            breakdown["formatting"] = max(breakdown["formatting"] - 2, 0)
        elif "duplicate code" in message.lower() or "repetitive" in message.lower():
            breakdown["reusability"] = max(breakdown["reusability"] - 2, 0)
        else:
            breakdown["best_practices"] = max(breakdown["best_practices"] - 2, 0)

    score = sum(breakdown.values())  #Total score is sum of breakdown values

    return max(score, 0), breakdown, recommendations[:5]  #Limit recommendations to 5

#To analyze .jsx and .js code using ESLint
def analyze_js_code(file_path: str):
    eslint_path = shutil.which("eslint")
    eslint_result = subprocess.run([eslint_path, file_path, "--format=json"], capture_output=True, text=True)
    eslint_output = json.loads(eslint_result.stdout) if eslint_result.stdout else []

    recommendations = []
    breakdown = {
        "naming": 10,               #Max 10
        "modularity": 20,           #Max 20
        "comments": 20,             #Max 20
        "formatting": 15,           #Max 15
        "reusability": 15,          #Max 15
        "best_practices": 20        #Max 20
    }
    score = 100  #Start with 100

    for issue in eslint_output:
        for message in issue.get("messages", []):
            msg_text = message.get("message", "Issue detected")
            recommendations.append(msg_text)

            if "camelCase" in msg_text or "naming" in msg_text:
                breakdown["naming"] = max(breakdown["naming"] - 2, 0)
            elif "too many lines" in msg_text or "complexity" in msg_text:
                breakdown["modularity"] = max(breakdown["modularity"] - 2, 0)
            elif "missing JSDoc" in msg_text:
                breakdown["comments"] = max(breakdown["comments"] - 2, 0)
            elif "indentation" in msg_text or "trailing spaces" in msg_text:
                breakdown["formatting"] = max(breakdown["formatting"] - 2, 0)
            elif "duplicate code" in msg_text or "DRY" in msg_text:
                breakdown["reusability"] = max(breakdown["reusability"] - 2, 0)
            else:
                breakdown["best_practices"] = max(breakdown["best_practices"] - 2, 0)

    score = sum(breakdown.values())

    return max(score, 0), breakdown, recommendations[:5]  #Limit recommendations to 5

#endpoint for analyze-code 
@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[-1]

    if file_extension not in [".py", ".js", ".jsx"]:
        return {"error": "Unsupported file type"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    if file_extension == ".py":
        score, breakdown, recommendations = analyze_python_code(temp_file_path)
    else:
        score, breakdown, recommendations = analyze_js_code(temp_file_path)

    os.remove(temp_file_path)

    return {
        "overall_score": score,
        "breakdown": breakdown,
        "recommendations": recommendations
    }
