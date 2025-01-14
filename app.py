import asyncio
import pyaudio
import websockets

# Reverie API
API_URL = "wss://revapi.reverieinc.com/stream?"
apikey="dc0ba72ee55460b2e90714d3907c16ca8172009c&"
appid="com.rhythem.jain2021&"
appname="stt_stream&"
src_lang = "hi"
domain="generic"

API_URL = API_URL+apikey+appid+appname+src_lang+"&"+domain

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
buffer = 1600

# Initialize PyAudio
audio = pyaudio.PyAudio()

async def stream_audio():
    # Open the audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=buffer)

    print("Start speaking...")
    async with websockets.connect(API_URL) as websocket:
        try:
            while True: 
                # Read audio data from the microphone
                audio_buffer = stream.read(buffer, exception_on_overflow=False)
                
                # Send the audio buffer to the WebSocket
                await websocket.send(audio_buffer)
                
                # Receive and print the transcribed text
                response = await websocket.recv()

                print("{response}\n")  # Real-time text display
        except KeyboardInterrupt:
            print("\nStopping...")
            await websocket.send("--EOF--")  # Send EOF to terminate recognition
            stream.stop_stream()
            stream.close()
            audio.terminate()
  

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(stream_audio())




# import asyncio
# import pyaudio
# import websockets
# import streamlit as st

# # Streamlit Title and Language Dropdown
# st.title("Streaming Speech-to-Text Converter")

# # Dropdown to select language
# languages = {
#     "Indian English": "en",
#     "Hindi": "hi",
#     "Punjabi": "pa",
#     "Bengali": "bn"
# }
# selected_language = st.selectbox("Select Language", options=list(languages.keys()), index=0)

# # Reverie API Configuration
# API_BASE_URL = "wss://revapi.reverieinc.com/stream?"
# apikey = "dc0ba72ee55460b2e90714d3907c16ca8172009c&"
# appid = "com.rhythem.jain2021&"
# appname = "stt_stream&"
# src_lang = languages[selected_language]
# domain = "generic"

# API_URL = f"{API_BASE_URL}apikey={apikey}appid={appid}appname={appname}src_lang={src_lang}&domain={domain}"

# # Audio Configuration
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# buffer = 1600  # 100 ms frame size

# # Initialize PyAudio
# audio = pyaudio.PyAudio()

# # Async Function to Stream Audio and Transcribe
# async def stream_audio(transcription_placeholder):
#     # Open the audio stream
#     stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=buffer)

#     st.write("Start speaking...")

#     async with websockets.connect(API_URL) as websocket:
#         try:
#             while True:
#                 # Read audio data from the microphone
#                 audio_buffer = stream.read(buffer, exception_on_overflow=False)
                
#                 # Send the audio buffer to the WebSocket
#                 await websocket.send(audio_buffer)
                
#                 # Receive and display the transcribed text
#                 response = await websocket.recv()
#                 transcription_placeholder.text(response)  # Update real-time transcription
#         except KeyboardInterrupt:
#             st.write("Stopping...")
#             await websocket.send("--EOF--")  # Send EOF to terminate recognition
#             stream.stop_stream()
#             stream.close()
#             audio.terminate()

# # Start Streaming Button
# if st.button("Start Streaming"):
#     transcription_placeholder = st.empty()  # Create a placeholder for real-time updates
#     st.write("Starting speech-to-text conversion...")
#     asyncio.run(stream_audio(transcription_placeholder))
