# Piopiy API - Python SDK

## Overview

Piopiy API provides a comprehensive Python SDK for managing and controlling voice interactions using our PCMO Actions. This SDK allows developers to integrate voice functionalities such as making calls,bi-directional streaming for conversational AI, playing audio, recording, and more into their Python applications.

## PCMO Features

- **Make Calls**: Initiate voice calls between two parties or multiple numbers.
- **Play and Get Input**: Play a media file or URL and get user input via DTMF.
- **Play Music**: Stream audio files or URLs during a call.
- **Text-to-Speech**: Convert text to speech during a call.
- **Set Values and Inputs**: Set custom values and collect user inputs.
- **Record Calls**: Record voice calls.
- **Hangup Calls**: Terminate calls programmatically.
- **Stream Audio**: Stream real-time audio via WebSocket during a call.

---

## Authentication

The API requires an API Key and Secret for authentication, passed during the initialization of the `RestClient` object.

## Dependencies

- `Python` 3.x or higher
- `pip`
- `piopiy`

## Installation

To use the Piopiy API, install the piopiy package from PyPI:

```bash
pip install piopiy
```

## Usage

Here’s a basic example of how to use the Piopiy API:

```python
from piopiy import RestClient, Action

# Initialize the RestClient with your appid and app token
piopiy = RestClient("your_appid", "your_app_token")

# Call two numbers with custom caller ID
try:
    response = piopiy.voice.call("first_phone_number", "piopiy_callerid", "second_phone_number", {
        'loop': 1,
        'timeout': 40,
        'duration': 30
    })
    print(response)
except Exception as error:
    print(error)

# Call and perform PCMO action
action = Action()

action.playGetInput(
    "https://example.com/webhook/dtmf",
    "https://example.com/your_audio_file.wav",
    {'max_digits': 3, 'max_retry': 2}
)

try:
    response = piopiy.voice.call("dest_phone_number", "piopiy_callerid", action.PCMO(), {
        'loop': 1,
        'timeout': 40,
        'duration': 30
    })
    print(response)
except Exception as error:
    print(error)
```

## Make Call

The call() method in the Piopiy Python SDK is designed to handle various types of call interactions. It supports connecting two numbers, managing multiple numbers, and executing PCMO (Programmable Call Media Operations) actions during a call.

## Usage

### 1. Making a Basic Call

To initiate a call between two numbers:

```python
from piopiy import RestClient

# Initialize the RestClient with your appid and app token
piopiy = RestClient("your_appid", "your_app_token")

try:
    # Call two numbers with custom caller ID and additional options
    response = piopiy.voice.call(
        9194xxxxxx,         # first number to connect
        9180xxxxxx,         # Caller ID
        9180xxxxxx,         # second number to connect
        {
            'duration': 30,     # (Optional) Maximum duration of the call in seconds
            'timeout': 40,      # (Optional) Time to wait for the call to be answered
            'loop': 1,          # (Optional) Number of retry attempts if call is not answered
            'record': True      # (Optional) Whether to record the call
        }
    )
    print('Call connected, answer URL:', response)
except Exception as error:
    print('Error:', error)
```

### 2. Making a Call with PCMO Actions

To make a call and perform specific PCMO actions, such as playing an audio file:

```python
from piopiy import RestClient, Action

def main():
    # Initialize the RestClient with your appid and app token
    piopiy = RestClient("your_appid", "your_app_token")

    # Define PCMO actions
    action = Action()
    action.playMusic('https://example.com/your_music_file.wav')

    try:
        # Call two numbers with custom caller ID, PCMO actions, and additional options
        response = piopiy.voice.call(
            9194xxxxxx,         # first number to connect
            9180xxxxxx,         # Caller ID
            action.PCMO(),      # PCMO actions to execute during the call
            {
                'duration': 30,     # (Optional) Maximum duration of the call in seconds
                'timeout': 40,      # (Optional) Time to wait for the call to be answered
                'loop': 1,          # (Optional) Number of retry attempts if call is not answered
                'record': True      # (Optional) Whether to record the call
            }
        )
        print('Call with PCMO actions connected, answer URL:', response)
    except Exception as error:
        print('Error:', error)

if __name__ == '__main__':
    main()
```

### 3. Streaming Audio in a Call

The `stream` method allows you to stream audio to the call in real-time using a WebSocket URL.

Here is an example of how to use the `stream` feature in the Piopiy API:

```python
from piopiy import Action, RestClient

def main():
    # Initialize RestClient with your API Key and Secret
    piopiy = RestClient("YOUR_API_KEY", "YOUR_API_SECRET")

    action = Action()

    # Define the stream action
    action.stream(
        'wss://telecmi.com/stream',
        {
            'listen_mode': 'callee',
            'voice_quality': 8000,
            'stream_on_answer': True
        }
    )

    try:
        # Call two numbers with custom caller ID, and execute the stream action
        response = piopiy.voice.call(
            9198333333,              # First number to connect
            91898989,                # Caller ID
            action.PCMO(),           # PCMO actions including the stream
            {
                'timeout': 40,
                'loop': 2,
                'duration': 80,
                'ring_type': 'group'
            }
        )
        print('Call with streaming audio connected, answer URL:', response)
    except Exception as error:
        print('Error:', error)

if __name__ == '__main__':
    main()
```

### 4. Handling Multiple Numbers

To attempt connecting a call to multiple numbers sequentially:

```python
from piopiy import RestClient

def main():
    # Initialize the RestClient with your appid and app token
    piopiy = RestClient("your_appid", "your_app_token")

    try:
        # Call two numbers with custom caller ID and additional options
        response = piopiy.voice.call(
            9194xxxxxx,          # first number to connect
            9180xxxxxx,          # Caller ID
            [9180xxxxx, 9196xxxx], # Array of second numbers to connect
            {
                'duration': 30,   # (Optional) Maximum duration of the call in seconds
                'timeout': 40,    # (Optional) Time to wait for each call to be answered
                'loop': 1,        # (Optional) Number of retry attempts for each number
                'record': True    # (Optional) Whether to record the call
            }
        )
        print('Call to multiple numbers connected, answer URL:', response)
    except Exception as error:
        print('Error:', error)

if __name__ == '__main__':
    main()
```

### `options` (dictionary) - Optional

- `duration` (Number): Maximum call duration in seconds.
- `timeout` (Number): Time in seconds to wait for each call to be answered.
- `loop` (Number): Number of retry attempts for each call.
- `record` (Boolean): Whether to record the call.

---

## PCMO (Piopiy Call Management Object)

The PCMO is a powerful tool that enables you to define specific actions to be executed during a call. These actions can include playing audio files, collecting user input, speaking text, and more.

### Setting Up PCMO Actions

To use PCMO (Programmable Call Management Object) in Python with the Piopiy SDK, you need to create an instance of the `Action` class, define the actions you want to perform, and then pass these actions to the `call()` method. Here is how you can do it:

```python
from piopiy import RestClient, Action

# Initialize RestClient with your API Key and Secret
piopiy = RestClient("YOUR_API_KEY", "YOUR_API_SECRET")

# Create an instance of the Action class
action = Action()

```

### Example Actions

1. **Playing Audio**

      - Play a specified audio file or URL during the call.

      ```javascript
      action.playMusic("https://example.com/your_music_file.wav");
      ```

2. **Collecting DTMF Input**

      - Play a message and collect user input via DTMF tones.

      ```javascript
      action.playGetInput(
              "https://example.com/webhook/dtmf",
              "https://example.com/your_audio_file.wav",
              {max_digit: 3, max_retry: 2}
      );
      ```

3. **Text-to-Speech**

      - Convert and play text as speech during the call.

      ```javascript
      action.speak("Hello, Welcome to Telecmi");
      ```

4. **Setting Custom Values**

      - Set custom values for use during the call session.

      ```javascript
      action.setValue("name");
      ```

5. **Collecting Input**

      - Collect user input, such as key presses, and send them to a specified URL.

      ```javascript
      action.input("https://example.com/action", {
              timeout: 20,
              max_digit: 4,
              min_digit: 2,
      });
      ```

6. **Recording the Call**

      - Record the call session.

      ```javascript
      action.record();
      ```

7. **Ending the Call**

      - Hang up the call.

      ```javascript
      action.hangup();
      ```

8. **Connecting to Other Numbers**

      - Attempt to connect the caller to multiple numbers in sequence until one answers.

      ```javascript
      action.call(9198xxxxxx, [9180xxxx, 9180xxxx], { duration: 10, timeout: 20, loop: 2, record: true });
      ```

9. **Streaming Audio**

      - Stream audio in real-time during the call using a WebSocket URL.

      ```javascript
      action.stream("wss://telecmi.com/stream", {
              listen_mode: "callee", // Options: "callee", "caller", or "both"
              voice_quality: 12000, // Voice quality in bits per second
              stream_on_answer: true, // Start streaming after the call is answered
      });
      ```

10. **Clearing Actions**

       - Clear all defined actions.

       ```javascript
       action.clear();
       ```

### Using PCMO in a Call

After defining the desired actions, use the `action.PCMO()` method to pass them to the `call()` method:

```python
from piopiy import RestClient, Action

def main():
    # Initialize RestClient with your API Key and Secret
    piopiy = RestClient("YOUR_API_KEY", "YOUR_API_SECRET")

    # Create an instance of the Action class
    action = Action()

    # Define PCMO actions
    action.playMusic('https://example.com/your_music_file.wav')

    try:
        # Call two numbers with custom caller ID, PCMO actions, and additional options
        response = piopiy.voice.call(
            9194xxxxxx,          # first number to connect
            9180xxxxxx,          # Caller ID
            9180xxxxxx,          # second number to connect
            action.PCMO(),       # PCMO actions
            {
                'duration': 30,   # (Optional) Maximum duration of the call in seconds
                'timeout': 40,    # (Optional) Time to wait for the call to be answered
                'loop': 1,        # (Optional) Number of retry attempts if call is not answered
                'record': True    # (Optional) Whether to record the call
            }
        )
        print('Call with PCMO actions connected, answer URL:', response)
    except Exception as error:
        print('Error:', error)

if __name__ == '__main__':
    main()

```

### PCMO Method Parameters

1. **playMusic(audioFileOrUrl)**

      - `audioFileOrUrl` (String): The URL or path to the audio file to be played.

2. **playGetInput(url, audioFileOrUrl, options)**

      - `url` (String): The URL to send the DTMF input to.
      - `audioFileOrUrl` (String): The URL or path to the audio file to be played.
      - `options` (Dictionary): Optional settings:
           - `max_digit` (Number): Maximum number of digits to capture.
           - `max_retry` (Number): Number of retry attempts.

3. **speak(text)**

      - `text` (String): The text to convert to speech.

4. **setValue(key)**

      - `key` (String): The key name for the value to set.

5. **input(url, options)**

      - `url` (String): The URL to send the input data to.
      - `options` (Dictionary): Optional settings:
           - `timeout` (Number): Time in seconds to wait for input.
           - `max_digit` (Number): Maximum number of digits to collect.
           - `min_digit` (Number): Minimum number of digits to collect.

6. **record()**

      - No parameters. Starts recording the call.

7. **hangup()**

      - No parameters. Ends the call.

8. **call(from, to, options)**

      - `from` (Number): The caller's phone number.
      - `to` (Number | Array): A single receiver's phone number or an array of phone numbers.
      - `options` (Dictionary): Optional settings:
           - `duration` (Number): Maximum call duration in seconds.
           - `timeout` (Number): Time to wait for each call to be answered.
           - `loop` (Number): Number of retry attempts for each number.
           - `record` (Boolean): Whether to record the call.

9. **stream(url, options)**

      - `url` (String): The WebSocket URL for streaming audio during the call.
      - `options` (Dictionary): Optional settings:
           - `listen_mode` (String): Specifies who hears the streamed audio. Options are `callee`, `caller`, or `both`.
           - `voice_quality` (String): The desired voice quality in bits per second. Options are `8000`, `16000`.
           - `stream_on_answer` (Boolean): Whether to start streaming after the call is answered.

10. **PCMO()**

       - No parameters. Returns the PCMO Object.

11. **clear()**

       - No parameters. Clears all defined actions.
