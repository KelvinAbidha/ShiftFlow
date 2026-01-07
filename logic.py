"""
Core logic for ShiftFlow: Calculating NHIF vs SHA contributions.
"""

# Constants based on Phase 1 Roadmap
SHIF_RATE = 0.0275
SHIF_FLOOR = 300.0

def calculate_old_system(gross_salary: float) -> float:
    """
    Calculates NHIF contribution based on the historical bracketed system.
    Cap historically at KES 1,700.
    """
    # TODO: Implement NHIF brackets (Day 2 Task)
    return 0.0

def calculate_new_system(gross_salary: float) -> float:
    """
    Calculates SHIF contribution: 2.75% of gross, floor KES 300, no maximum cap.
    """
    # TODO: Implement SHIF logic (Day 2 Task)
    return 0.0