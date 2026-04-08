# Legal Document Summarizer

A full-stack web application designed to extract text from legal documents (PDFs & Images), perform Named Entity Recognition (NER), and generate both extractive and abstractive summaries mathematically. 

This project consists of a **React (Vite)** frontend and a **Python (Flask)** backend.

## 🛠️ Prerequisites
Before running this project on a brand new system, ensure you have the following installed:
1. **Node.js** (v16 or higher) - For running the React frontend.
2. **Python** (3.9 or higher) - For running the Flask backend.
3. **Tesseract OCR (Optional but recommended)** - If you plan on extracting text from images or scanned PDFs, you must install Tesseract OCR on your system and ensure it is added to your system's PATH.

---

## ⚙️ Step 1: Backend Setup (Python)
The backend uses Flask, HuggingFace Transformers, and SpaCy.

1. Open your terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment (Recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the required SpaCy Language Model for Entity Recognition:
   ```bash
   python -m spacy download en_core_web_sm
   ```

---

## 🎨 Step 2: Frontend Setup (React)
The frontend uses Vite, React, and Lucide Icons.

1. Open a *new* terminal window and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install the necessary Node packages:
   ```bash
   npm install
   ```

---

## 🚀 Step 3: Running the Application

### The Easy Way (Windows Only)
If you are on Windows, simply double-click the **`Start_Application.bat`** file located in the root folder. It will automatically open two terminals and boot up both the frontend and backend simultaneously.

### The Manual Way (Mac / Linux / Windows)
You need to run both servers at the same time.

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```
*(The API will start running on http://localhost:5002)*

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
*(The User Interface will start running on http://localhost:5173)*

Open your browser and navigate to **http://localhost:5173** to use the application!
