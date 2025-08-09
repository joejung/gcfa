import streamlit as st
import pandas as pd
import json
from datetime import date, datetime
import os

st.set_page_config(layout="wide")

st.sidebar.title("GCFA Navigation")
page = st.sidebar.radio("Choose a function:", ["Register Test Report", "View Records"])

st.title("GCF Agent (GCFA)")
st.write("Manage test case (TC) data: Register new test reports and view existing ones.")

RECORDS_FILE = "records.json"

def load_records():
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_records(records):
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def mock_ai_parse_table(raw_text):
    # --- AI Model Integration Placeholder ---
    # Replace this block with your AI model call to parse and standardize pasted data.
    # For example, you could use OpenAI, HuggingFace, or a custom model here.
    # The model should return a list of dicts with keys:
    # '3GPP spec', 'TC number', 'Band', 'Result', 'customer action item'
    # DEMO: Fallback to simple CSV parsing for now
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

if page == "Register Test Report":
    st.header("Register a New Test Report")
    if "df" not in st.session_state:
        st.session_state["df"] = None
    if "confirmed" not in st.session_state:
        st.session_state["confirmed"] = False
    st.write("Paste your test case table below (copied from email or web page):")
    example_input = """3GPP spec,TC number,Band,Result,customer action item\n38.521-1,TC001,n78,Pass,Check log for details\n38.521-1,TC002,n41,Fail,Request retest\n38.521-3,TC003,n1,Pass,No action needed"""
    pasted_data = st.text_area("Paste Table Here", value=example_input, height=200, key="register_text")
    selected_date = st.date_input("Select Date", value=date.today(), key="register_date")
    project_name = st.text_input("Project Name (e.g., TabS11, TabS10)", key="register_project")
    if st.button("Register Test Report as a Record"):
        df = mock_ai_parse_table(pasted_data)
        st.session_state["df"] = df
        st.session_state["confirmed"] = False
    # Confirmation: Display parsed data
    if st.session_state["df"] is not None:
        st.write("Parsed Table:")
        st.dataframe(st.session_state["df"])
        if st.button("Confirm Table"):
            st.session_state["confirmed"] = True
    # Data Enhancement: Add 'MTK action item' column
    if st.session_state.get("confirmed"):
        df = st.session_state["df"].copy()
        if "MTK action item" not in df.columns:
            df["MTK action item"] = ""
        st.write("Edit 'customer action item' and 'MTK action item' below:")
        edited_df = st.data_editor(df, num_rows="dynamic", key="register_editor")
        st.session_state["edited_df"] = edited_df
        if st.button("Save Table as JSON"):
            # Load existing records
            records = load_records()
            # Add new record
            new_record = {
                "date": str(selected_date),
                "project_name": project_name,
                "data": edited_df.to_dict(orient="records")
            }
            records.append(new_record)
            save_records(records)
            st.success(f"Test report saved to {RECORDS_FILE}")
            # Reset state for next registration
            st.session_state["df"] = None
            st.session_state["confirmed"] = False

elif page == "View Records":
    st.header("View and Access Existing Records")
    records = load_records()
    if records:
        # Sort records by date (descending)
        records_sorted = sorted(records, key=lambda r: r["date"], reverse=True)
        date_options = [f"{r['date']} ({r.get('project_name','')})" for r in records_sorted]
        selected_idx = st.selectbox("Select a report date:", range(len(date_options)), format_func=lambda i: date_options[i], index=0)
        selected_record = records_sorted[selected_idx]
        st.write(f"Report Date: {selected_record['date']}")
        st.write(f"Project Name: {selected_record.get('project_name','')}")
        df = pd.DataFrame(selected_record["data"])
        st.write("Edit 'MTK action item' below and click Save to update the record:")
        edited_df = st.data_editor(df, num_rows="dynamic", column_order=df.columns.tolist(), disabled=[col for col in df.columns if col != "MTK action item"], key="view_editor")
        if st.button("Save Changes to Record"):
            selected_record["data"] = edited_df.to_dict(orient="records")
            save_records(records)
            st.success(f"Changes saved to {RECORDS_FILE}")
        st.dataframe(edited_df)
    else:
        st.info("No records found. Please register a test report first.")
