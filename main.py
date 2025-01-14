import streamlit as st
import requests
import json

st.title("Speech-to-Text Converter")
st.write("Upload an audio file to convert it to text.")


uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "m4a", "wav"])

if uploaded_file:
    st.write("Uploaded file:", uploaded_file.name)

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File saved locally.")

    api_url = "https://revapi.reverieinc.com/"
    headers = {
        "src_lang": "en",
        "domain": "generic",
        "REV-API-KEY": "dc0ba72ee55460b2e90714d3907c16ca8172009c",
        "REV-APPNAME": "stt_file",
        "REV-APP-ID": "com.rhythem.jain2021",
        "format": "mp3",
    }

    with open(uploaded_file.name, "rb") as audio_file:
        files = {"audio_file": audio_file}
        response = requests.post(api_url, headers=headers, files=files)

    if response.status_code == 200:
        st.success("Transcription Successful!")
        
    
        try:
            response_data = response.json() 
            transcription = response_data.get("text", "No tex")
            st.write("Transcription:")
            st.text(transcription)  
        except json.JSONDecodeError:
            st.error("Error parsing the response JSON.")
            st.write(response.text) 
    else:
        st.error(f"Error: {response.status_code}")
        st.write(response.text)