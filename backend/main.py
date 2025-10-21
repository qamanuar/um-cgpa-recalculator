from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import time

class Subject(BaseModel):
    credit: int
    old_grade: str
    new_grade: str

class CalculationRequest(BaseModel):
    current_cgpa: float
    credits_taken: int
    subjects: List[Subject]

GRADE_TO_POINT = {
    "A+": 4.0, "A": 4.0, "A-": 3.67, "B+": 3.33, "B": 3.00,
    "B-": 2.67, "C+": 2.33, "C": 2.00, "C-": 1.67,
    "D+": 1.33, "D": 1.00, "F": 0.0
}

def get_point(grade_input):
    return GRADE_TO_POINT.get(grade_input.upper(), 0.0)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5174", 
    "http://127.0.0.1:5500", 
    "https://um-cgpa-recalculator.netlify.app/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calculate-cgpa")
async def calculate_cgpa(request: CalculationRequest):
    time.sleep(0.5) #loading effect

    total_point = request.current_cgpa * request.credits_taken

    for s in request.subjects:
        if s.credit == 0:
            continue
            
        old_points = get_point(s.old_grade)
        new_points = get_point(s.new_grade)
        
        total_point -= (s.credit * old_points)
        total_point += (s.credit * new_points)
        
    final_cgpa = total_point / request.credits_taken if request.credits_taken > 0 else 0
    
    return {"new_cgpa": round(final_cgpa, 2)}