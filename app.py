import streamlit as st
import pandas as pd
import json
from datetime import date

st.title("GCF Agent (GCFA) - Test Case Manager")

# 1. User Interface: Paste table and select date
st.write("Paste your test case table below (copied from email or web page):")
example_input = """3GPP spec,TC number,Band,Result,customer action item\n38.521-1,TC001,n78,Pass,Check log for details\n38.521-1,TC002,n41,Fail,Request retest\n38.521-3,TC003,n1,Pass,No action needed"""
pasted_data = st.text_area("Paste Table Here", value=example_input, height=200)
selected_date = st.date_input("Select Date", value=date.today())

# 2. Data Processing: AI model to parse and standardize (mocked)
def mock_ai_parse_table(raw_text):
    # This is a placeholder for AI parsing logic
    # For demo, parse CSV-like text
    lines = [line for line in raw_text.splitlines() if line.strip()]
    if not lines:
        return pd.DataFrame(columns=["3GPP spec", "TC number", "Band", "Result", "customer action item"])
    header = lines[0].split(',')
    data = [line.split(',') for line in lines[1:]]
    df = pd.DataFrame(data, columns=header)
    # Ensure required columns
    for col in ["3GPP spec", "TC number", "Band", "Result", "customer action item"]:
        if col not in df.columns:
            df[col] = ""
    return df[["3GPP spec", "TC number", "Band", "Result", "customer action item"]]

if st.button("Parse Table"):
    df = mock_ai_parse_table(pasted_data)
    st.session_state["df"] = df
    st.session_state["confirmed"] = False

# 3. Confirmation: Display parsed data
if "df" in st.session_state:
    st.write("Parsed Table:")
    st.dataframe(st.session_state["df"])
    if st.button("Confirm Table"):
        st.session_state["confirmed"] = True

# 4. Data Enhancement: Add 'MTK action item' column
if st.session_state.get("confirmed"):
    df = st.session_state["df"].copy()
    if "MTK action item" not in df.columns:
        df["MTK action item"] = ""
    st.write("Edit 'customer action item' and 'MTK action item' below:")
    edited_df = st.data_editor(df, num_rows="dynamic")
    st.session_state["edited_df"] = edited_df
    if st.button("Save Table as JSON"):
        # 5. Data Persistence: Save as JSON
        output = {
            "date": str(selected_date),
            "data": edited_df.to_dict(orient="records")
        }
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        st.success("Table saved as output.json")
