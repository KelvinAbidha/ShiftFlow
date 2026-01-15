import streamlit as st
import pandas as pd
import logic
import analysis

st.set_page_config(
    page_title="ShiftFlow",
    page_icon="🏥",
    layout="centered"
)

st.title("ShiftFlow 🏥")
st.subheader("NHIF to SHA Transition Tool")

st.markdown("---")

# Create Tabs for Phase 2 Scope
tab1, tab2 = st.tabs(["Individual Calculator", "Market Impact Analysis"])

with tab1:
    # Day 3: Inputs
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        gross_salary = st.number_input("Gross Salary (KES)", min_value=0.0, value=50000.0, step=1000.0)
    with col_input2:
        procedure = st.selectbox("Select Procedure", options=list(logic.TARIFFS.keys()))

    # Logic Calculations
    old_deduction = logic.calculate_old_system(gross_salary)
    new_deduction = logic.calculate_new_system(gross_salary)
    diff = new_deduction - old_deduction

    # Day 4: Visualization & Metrics
    st.markdown("### Contribution Analysis")

    # Traffic-light logic: Green if cost goes down (diff < 0), Red if cost goes up (diff > 0)
    col1, col2, col3 = st.columns(3)
    col1.metric("Old NHIF", f"{old_deduction:,.2f}")
    col2.metric("New SHIF (2.75%)", f"{new_deduction:,.2f}")
    col3.metric("Difference", f"{diff:,.2f}", delta=f"{diff:,.2f}", delta_color="inverse")

    st.markdown("---")

    # Bar Chart
    st.subheader("Monthly Deduction Comparison")
    chart_data = pd.DataFrame({
        "System": ["Old NHIF", "New SHIF"],
        "Amount (KES)": [old_deduction, new_deduction]
    })
    st.bar_chart(chart_data, x="System", y="Amount (KES)")

    # Procedure Info
    st.subheader("Benefit Coverage (SHA)")
    limit = logic.TARIFFS[procedure]
    st.info(f"Under the new SHA system, the benefit limit for **{procedure}** is set to **KES {limit:,.0f}**.")

with tab2:
    st.header("Differential Rate Analysis")
    st.markdown("Analysis of gazetted tariffs vs legacy NHIF rebates.")
    
    # Load Analysis Data
    df_analysis, stats = analysis.run_differential_analysis()
    
    # Display Summary Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Procedures", stats["total_procedures_analyzed"])
    m2.metric("Net Financial Impact", f"KES {stats['net_financial_impact']:,.0f}")
    m3.metric("Avg Variance", f"KES {stats['average_variance']:,.0f}")
    
    # Display Data Table
    st.dataframe(df_analysis[["procedure", "old_rate", "new_rate", "variance", "impact_type"]], use_container_width=True)