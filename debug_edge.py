
import asyncio
import edge_tts
import sys
import datetime

async def main():
    print(f"Python version: {sys.version}")
    print(f"Current System Time: {datetime.datetime.now()}")
    try:
        print(f"Edge TTS Version: {edge_tts.__version__}")
    except AttributeError:
        print("Edge TTS Version: Unknown (no __version__ attribute)")

    TEXT = "[neutral]"
    VOICE = "en-US-AnaNeural"
    OUTPUT_FILE = "test_audio.mp3"

    print(f"Attempting to generate audio with voice: {VOICE}")
    try:
        communicate = edge_tts.Communicate(TEXT, VOICE)
        communicate.save_sync(OUTPUT_FILE)
        print("Success! Audio generated.")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
