"""
Core logic for ShiftFlow: Calculating NHIF vs SHA contributions.
"""
import json
import os
from pydantic import BaseModel

# Constants based on Phase 1 Roadmap
SHIF_RATE = 0.0275
SHIF_FLOOR = 300.0

# Historical NHIF Brackets (Limit, Deduction)
NHIF_BRACKETS = [
    (5999, 150),
    (7999, 300),
    (11999, 400),
    (14999, 500),
    (19999, 600),
    (24999, 750),
    (29999, 850),
    (34999, 900),
    (39999, 950),
    (44999, 1000),
    (49999, 1100),
    (59999, 1200),
    (69999, 1300),
    (79999, 1400),
    (89999, 1500),
    (99999, 1600),
    (float('inf'), 1700),
]

# Pydantic Models for Architecture ---
class SalaryInput(BaseModel):
    gross_salary: float

class ContributionOutput(BaseModel):
    gross_salary: float
    old_nhif: float
    new_shif: float
    difference: float
    notes: str

class TariffOutput(BaseModel):
    procedure: str
    old_reimbursement: float
    new_reimbursement: float
    variance: float

# --- Core Calculation Logic ---
def calculate_old_system(gross_salary: float) -> float:
    """
    Calculates NHIF contribution based on the historical bracketed system.
    Cap historically at KES 1,700.
    """
    for limit, amount in NHIF_BRACKETS:
        if gross_salary <= limit:
            return float(amount)
    return 1700.0

def calculate_new_system(gross_salary: float) -> float:
    """
    Calculates SHIF contribution: 2.75% of gross, floor KES 300, no maximum cap.
    """
    contribution = gross_salary * SHIF_RATE
    return max(contribution, SHIF_FLOOR)

# --- Day 3: Data Ingestion (JSON Parser) ---
def load_gazetted_tariffs(file_path="mock_api.json"):
    """
    Parses the JSON tariff file to populate reimbursement rules.
    Returns tuple of (New SHIF Tariffs, Old NHIF Tariffs).
    """
    new_tariffs = {}
    old_tariffs = {}
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            for item in data.get("tariffs", []):
                proc = item["procedure"]
                new_tariffs[proc] = item["new_rate"]
                old_tariffs[proc] = item["old_rate"]
    
    return new_tariffs, old_tariffs

# Initialize Data
TARIFFS, NHIF_TARIFFS = load_gazetted_tariffs()

def calculate_benefit_comparison(procedure: str) -> TariffOutput:
    """
    Translates the reimbursement rule by comparing Legacy vs Modern limits.
    """
    new_rate = float(TARIFFS.get(procedure, 0))
    old_rate = float(NHIF_TARIFFS.get(procedure, 0))
    return TariffOutput(
        procedure=procedure,
        old_reimbursement=old_rate,
        new_reimbursement=new_rate,
        variance=new_rate - old_rate
    )