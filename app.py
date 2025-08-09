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
            # Data Persistence: Save as JSON with yyyymmdd_hhmmss filename
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"records/{now}.json"
            output = {
                "date": str(selected_date),
                "data": edited_df.to_dict(orient="records")
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)
            st.success(f"Table saved as {filename}")
            # Reset state for next registration
            st.session_state["df"] = None
            st.session_state["confirmed"] = False

elif page == "View Records":
    st.header("View and Access Existing Records")
    record_dir = "records"
    files = [f for f in os.listdir(record_dir) if f.endswith(".json")]
    files.sort(reverse=True)
    selected_file = None
    if files:
        default_file = files[0]
        file_dates = [f.replace(".json","") for f in files]
        selected_date_str = st.selectbox("Select a report date:", file_dates, index=0)
        selected_file = f"{selected_date_str}.json"
        with open(os.path.join(record_dir, selected_file), "r", encoding="utf-8") as f:
            record = json.load(f)
        st.write(f"Report Date: {record['date']}")
        df = pd.DataFrame(record["data"])
        st.write("Edit 'MTK action item' below and click Save to update the record:")
        edited_df = st.data_editor(df, num_rows="dynamic", column_order=df.columns.tolist(), disabled=[col for col in df.columns if col != "MTK action item"], key="view_editor")
        if st.button("Save Changes to Record"):
            record["data"] = edited_df.to_dict(orient="records")
            with open(os.path.join(record_dir, selected_file), "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2)
            st.success(f"Changes saved to {selected_file}")
        st.dataframe(edited_df)
    else:
        st.info("No records found. Please register a test report first.")
