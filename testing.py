import os
import streamlit as st
import pandas as pd
import requests
import json

st.title("Batch File Speech-to-Text Converter")
st.write("Upload multiple audio files to transcribe them and save the results in a CSV file.")

# Step 1: File upload
uploaded_files = st.file_uploader("Upload audio files", type=["mp3", "m4a", "wav"], accept_multiple_files=True)

if uploaded_files:
    # API details
    api_url = "https://revapi.reverieinc.com/"
    headers = {
        "src_lang": "en",
        "domain": "generic",
        "REV-API-KEY": "",
        "REV-APPNAME": "stt_file",
        "REV-APP-ID": "",
        "format": "mp3",
    }

    # Initialize results list
    results = []

    # Step 2: Process each uploaded file
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        st.write(f"Processing file: {file_name}")

        # Save the uploaded file locally
        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Send the file to the API
        with open(file_name, "rb") as audio_file:
            files = {"audio_file": audio_file}
            response = requests.post(api_url, headers=headers, files=files)

        # Process the API response
        if response.status_code == 200:
            try:
                response_data = response.json()
                transcription = response_data.get("text", "No text available")
            except json.JSONDecodeError:
                transcription = "Error parsing JSON response."
        else:
            transcription = f"API Error: {response.status_code}"

        # Append the result to the list
        results.append({"File Name": file_name, "Transcription": transcription})

        # Show progress in Streamlit
        st.write(f"Transcription for {file_name}: {transcription}")

    # Step 3: Create a DataFrame and display results
    df = pd.DataFrame(results)
    st.write("Transcription Results:")
    st.dataframe(df)

    # Step 4: Append results to the specified CSV file
    # file_path = st.text_input("Enter the file path to save the CSV:", "transcriptions_results.csv")
    file_path = "/Users/rhythemjain/Desktop/reverieSTTdemo/STTbatch.csv"

    file_exists = os.path.isfile(file_path)

    # Save to CSV with header only if the file doesn't exist
    df.to_csv(file_path, mode='a', index=False, header=not file_exists)

    # Provide a download button
    with open(file_path, "rb") as f:
        st.download_button(
            label="Download Transcriptions CSV",
            data=f,
            file_name="transcriptions_results.csv",
            mime="text/csv",
        )
