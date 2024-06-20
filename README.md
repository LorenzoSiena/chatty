# Chatty the vocal [Cheshire Cat](https://github.com/cheshire-cat-ai/core) API Client in python
![chatty-cat-image](https://github.com/LorenzoSiena/chatty/assets/74120782/40008f86-b713-4beb-b924-dd35be8e99cd)

This project is a Python client for connecting to a WebSocket API using the `cheshire_cat_api` module. The client is configured to send and receive messages, including audio files, via WebSocket.

Best use with [Local Whisper Cat](https://github.com/LorenzoSiena/local_whisper_cat) and [Piper Cat](https://github.com/pazoff/Piper-Cat) for going full vocal and local.
## Requirements

Ensure you have the following modules installed:

- `datetime`
- `json`
- `time`
- `cheshire_cat_api`
- `pprint`
- `base64`
- `beautifulsoup4`
- `playsound`
- `threading`

You can install any missing dependencies using `pip`:

```sh
pip install datetime json time pprint base64 beautifulsoup4 playsound threading
```

## Configuration

The client uses a default configuration, but you can modify the parameters as follows:

```python
config = ccat.Config(
    base_url="localhost",
    port=1865,
    user_id="user_boy",
    auth_key="",
    secure_connection=False,
)
```
### Recording and Sending Audio Messages :microphone:

The client can record audio messages and send them to the server:

```python
while True:
    message = input("Write 'stop' to exit: \nPress Enter for recording")
    if message == "stop":
        break
    else:
        my_audio = record_audio()
        extra_fields["audio_key"] = read_file_as_base64(my_audio)
        cat_client.send(message, **extra_fields)
```

## Listening the response :sound:
If there is a message with an audio inside the playaudio function will play the response!
In the following response format it will look for the audio file 

```python
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
```

with the function on_message() on a separate thread 

```python
 if message["type"] == "chat" and "type='audio/mp3" in message["content"]:
        html_string = message["content"]
        url_audio_to_play = get_audio_file_path(
            html_string
        ) 
        print("The file you are looking for is at :--->" + url_audio_to_play)
        thread = threading.Thread(target=playsound, args=(url_audio_to_play,))
        thread.start()
```
## Running the Client

To run the client, ensure the WebSocket server is up and running, then start the client:

```python
python chatty.py
```

it will wait for your "enter" and than rec 10 seconds of audio,replying you what you said , the text and audio response

```python
# Connect to the WebSocket API
cat_client.connect_ws()

while not cat_client.is_ws_connected:
    time.sleep(1)

# Run the main loop
while True:
    message = input("Write 'stop' to exit: \nPress Enter for recording")
    if message == "stop":
        break
    else:
        my_audio = record_audio()
        extra_fields["audio_key"] = read_file_as_base64(my_audio)
        cat_client.send(message, **extra_fields)

# Close the connection
cat_client.close()
```

## Main Functions from cheshire_cat_api module

### Connection

The WebSocket connection is managed by the `CatClient` class from `cheshire_cat_api` with callbacks for specific events:

- `on_open`: Triggered when the connection is opened.
- `on_message`: Triggered when a new message arrives.
- `on_error`: Triggered when a WebSocket error occurs.
- `on_close`: Triggered when the connection is closed.

### Message Handling

The `on_message` method handles incoming messages, looking for audio files in the message content and playing them if found.

### File Reading and Encoding

The client includes functions to read files and encode them in base64:

- `read_file(file_path)`: Reads a file and returns its content.
- `read_file_as_base64(file_path)`: Reads a file and encodes its content to base64.

### Extracting Audio File Paths

The `get_audio_file_path` method extracts the audio file path from an HTML string and returns the complete URL to reach the audio file.

## Contributions

If you wish to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [GNU General Public License v3.0.](LICENSE).
