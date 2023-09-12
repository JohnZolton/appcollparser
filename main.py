import pandas as pd
import csv
import streamlit as st
from playsound import playsound
import webbrowser
import os
from io import StringIO
from io import BytesIO
import base64  


def replace_space_after_WO(input_string):
    if len(input_string) > 2:
        if input_string[2] == ' ':
            input_string = input_string[:2] + '-' + input_string[3:]
            input_string = handleSuffix(input_string)
            return input_string
        if input_string[2].isdigit():
            input_string = input_string[:2] + '-' + input_string[2:]
            input_string = handleSuffix(input_string)
            return input_string
    return input_string

def handleSuffix(input_string):
    if input_string[-2].isalpha():
        if input_string[-3] == ' ':
            input_string = input_string[:-3] + '-' + input_string[-2:]
        else:
            input_string = input_string[:-2] + '-' + input_string[-2:]
    return input_string

# Define the input and output file paths
#input_csv_file = 'US AppColl Import List 2.csv'  # Replace with the path to your input CSV file
output_csv_file = 'output.csv'  # Replace with the desired path for the output CSV file

# Create a list to store the modified rows
modified_rows = []


st.set_page_config(page_title="AppColl document title formatter")
st.header("AppColl document title formatter")
file = st.file_uploader("Upload your file (csv)")

if file is not None:
    file_type = file.name.split('.')[-1].lower()
    if file_type == 'csv':
        # Read the input CSV file and modify the rows
        with file:
            csv_reader = csv.reader(file.read().decode('utf-8').splitlines())
            print(csv_reader)
            for row in csv_reader:
                if len(row[2]) == 0: continue
                if len(row) >= 3:
                    row[2] = replace_space_after_WO(row[2])
                    
                modified_rows.append(row)
            st.write("CSV File Contents:")
            st.write(modified_rows)

            df = pd.DataFrame(modified_rows)
            print(df)
            df.to_csv(output_csv_file, index=False, header=False, encoding='utf-8')



            # Create a download link for the modified CSV
            with open(output_csv_file, 'rb') as csvfile:
                st.download_button(
                label="Download Modified CSV",
                data=csvfile.read(),
                file_name="output.csv",
                key="download_button"
            )
            st.write(f"Modified data has been written to '{output_csv_file}'.")
    else:
        st.write("error, must be .CSV file")