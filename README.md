# Chatty the vocal Cheshire Cat API Client in python

This project is a Python client for connecting to a WebSocket API using the `cheshire_cat_api` module. The client is configured to send and receive messages, including audio files, via WebSocket.

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
- `recorder`
- `threading`

You can install any missing dependencies using `pip`:

```sh
pip install datetime json time pprint base64 beautifulsoup4 playsound recorder threading
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

## Main Functions

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

### Recording and Sending Audio Messages

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

## Running the Client

To run the client, ensure the WebSocket server is up and running, then start the client:

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

## Contributions

If you wish to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [GNU General Public License v3.0.](LICENSE).
