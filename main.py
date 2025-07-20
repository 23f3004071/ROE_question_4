from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# ✅ Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "23f3004071@ds.study.iitm.ac.in"
EXAM = "tds-2025-05-roe"

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Load CSV
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content), sep=';')

    # Clean column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Strip strings and normalize casing in 'category'
    df['category'] = df['category'].astype(str).str.strip().str.lower()

    # Clean 'amount' column: remove commas, strip spaces, convert to float
    df['amount'] = df['amount'].astype(str).str.replace(",", "").str.strip()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # Filter to category = "food"
    total = df[df['category'] == 'food']['amount'].sum()

    return {
        "answer": round(total, 2),
        "email": EMAIL,
        "exam": EXAM
    }
