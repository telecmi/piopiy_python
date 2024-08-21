# Piopiy API - Python SDK: Conversational AI Streaming with Full-Duplex Control

## Overview

The Piopiy API provides a robust real-time streaming capability optimized for Conversational AI scenarios. This feature allows for full-duplex communication via WebSocket, enabling the AI agent to not only listen to the call but also control the call flow by pausing, resuming, stopping the stream, playing music, and transferring the conversation to a human agent when needed.

This functionality is essential for building intelligent Conversational AI systems that can interact naturally with users, handle various scenarios, and switch to human agents seamlessly when required.

## Features

- **Real-Time Full-Duplex Communication**: Control the call via WebSocket with the ability to manage the call flow dynamically.
- **Stream Control**: Pause, resume, or stop the audio stream as needed.
- **Play Audio During Conversation**: Play music or other media during the call.
- **AI-Human Handoff**: Transfer the conversation to a human agent while maintaining the stream for monitoring or coaching.
- **High-Quality Audio Streaming**: Select between 8000, 16000, and 32000 Hz audio quality.

## Installation

First, ensure you have the `piopiy` package installed:

```bash
pip install piopiy
```

## Usage Example

Here’s how to set up a real-time conversation stream with control actions using the Piopiy Python SDK:

```python
from piopiy import RestClient, StreamAction, Action

def main():
    # Initialize Piopiy API client
    piopiy = RestClient("your_app_id", "your_app_token")

    # Create StreamAction instance
    stream = StreamAction()

    # Set up the stream with a WebSocket URL and configurations
    stream.stream(
        "wss://your-websocket-url/webhook/stream",
        {
            'listen_mode': 'callee',  # Options: 'caller', 'callee', 'both'
            'voice_quality': 8000,  # Audio quality: '8000', '16000', '32000'
            'stream_on_answer': True  # Start streaming only when the call is answered
        }
    )

    # Initiate a call with streaming enabled
    result = piopiy.voice.call(
        91989xxxxxx,  # First number to connect
        9188xxxxxx,   # PIOPIY Number
        stream.PCMO()
        {
            'loop': 1,        # Number of retry attempts
            'timeout': 40,    # Time to wait for the call to be answered
            'duration': 30    # Maximum call duration in seconds
        }
    )

    print(result)

    # Play music or audio during the call
    stream.playMusic("path/to/your_audio_file.wav")

    # Pause the streaming
    print(stream.pause())

    # Resume the streaming
    print(stream.resume())

    # Stop the streaming
    print(stream.stop())

    # Hang up the call
    stream.hangup()

    # Output the final PCMO actions
    print(stream.PCMO())

if __name__ == '__main__':
    main()
```

## Streaming Method Parameters

1. **stream(url, options)**

      - `url` (String): The WebSocket URL to stream the audio.
      - `options` (dict): Optional settings:
           - `listen_mode` (String): Specifies whose audio is streamed. Options: `'caller'`, `'callee'`, or `'both'`.
           - `voice_quality` (int): The audio quality in Hz. Options: `8000`, `16000`, or `32000`.
           - `stream_on_answer` (bool): Whether to start streaming only when the call is answered (default is `True`).

2. **call(from, to, caller_id, options)**

      - `from` (int): The caller’s phone number.
      - `to` (int): The receiver’s phone number.
      - `caller_id` (int): The Caller ID to be displayed.
      - `options` (dict): Optional settings:
           - `loop` (int): Number of retry attempts if the call is not answered.
           - `timeout` (int): Time to wait for the call to be answered.
           - `duration` (int): Maximum call duration in seconds.

3. **playMusic(audio_file)**

      - `audio_file` (String): The path or URL to the audio file to be played during the call.

4. **pause()**

      - Pauses the streaming temporarily.

5. **resume()**

      - Resumes the paused streaming.

6. **stop()**

      - Stops the streaming completely.

7. **hangup()**

      - Ends the call and terminates all actions.

## Example Use Cases

1. **Conversational AI**: Use the full-duplex WebSocket stream to build an interactive AI that can manage conversations, dynamically control call actions, and intelligently transfer the conversation to a human agent if needed.

2. **AI-Human Handoff**: Seamlessly switch from AI to a human agent when the AI is unable to handle the conversation, while keeping the stream active for real-time monitoring or coaching.

3. **Live Call Monitoring**: Monitor calls in real-time, even when they are transferred to other agents, allowing supervisors to coach or intervene if needed.
