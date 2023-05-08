import json
import os
import uuid
from typing import Any

import pandas as pd
import requests


def trans_xlsx_to_json(bytes_data: Any, system: str) -> str:
    """
    Converts the contents of an XLSX file to a JSON file.

    Args:
    bytes_data (Any): The name of the XLSX file to be converted.
    system (str): The name of the system that the XLSX file corresponds to.

    Returns:
    None.
    """
    # Open the XLSX file
    xlsx_file = pd.ExcelFile(bytes_data)
    # Get a list of all sheet names
    sheet_names = xlsx_file.sheet_names
    # Create an empty list to store data from all sheets
    all_data = []
    # Loop through each sheet and append its contents to the list
    for sheet in sheet_names:
        # Read the sheet and fill in any empty cells with an empty string
        df = pd.read_excel(xlsx_file, sheet_name=sheet).fillna('')
        # Loop through each row in the sheet and create a dictionary for it
        for value in df.itertuples(index=False):
            client_section = getattr(value, "ClientSection")
            client_field = getattr(value, "ClientUIFieldname")
            is_require = getattr(value, "Required")
            vincere_field = getattr(value, "VincereField")
            customer_comment = getattr(value, "CustomersComment")
            vincere_comment = getattr(value, "VincereComments")
            # Append the dictionary to the list
            all_data.append({
                'id': uuid.uuid4().__str__(),
                'System': system,
                'Entity': sheet,
                'ClientSection': client_section,
                'ClientUIFieldname': client_field,
                'Required': is_require,
                'VincereField': vincere_field,
                "CustomersComment": customer_comment,
                'VincereComments': vincere_comment
            })
    # Convert the list to JSON
    json_data = json.dumps(all_data)
    return json_data


if __name__ == '__main__':
    # trans_xlsx_to_json(args.xlsx_file, args.json_file, args.system)
    import streamlit as st

    st.set_page_config(
        page_title="Insert New Documents for Vincere Field Mapping",
        page_icon=":shark:",
        initial_sidebar_state="expanded",
    )
    st.text("Insert New Documents for Vincere Field Mapping")
    st.divider()
    user_name = st.text_input("Username: ", key="user_name")
    password = st.text_input("Password: ", key="password", type="password")
    system = st.text_input("System: ", key="system")
    uploaded_file = st.file_uploader("Choose a excel file", type=[".xlsx"])
    if uploaded_file is not None:
        # To read file as bytes:
        _bytes_data = uploaded_file.getvalue()
        # Creating a json file name
        full_file_name = uploaded_file.name
        _json_file_name = ".".join([os.path.splitext(full_file_name)[0], "json"])
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_excel(uploaded_file)
        st.caption("Preview")
        st.write(dataframe)
        url = "https://brave-walrus-qpgce4.t1171joh.traefikhub.io/receive_json_data"
        headers = {'Content-Type': 'application/json'}
        json_data = trans_xlsx_to_json(_bytes_data, system)
        response = requests.post(url, headers=headers, json=json_data, auth=(user_name, password))
        # Display the response
        st.write(response.status_code)
        st.write(response.json())
