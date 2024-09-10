# Piopiy API - Python SDK: Streaming Audio Feature

## Overview

The Piopiy API allows you to leverage powerful real-time audio streaming via WebSocket during voice calls. This feature is critical for use cases like live monitoring, real-time transcription, and AI-powered voice analysis.

## Features

- **Real-Time Audio Streaming**: Stream live call audio via WebSocket.
- **Flexible Listen Modes**: Choose to stream audio from the caller, callee, or both sides.
- **Configurable Audio Quality**: Select from various audio quality options (8000, 12000, 16000 Hz).
- **Stream on Answer**: Optionally start streaming only after the call is answered.

## Installation

First, ensure you have the `piopiy` package installed:

```bash
pip install piopiy
```

## Usage Example

Here’s how to set up audio streaming during a call using the Piopiy Python SDK:

```python
from piopiy import Action, RestClient, StreamAction

def main():
    # Create instances for actions and streaming
    action = Action()
    stream = StreamAction()

    # Define streaming parameters
    action.stream(
        'wss://your-websocket-url/webhook/stream',
        {
            'listen_mode': 'callee',  # Options: 'caller', 'callee', 'both'
            'voice_quality': 12000,  # Audio quality: '8000', '12000', '16000'
            'stream_on_answer': True  # Start streaming only when the call is answered
        }
    )



    # Example of making a call with streaming enabled
    piopiy = RestClient("your_app_id", "your_app_token")
    result = piopiy.voice.call(
        9198333333, 91898989,stream.PCMO(),
        {
            'timeout': 40,
            'loop': 2,
            'duration': 80,
            'ring_type': 'group'
        }
    )
    print(result)

if __name__ == '__main__':
    main()
```

## Streaming Method Parameters

1. **stream(url, options)**
      - `url` (String): The WebSocket URL where the audio should be streamed.
      - `options` (dict): Configuration settings:
           - `listen_mode` (String): Determines which side’s audio to stream. Options are `'caller'`, `'callee'`, or `'both'`.
           - `voice_quality` (String): The audio quality in Hz. Options are `8000`, `16000`.
           - `stream_on_answer` (bool): Whether to start streaming only when the call is answered (default is `True`).

## Example Use Cases

1. **Real-Time Transcription**: Stream call audio to a transcription service for live transcription.
2. **Live Monitoring**: Use WebSocket to stream live audio for call quality assurance.
3. **AI-Powered Conversational Analysis**: Integrate the streaming feature with AI models for sentiment analysis, customer interaction analysis, and real-time decision-making.
4. **Voice Biometrics and Verification**: Stream audio for live voice verification or biometric analysis.
