from fastapi import FastAPI
from logic import SalaryInput, ContributionOutput, TariffOutput, calculate_old_system, calculate_new_system, calculate_benefit_comparison
from analysis import run_differential_analysis

app = FastAPI(
    title="ShiftFlow Migration Engine",
    description="API for translating legacy NHIF rules to 2025 SHIF framework.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "active", "system": "ShiftFlow Engine"}

@app.post("/calculate", response_model=ContributionOutput)
def calculate_contribution(data: SalaryInput):
    """
    Translates a gross salary into both Old NHIF and New SHIF contributions.
    """
    gross = data.gross_salary
    old_val = calculate_old_system(gross)
    new_val = calculate_new_system(gross)
    diff = new_val - old_val
    
    note = "Cost increases" if diff > 0 else "Cost savings"
    
    return ContributionOutput(
        gross_salary=gross,
        old_nhif=old_val,
        new_shif=new_val,
        difference=diff,
        notes=note
    )

@app.get("/reimbursement/{procedure}", response_model=TariffOutput)
def translate_reimbursement_rule(procedure: str):
    """
    Automates the translation of reimbursement rules:
    Returns the financial shift from Legacy NHIF to Modern SHIF for a specific procedure.
    """
    return calculate_benefit_comparison(procedure)

@app.get("/impact/summary")
def get_impact_summary():
    """
    Returns the statistical summary of the transition impact across all gazetted tariffs.
    """
    _, summary = run_differential_analysis()
    return summary