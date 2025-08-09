# GCF Agent (GCFA)

## Rewritten Prompt

Create a Streamlit application for managing test case (TC) data. The program must fulfill the following requirements:

1.  **User Interface:** Provide a text area where a user can paste a table directly from an email or web page.
2.  **Data Ingestion & Date:** Along with the pasted table, the user must select a date using a dedicated date input widget.
3.  **Data Processing:** The application should use an AI model to parse the pasted data and standardize it into a JSON format that conforms to a specific schema: '3GPP spec', 'TC number', 'Band', 'Result', and 'customer action item'.
4.  **Confirmation:** Display the parsed data in a DataFrame table, allowing the user to review and confirm its accuracy.
5.  **Data Enhancement:** After confirmation, automatically add a new column named 'MTK action item' to the DataFrame.
6.  **User Modification:** Implement an interactive interface that allows the user to directly edit the content of both the 'customer action item' and 'MTK action item' columns.
7.  **Data Persistence:** The final, confirmed, and potentially modified table should be saved as a JSON file.