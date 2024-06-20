import datetime
import json
import time
import cheshire_cat_api as ccat
from pprint import pprint
import base64
from bs4 import BeautifulSoup
from playsound import playsound
from recorder import record_audio
import threading


# Connection settings with default values
config = ccat.Config(
    base_url="localhost",
    port=1865,
    user_id="user_boy",
    auth_key="",
    secure_connection=False,
)


def on_open():
    # This is triggered when the connection is opened
    print("Connection opened!")


def on_message(message: str):
    # This is triggered when a new message arrives

    """ Looking for the audio file in the message
    {
        "type" :
            "chat",
        "content" :
            "<audio controls autoplay><source 
            src='/admin/assets/voice/voice_20240617_140731.wav' 
            type='audio/mp3'
            >
            Your browser does not support the audio element.</audio>"
        }
    """

    message = json.loads(message)
    
    if message["type"] == "chat" and "type='audio/mp3" in message["content"]:
        html_string = message["content"]
        url_audio_to_play = get_audio_file_path(
            html_string
        ) 
        print("The file you are looking for is at :--->" + url_audio_to_play)
        thread = threading.Thread(target=playsound, args=(url_audio_to_play,))
        thread.start()
        
        #playsound(url_audio_to_play) was blocking the thread and the connection was closed by the server because of a timeout

    elif message["type"] == "chat" and "type='audio/wav" not in message["content"]:
        
        print("Your user input was :")
        print(message["why"]['input'])
        print("Your response :")
        print(message["content"])
        
    


def on_error(exception: Exception):
    # This is triggered when a WebSocket error is raised
    print(str(exception))


def on_close(status_code: int, message: str):
    # This is triggered when the connection is closed
    print(f"Connection closed with code {status_code}: {message}")


def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, "rb") as file:
        return file.read()


def read_file_as_base64(file_path):
    """Reads a file and encodes its content to base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def get_audio_file_path(html_string):
    """
    get the audio file path from the html string
    and returns the url to reach the audio file
    """

    soup = BeautifulSoup(html_string, "lxml")
    source_tag = soup.find("source")
    src_value = source_tag["src"]

    url_audio = "http://" + config.base_url + ":" + str(config.port) + src_value
    return url_audio


audio_file = ""

extra_fields = {
    "audio_key": "",  # Base64 encoded audio file
    "audio_type": "audio/ogg",  # MIME type of the audio file
    "audio_name": "msg45430839-160807.ogg",  # final part of the audio file path , should be better use timestamp
    "encodedBase64": True,  # Flag to indicate that the audio is encoded in base64
}


# Cat Client
cat_client = ccat.CatClient(
    config=config,
    on_open=on_open,
    on_close=on_close,
    on_message=on_message,
    on_error=on_error,
)

url_audio_to_play = ""
# Connect to the WebSocket API
cat_client.connect_ws()

    
while not cat_client.is_ws_connected:
    # A better handling is strongly advised to avoid an infinite loop
    time.sleep(1)


while True:
    # Send a message to the WebSocket
    print("url i'm reaching for " + config.base_url + ":" + str(config.port))
    message = input("Write 'stop' to exit: \nPress Enter for recording")
    if message == "stop":
        break
    else:
        print("I'm recording for 10 seconds...")
        my_audio=record_audio()
        extra_fields["audio_key"] = read_file_as_base64(my_audio)
        print("I'm sending the audio to the server")
        try:
            cat_client.send(message, **extra_fields)
        except Exception as e:
            print("Error sending the message because of " + str(e))
            print("Closing the connection")
            cat_client.close()
            print("Trying to reconnecting to the server")
            cat_client.connect_ws()

# Close connection
cat_client.close()
