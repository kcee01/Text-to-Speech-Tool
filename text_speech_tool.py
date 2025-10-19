import argparse
import pyttsx3
from gtts import gTTS

def list_voices(engine):
    """List available voices for pyttsx3."""
    voices = engine.getProperty('voices')
    print("\n🗣️ Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.id})")
    return voices

def save_wav(text, filename, voice_id=None, rate=150):
    """Generate WAV file using pyttsx3 (offline)"""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    # Set custom voice if provided
    if voice_id is not None:
        voices = engine.getProperty('voices')
        try:
            engine.setProperty('voice', voices[voice_id].id)
        except IndexError:
            print("⚠️ Invalid voice index, using default voice.")
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print(f"✅ Saved WAV file: {filename}")

def save_mp3(text, filename, lang='en'):
    """Generate MP3 file using gTTS (online, requires internet)"""
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    print(f"✅ Saved MP3 file: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Simple Text-to-Speech Tool with Voice Selection")
    parser.add_argument("--text", "-t", help="Text to convert to speech")
    parser.add_argument("--wav", help="Output WAV file (offline, uses pyttsx3)")
    parser.add_argument("--mp3", help="Output MP3 file (online, uses gTTS)")
    args = parser.parse_args()

    # 🔹 Prompt the user if no text was given
    if not args.text:
        args.text = input("📝 Enter the text you want to convert to speech:\n> ")

    # 🔹 Ask for output type if none provided
    if not args.wav and not args.mp3:
        choice = input("🎧 Do you want WAV or MP3 output? (type 'wav' or 'mp3'): ").strip().lower()
        filename = input("💾 Enter output filename (without extension): ").strip()
        if choice == "wav":
            args.wav = f"{filename}.wav"
        elif choice == "mp3":
            args.mp3 = f"{filename}.mp3"
        else:
            print("⚠️ Invalid choice. Please restart and type 'wav' or 'mp3'.")
            return

    # 🔹 Handle WAV with voice choice
    if args.wav:
        engine = pyttsx3.init()
        voices = list_voices(engine)
        try:
            voice_choice = int(input("\n🎙️ Choose a voice number from the list above: "))
        except ValueError:
            voice_choice = None
        save_wav(args.text, args.wav, voice_id=voice_choice)

    # 🔹 Handle MP3 (no custom voice support in gTTS)
    if args.mp3:
        save_mp3(args.text, args.mp3)

if __name__ == "__main__":
    main()
