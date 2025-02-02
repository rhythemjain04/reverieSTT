import websocket
import pyaudio
import threading
import time
import ssl
import json

# API URL with authentication and configuration
API_URL = API_URL #with continous true parameter to get continous transcription and no websocket close error
# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 254

# Initialize PyAudio instance
p = pyaudio.PyAudio()

previous_output = ""  

def stream_audio(ws):
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Started streaming audio...")

    try:
        while ws.keep_running:
            data = stream.read(CHUNK, exception_on_overflow=False)
            ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
            time.sleep(0.0005)
    except Exception as e:
        print(f"Audio streaming error: {e}")
    finally:
        stream.stop_stream()
        stream.close()

def on_message(ws, message):
    global previous_output
    try:
        response = json.loads(message)
        print(response['text'])
        # if 'text' in response and response['text'].strip():
        #     current_output = response['text']

        #     if previous_output in current_output:
        #         unique_part = current_output[len(previous_output):].strip()
        #     else:
        #         unique_part = current_output

        #     if unique_part:
        #         print(unique_part)
        #         previous_output = current_output
    except Exception as e:
        print(f"Error parsing message: {e}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed.")

def on_open(ws):
    print("WebSocket connection opened.")
    threading.Thread(target=stream_audio, args=(ws,)).start()

def start_streaming():
    ws = websocket.WebSocketApp(API_URL,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})

start_streaming()


# import websocket
# import pyaudio
# import threading
# import time
# import ssl
# import json

# # API URL with authentication and configuration
# API_URL = "wss://revapi.reverieinc.com/stream?apikey=dc0ba72ee55460b2e90714d3907c16ca8172009c&appid=com.rhythem.jain2021&appname=stt_stream&src_lang=en&domain=generic&timeout=180&silence=0&continuous=true"

# # Audio configuration
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# CHUNK = 254

# # Initialize PyAudio instance
# p = pyaudio.PyAudio()

# previous_output = ""  

# def stream_audio(ws):
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
#     print("Started streaming audio...")

#     try:
#         while ws.keep_running:
#             data = stream.read(CHUNK, exception_on_overflow=False)
#             ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
#             time.sleep(0.0005)
#     except Exception as e:
#         print(f"Audio streaming error: {e}")
#     finally:
#         stream.stop_stream()
#         stream.close()

# def on_message(ws, message):
#     global previous_output
#     try:
#         response = json.loads(message)
#         if 'text' in response and response['text'].strip():
#             current_output = response['text']

#             if previous_output in current_output:
#                 unique_part = current_output[len(previous_output):].strip()
#             else:
#                 unique_part = current_output

#             if unique_part:
#                 print(unique_part)
#                 previous_output = current_output
#     except Exception as e:
#         print(f"Error parsing message: {e}")

# def on_error(ws, error):
#     print(f"WebSocket Error: {error}")

# def on_close(ws, close_status_code, close_msg):
#     print("WebSocket closed.")

# def on_open(ws):
#     print("WebSocket connection opened.")
#     threading.Thread(target=stream_audio, args=(ws,)).start()

# def start_streaming():
#     ws = websocket.WebSocketApp(API_URL,
#                                 on_open=on_open,
#                                 on_message=on_message,

#                                 on_error=on_error,
#                                 on_close=on_close)

#     ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})

# start_streaming()