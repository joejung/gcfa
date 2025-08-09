### Rewritten Prompt

---

# GCF Agent (GCFA) Streamlit Application

Create a Streamlit application named "GCFA" that provides two main functionalities for managing test case (TC) data: registering new test reports and viewing existing ones.

---

### 1. Register a New Test Report

The application must include a section for users to register a new test report.

* **Registration Trigger:** A dedicated button titled "Register Test Report as a Record" should initiate the process.
* **User Input:** The user will be required to provide two inputs:
    1.  A text area for pasting a table directly from an email or web page.
    2.  A date selector to specify the date of the report.
* **Data Processing:** The application must use an AI model to parse the pasted table, conforming the data to a JSON format with the following columns: '3GPP spec', 'TC number', 'Band', 'Result', and 'customer action item'.
* **User Confirmation:** Display the parsed data in a Streamlit DataFrame table, allowing the user to review and confirm its accuracy before proceeding.
* **Data Enrichment:** After confirmation, automatically add a new column named 'MTK action item' to the DataFrame.
* **User-Modifiable Fields:** The application must allow the user to directly modify the contents of both the 'customer action item' and 'MTK action item' columns within the table.
* **Data Persistence:** The final, confirmed, and potentially modified table must be saved as a JSON file. The filename should follow a `yyyymmdd_hhmmss` format to ensure uniqueness and proper sorting.

---

### 2. View and Access Existing Records

The application must also provide a way to access previously saved reports.

* **Default View:** Upon launch, the application should automatically display the most recently saved test report.
* **Record Selection:** Provide a date selector UI element that allows the user to browse and select a specific date.
* **Dynamic Display:** When a user selects a date, the application must load and display the corresponding test report from the stored JSON files.