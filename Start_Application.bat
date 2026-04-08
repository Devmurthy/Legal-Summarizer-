@echo off
echo Starting Legal Summarizer Backend (Python/Flask)...
start cmd /k "cd backend && python app.py"

echo Starting Legal Summarizer Frontend (React/Vite)...
start cmd /k "cd frontend && npm run dev"

echo Successfully started both services in separate windows!
echo The Frontend User Interface is accessible at http://localhost:5173
echo The Backend API is accessible at http://localhost:5002
