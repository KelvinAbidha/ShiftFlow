import json
import pandas as pd
import numpy as np

DATA_FILE = "mock_api.json"

def load_tariff_dataframe(file_path: str = DATA_FILE) -> pd.DataFrame:
    """
    Ingests raw JSON data into a Pandas DataFrame for analysis.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data["tariffs"])

def run_differential_analysis():
    """
    Day 4: Differential Rate Analyzer.
    Identifies pricing discrepancies and generates statistical summaries.
    """
    df = load_tariff_dataframe()
    
    # Vectorized calculation of Variance using NumPy/Pandas
    df["variance"] = df["new_rate"] - df["old_rate"]
    
    # Categorize impact
    df["impact_type"] = np.where(df["variance"] > 0, "Benefit Improved",
                        np.where(df["variance"] < 0, "Benefit Reduced", "No Change"))

    # Statistical Summary
    summary = {
        "total_procedures_analyzed": int(len(df)),
        "net_financial_impact": float(df["variance"].sum()),
        "average_variance": float(df["variance"].mean()),
        "procedures_improved": int(len(df[df["variance"] > 0])),
        "procedures_reduced": int(len(df[df["variance"] < 0]))
    }
    
    return df, summary

if __name__ == "__main__":
    df_result, stats = run_differential_analysis()
    print("--- Differential Analysis Summary ---")
    print(json.dumps(stats, indent=2))
    print("\n--- Detailed Discrepancies ---")
    print(df_result[["procedure", "old_rate", "new_rate", "variance", "impact_type"]])