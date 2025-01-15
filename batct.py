import streamlit as st
import requests
import pandas as pd

# Streamlit app title
st.title("Batch Speech-to-Text Converter")
st.write("Upload multiple audio files to transcribe them.")

# Function to send files to the API
def transcribe_file(api_url, api_key, app_id, file_path, src_lang="en", domain="generic"):
    headers = {
        "src_lang": src_lang,
        "domain": domain,
        "REV-API-KEY": api_key,
        "REV-APPNAME": "stt_file",
        "REV-APP-ID": app_id,
        "subtitles": "true",
    }
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(api_url, headers=headers, files=files)

        if response.status_code == 200:
            # Extract the transcription text
            return response.json().get("text")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except FileNotFoundError:
        return "File not found"

# API details
api_url = "https://revapi.reverieinc.com/upload"
api_key = "dc0ba72ee55460b2e90714d3907c16ca8172009c"
app_id = "com.rhythem.jain2021"

# File uploader for multiple audio files
uploaded_files = st.file_uploader("Upload audio files (mp3, wav, m4a)", 
                                   type=["mp3", "wav", "m4a"], 
                                   accept_multiple_files=True)

if uploaded_files:
    st.write("Files uploaded successfully. Processing...")
    
    # Initialize a list to store transcription results
    rows = []

    # Process each uploaded file
    for uploaded_file in uploaded_files:
        st.write(f"Processing: {uploaded_file.name}")

        # Save the uploaded file locally
        with open(uploaded_file.name, "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())

        # Transcribe the audio file
        transcription = transcribe_file(
            api_url=api_url,
            api_key=api_key,
            app_id=app_id,
            file_path=uploaded_file.name
        )

        # Append the result to the list
        rows.append({"File Name": uploaded_file.name, "Transcription": transcription})

    # Create a DataFrame from the results
    results = pd.DataFrame(rows)

    # Display transcription results in a table
    st.write("Transcription Results:")
    st.dataframe(results)

    # Provide a CSV download button
    st.download_button(
        label="Download CSV FILE",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="transcriptions.csv",
        mime="text/csv",
    )


# import subprocess
# import os
# from openpyxl import Workbook, load_workbook
# from tkinter import Tk
# from tkinter.filedialog import askopenfilenames

# # Configuration
# OUTPUT_FILE = "STT_results.xlsx"

# # Function to create the Excel file if it doesn't exist
# def create_workbook(file_path):
#     if not os.path.exists(file_path):
#         wb = Workbook()
#         ws = wb.active
#         ws.title = "Batch Results"
#         ws.append(["Audio File", "Actual Output", "Expected Output"])
#         wb.save(file_path)
#         print(f"Excel file created at {file_path}")

# # Function to append results to the Excel file
# def append_to_excel(file_path, data):
#     wb = load_workbook(file_path)
#     ws = wb.active
#     ws.append(data)
#     wb.save(file_path)

# # Function to process a single audio file using app.py
# def process_audio_with_app(file_path):
#     try:
#         # Run the app.py script and capture its output
#         result = subprocess.run(
#             ["python", "app.py", file_path], 
#             stdout=subprocess.PIPE, 
#             stderr=subprocess.PIPE, 
#             text=True
#         )
#         # Extract the actual output from the app.py result
#         actual_output = result.stdout.strip()
#         print(f"Processed {file_path}: {actual_output}")
#         return actual_output
#     except Exception as e:
#         print(f"Error processing {file_path}: {e}")
#         return None

# # Main function to process multiple files
# def process_files(file_paths, expected_outputs):
#     create_workbook(OUTPUT_FILE)

#     for i, file_path in enumerate(file_paths):
#         print(f"Processing file: {file_path}")
#         actual_output = process_audio_with_app(file_path)
#         expected_output = expected_outputs[i] if i < len(expected_outputs) else "N/A"
#         append_to_excel(OUTPUT_FILE, [os.path.basename(file_path), actual_output, expected_output])


# if __name__ == "__main__":
#     # File upload dialog
#     Tk().withdraw()
#     file_paths = askopenfilenames(title="Select Audio Files", filetypes=[("Audio Files", "*.wav *.mp3 *.flac *.m4a")])
#     print(f"Selected files: {file_paths}")
    
#     # Expected outputs for the files
#     expected_outputs = []
#     for file_path in file_paths:
#         expected_output = input(f"Enter expected output for {os.path.basename(file_path)}: ")
#         expected_outputs.append(expected_output)
    
#     # Process all selected files
#     process_files(file_paths, expected_outputs)