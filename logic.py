"""
Core logic for ShiftFlow: Calculating NHIF vs SHA contributions.
"""

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

# Tariff Examples (Procedure: Limit in KES)
TARIFFS = {
    "Normal Delivery": 11200,
    "C-Section": 32600,
    "MRI": 11000,
}